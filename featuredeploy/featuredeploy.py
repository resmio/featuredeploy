import os
import subprocess
import sys
from datetime import datetime
from time import sleep
from uuid import uuid4

import digitalocean
import pytz

from .readconfig import read_config, read_environemnt, read_startup

USAGE = ('USAGE: featuredeploy deploy [$branch [$commit]] | ls | rm $id | '
         'rmbranch $branch | rmall | ttl $ip $hours | logs $ip)')
NAME_PREFIX = 'resmioapp--'


dir_path = os.path.dirname(os.path.realpath(__file__))
startup_script = os.path.join(dir_path, 'deploy.sh')
config = read_config()


def get_manager():
    return digitalocean.Manager(token=config['DIGITAL_OCEAN_TOKEN'])


def expand_config_vars(stri, extra):
    for key, value in config.items():
        if key.isupper():
            stri = stri.replace('{{' + key + '}}', value)
    for key, value in extra.items():
        if key.isupper():
            stri = stri.replace('{{' + key + '}}', value)
    return stri


def create_droplet(branch, githash):
    user_data = open(startup_script).read()

    # use all keys registered at digitalocean
    keys = get_manager().get_all_sshkeys()

    setenvs = []
    for var, value in read_environemnt().items():
        assert var.replace('_', '').isalnum()
        export = '{var}=$(cat <<-{eof}\n{value}\n{eof}\n)'.format(
            value=value,
            var=var,
            eof=uuid4().hex)
        setenvs.append(export)

    user_data = expand_config_vars(
        user_data,
        {'GITHASH': githash,
         'BRANCH': branch,
         'SETENVS': ' '.join(setenvs),
         'STARTUP': read_startup()})

    droplet = digitalocean.Droplet(token=config['DIGITAL_OCEAN_TOKEN'],
                                   name='{}{}--{}'.format(
                                       NAME_PREFIX, githash, branch),
                                   region='fra1',
                                   image='docker-20-04',
                                   size_slug='s-2vcpu-4gb',
                                   user_data=user_data,
                                   ssh_keys=keys,  # Automatic conversion
                                   backups=False)
    droplet.create()
    return droplet


def get_servers():
    for droplet in get_manager().get_all_droplets():
        if droplet.name.startswith(NAME_PREFIX):
            name = droplet.name[len(NAME_PREFIX):]
        else:
            continue
        naive_created = datetime.strptime(
            droplet.created_at,
            '%Y-%m-%dT%H:%M:%SZ')
        utc_created = naive_created.replace(tzinfo=pytz.UTC)
        local_created = utc_created.astimezone(pytz.timezone('Europe/Berlin'))
        pretty_created = local_created.strftime('%d.%m %H:%M')

        githash, branch = name.split('--')

        assert droplet.name.startswith(NAME_PREFIX)
        yield dict(
            id=droplet.id,
            pretty_created=pretty_created,
            ip=droplet.ip_address,
            githash=githash,
            branch=branch,
            droplet_status=droplet.status)


def list_servers():
    servers = list(get_servers())
    if servers:
        longest_branch = max(len(s['branch']) for s in servers)
        longest_ip = max(len(s.get('ip') or '') for s in servers)
        for s in servers:
            print('{id} | {ip: <%s} | {githash} | {branch: <%s} | '
                   '{pretty_created} | {droplet_status}'
                   % (longest_ip, longest_branch)
                   ).format(**s)


def deploy(branch=None, githash=None):

    if branch is None:
        # get information on the current commit and branch
        branch = subprocess.check_output(
            'git rev-parse --symbolic-full-name --abbrev-ref HEAD'.split())
        branch = branch.decode()
        branch = branch.rstrip('\n')

    if githash is None:
        githash = subprocess.check_output('git rev-parse HEAD'.split())
        githash = githash.decode()
        githash = githash.rstrip('\n')
        commitmsg = subprocess.check_output(
            ['git', 'log', '--format=%B', '-n', '1', githash])
        commitmsg = commitmsg.decode()
        commitmsg = commitmsg.rstrip('\n')

        print('Deploying {} "{}" (branch {})'.format(githash, commitmsg, branch))
    else:
        print('Deploying {} (branch {})'.format(githash, branch))

    githash = githash[:8]

    # remove older instances
    rmbranch(branch)

    new_droplet = create_droplet(branch, githash)

    print('Waiting for ip address ...')
    while True:
        servers = dict((s['id'], s['ip']) for s in get_servers())
        ip = servers[new_droplet.id]
        if ip:
            print(ip)
            return
        sleep(1)


def rm(id):
    print('Removing instance {} ...'.format(id))
    droplet = get_manager().get_droplet(id)
    ip = droplet.ip_address

    exit_code = None
    if ip:
        exit_code = remote_execute(ip, 'sh -e /root/self_destroy', silent=True)

    if exit_code is not None and exit_code:
        print('Graceful remove failed, removing hard')
        try:
            assert droplet.destroy()
        except Exception as e:
            if 'droplet is still being created' in str(e):
                sleep(5)
                print('Waiting on {}'.format(id))
                rm(id)
            else:
                raise e
        print('Removed hard')
    else:
        print('Graceful remove succeded')


def rmbranch(branch):
    # remove older instances
    for s in get_servers():
        if s['branch'] == branch:
            rm(s['id'])


def rmall():
    for s in get_servers():
        rm(s['id'])


def remote_execute(ip, cmd, silent=False):
    if not silent:
        print('Executing: ' + cmd)
        extra = {}
    else:
        devnull = open(os.devnull, 'w')
        extra = {'stdout': devnull, 'stderr': devnull}

    return subprocess.Popen([
        'ssh',
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'ConnectTimeout=1',
        'root@{}'.format(ip), cmd],
        **extra).wait()


def logs(ip):
    remote_execute(ip, 'cd app && docker-compose logs --follow')


def ttl(ip, hours):
    if not hours.isdigit():
        print('hours (2nd arg) should be a number')
        sys.exit(1)

    # dummy job, so we always have some
    remote_execute(ip, "echo '' | at 'now +1 hour'")

    # delete all jobs
    remote_execute(ip, "at -l |  awk '{print $1;}' | xargs at -d")

    # at our destroy job with new schedule
    remote_execute(ip, "cat /root/self_destroy | at 'now + %s hours'" % hours)

    print()
    print('{} will self destroy in {} hours'.format(ip, hours))


def getarg():
    try:
        return sys.argv[2]
    except IndexError:
        print('Argument missing')
        sys.exit(1)


def gettwoargs():
    try:
        return sys.argv[2], sys.argv[3]
    except IndexError:
        print('Needs two arguments')
        sys.exit(1)


def gettwoargsmax():
    try:
        return sys.argv[2], sys.argv[3]
    except IndexError:
        try:
            return sys.argv[2]
        except IndexError:
            return []


def main():
    try:
        cmd = sys.argv[1]
    except IndexError:
        print(USAGE)
        sys.exit(1)
    if cmd in ('ls', 'list', 'ps'):
        list_servers()
    elif cmd == 'log' or cmd == 'logs':
        logs(getarg())
    elif cmd == 'deploy':
        deploy(*gettwoargsmax())
    elif cmd in ('rm', 'kill', 'destroy'):
        rm(getarg())
    elif cmd == 'rmbranch':
        rmbranch(getarg())
    elif cmd == 'rmall':
        rmall()
    elif cmd == 'ttl':
        ttl(*gettwoargs())
    elif cmd == 'help' or cmd == '--help':
        print(USAGE)
    else:
        print(USAGE)
        sys.exit(1)


if __name__ == '__main__':
    main()
