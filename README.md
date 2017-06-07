

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

The `.featuredeploy/` folder consits of the following files:
```
.featuredeploy/
├── config.ini
├── environment.ini
└── startup

0 directories, 3 files
```

`.featuredeploy/startup` is an executable file that has to start at port 8000, you get an ubuntu 16.04 but it is recommended to only rely on the docker and docker-compose installation to bring the app up.

`.featuredeploy/environment.ini`
Are optional environemnt variables that are exported for the startup script. This is an ad-hoc solution to maintain secret configurations, it's an vim encrypted file, make sure to use the `blowfish2` encryption method or newer if available.

`.featuredeploy/config.ini` are configuration keys. See the next section for available options. It is also vim encrypted.

### `config.ini` configurations

| Key | Description |
| --- | --- |
|DIGITAL_OCEAN_TOKEN| The token of an digital ocean account to start the machine where the deployment happens.|
|GITHUB_INSTALLATION_ID|TODO: ask steve|
|GIT_CLONE| The app to clone|
|HIPCHAT_ROOM_ID|The room to post the hipchat message|
|HIPCHAT_TOKEN| an hipchat token to send a success message after deployment|
|HTTP_AUTH_PASS| The password for the http authentification|
|HTTP_AUTH_USER | the user for the http authentification|
|PRIVATE_SSH_KEY| An private ssh key that you probably need for the git clone, see https://developer.github.com/v3/guides/managing-deploy-keys/|
|STATUS_SERVER_FULL_NAME|TODO figure out|
|STATUS_SERVER_SECRET|a secret shared with the status server|
|STATUS_SERVER_URL| the url of the status server|


### The Sombrero status server
The sombrero status server is is an integration of this featuredeploy command line interface with github.
Its source code can be found here: [https://github.com/resmio/sombrero](https://github.com/resmio/sombrero).
The sombrero status server gets input over http callbacks and updates the pull request at github.
With the Sombrero integration you can start the deployment of the last commit of a github pull request by just adding a label to it.
The status of the deployment will be updated on the pull request and appropiate GIFs will be used for general amusement.

For a better overview of you sombrero plays with the featuredeploy CLI you can  [open the Diagram](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1#R5VlLc5swEP41HJ0BZGN89CtpZtJpJj60PcqwBrUYuUL4kV9fCYRBxjg4sZNpk0MirVYraffbT4tioPFye8fwKvxKfYgM2%2FS3BpoYtm11kSn%2BSMkul%2FT7bi4IGPGVUimYkWdQQjUvSIkPiabIKY04WelCj8YxeFyTYcboRldb0EhfdYUDqAlmHo7q0u%2FE52EudXtmKf8CJAiLlS1Tjcyx9ztgNI3VeoaNFtlPPrzEhS2ln4TYp5uKCE0NNGaU8ry13I4hkr4t3JbPu20Y3e%2BbQcxbTXDUPviuODv4whWqSxkPaUBjHE1L6Sg7H0gLpuiFfBmJpiWav4DznYomTjkVotLCA6UrpZevKRdq3LYSJTRlntLqKiBgFoDS6u1dJqAIdAmc7YQKgwhzstatY4WJYK%2Bnpg4Zw7uKwoqSmCcVy49SIBQUvFGBUgVuu3%2Fg4%2FP0RSPfQdGrHKUUZXFriOEgN7%2FGUaqOPF2DPAIaGrYTCV%2BNfLIWzUA2IzzPshX7MoZqXKxRUTkxi8GSrpvnHWCJw5brEGGQkGc8zxQkepSzhXZvZPQmQoIjEsRCEMFCzl0D40Rk5lCJl8T3MxRmOxrt821MI8qyVYuMK%2FYjLcDWOMIbah9lOmoIdI6DS1kyb5yBjbTAdhVCz4NfDS%2Bdwo4y27EHugm6WCQiA3QMnYuabg00d4SH6bwWwzLbZfw2IeEwW%2BEsKTeC%2FfXwNiZyLQiNjrVNPV0sV%2FU3JRNbRcDCCgs7ZrOnNUedyiX3knwIW8J%2FSPGN5SLV%2F6nU2nKlnPMIjIijAFNzX8efFyHLGlr3uVOwW%2FcgDDlfq1llJM5l3cN1UPeyLFqYryTE0OOExsdZNF35mIO8jkL5%2B%2FHpMzCi%2BwIjmgM9cy9Ch9YBGR7A6yJk2KvFfkaXcwaMXoIOj7i7lqqt6XBfTbwLHVq181%2BEDnsVMrx%2B4dg3aoVjA5JbQ7W1A%2B0GVmkozsYMMlrJB%2BbsREX2lFVipwu4%2F5mMTqeNICPX6r2NgArKQVdgHNR03TQAw4dVRHctyvVKfJ0%2FqfyOHMkwd1TchG0zC91%2BtLDCTuLp2iwglURs2a4yJLsfxhBvrZbaMkS%2FhoNbQQEpAz3iVY54uG8ZpY%2B%2Bq7rOe95V6BootaoYzWB5XSS6l0fi6x45HD2UDnrhkcO5bnlu1b9XTz1yTBmjrPXjxiz1PEiS1voTSDiju8%2FxDIJOpnzHvLEPnyvedutudTPFZ6V9hUvYrWFqQgLCsdT55gGOj8T%2BPk44jgVc%2FhEOdszrcbDolk%2FVuf%2FL%2Fweg6V8%3D)
