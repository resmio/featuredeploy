import os
from ConfigParser import ConfigParser
from cStringIO import StringIO

from vimdecrypt import decryptfile

config_file = os.path.join(
    os.getcwd(),
    '.featuredeploy',
    'config.ini')

environment_file = os.path.join(
    os.getcwd(),
    '.featuredeploy',
    'environment.ini')

startup_file = os.path.join(
    os.getcwd(),
    '.featuredeploy',
    'startup')


def vim_decrypt_file(fname, password):
    with open(fname, 'rb') as fp:
        args = type('Args', (), {'verbose': False})
        text = decryptfile(fp.read(), password, args)
        return StringIO(text)


def get_encrypt_key():
    try:
        return os.environ['SECRET_KEY']
    except KeyError:
        with open('.encrypt_key') as f:
            content = f.read()
            content = content.rstrip('\n')
            return content


def read_encrypted_config(config_file):
    conf = ConfigParser()
    conf.optionxform = str
    encrypt_key = get_encrypt_key()
    conf.readfp(vim_decrypt_file(config_file, encrypt_key))
    return dict(conf.items('main'))


def read_config():
    return read_encrypted_config(config_file)


def read_environemnt():
    return read_encrypted_config(environment_file)


def read_startup():
    with open(startup_file) as f:
        return f.read()
