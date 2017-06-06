

featuredeploy allows to deploy specific commits of an application for testing by e.g. QA

To deploy the current commit of a branch run:
```
$ featuredeploy deploy
Deploying d8332a057cc09deebb6c4c7a1a35d576d8189866 "Adding file" (branch my-branch)
Waiting for ip address ...
178.62.231.207
```

The feature will be deployed to the given ip, until then the build process is monitored, HTTP basic authentification is used.

To list deployed instances:
```
$ featuredeploy ls
50918708 | 188.166.76.183 | 5f590f20 | master                        | 06.06 12:38 | active
50924872 | 188.166.92.121 | 9db8968a | 5061-my-awesome-branch        | 06.06 13:50 | active
50927969 | 178.62.214.231 | d80d3dff | 5064-my-not-so-awesome-branch | 06.06 14:23 | active
```
You can also delete, schedule a delete and do other actions on deployed instances:
```
$ featuredeploy -h
USAGE: featuredeploy (deploy | ls | rm $id | rmbranch $branch | rmall | ttl $ip $hours | logs $ip)
```
An instance will be removed after a given time period or when its branch gets merged.

Featuredeploys is application independent, application specific things like credentials or setting up the app is configured inside a `.featuredeploy` folder inside the project root of the application you wish to deploy.

The `.featuredeploy` folder consits of the following files:
```
.featuredeploy/
├── config.ini
├── environment.ini
└── startup

0 directories, 3 files
```
