
## Featuredeploy

### Overview
featuredeploy allows to deploy specific commits of an application for testing by e.g. QA

To deploy the latest commit of the current branch run:
```
$ featuredeploy deploy
Deploying d8332a057cc09deebb6c4c7a1a35d576d8189866 "Adding file" (branch my-branch)
Waiting for ip address ...
178.62.231.207
```

The feature will be deployed to the printed ip, the build process can be monitored over HTTP, basic authentication is used.

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
An instance will be removed after two days or when its branch gets merged.

### Configuration
Featuredeploy is application independent, everything application specific like credentials is configured inside a `.featuredeploy` folder at your project root folder of the application you wish do deploy.

The `.featuredeploy/` folder consists of the following files:
```
.featuredeploy/
├── config.ini
├── environment.ini
└── startup
```

`.featuredeploy/startup` is an executable file that has to start your app at port 8000, you get an ubuntu 16.04 but it is recommended to only rely on the docker and docker-compose installation to run the app. Probably you also want to create test data.

`.featuredeploy/environment.ini`
Are optional environment variables that are exported for the startup script. This is an ad-hoc solution to maintain secret configurations, it's an vim encrypted file make sure to use the `blowfish2` encryption method or newer if available.

`.featuredeploy/config.ini` are configuration keys, also vim encrypted. See the table for configuration options:

| Key | Description |
| --- | --- |
|DIGITAL_OCEAN_TOKEN| The token of a digital ocean account to start the machine where the deployment happens.|
|GITHUB_INSTALLATION_ID| A Github installation id for sombrero. |
|GIT_CLONE| The app to clone| Where to clone your app from. |
|HIPCHAT_TOKEN| A hipchat token to send a success message after deployment.|
|HIPCHAT_ROOM_ID|A Hipchat room to post a success message.|
|HTTP_AUTH_PASS| The password for the http authentification.|
|HTTP_AUTH_USER | the user for the http authentification.|
|PRIVATE_SSH_KEY| A private ssh key that you probably need for the git clone, see https://developer.github.com/v3/guides/managing-deploy-keys/ |
|STATUS_SERVER_FULL_NAME| The github user- and repo name separated by a slash, e.g. docker/compose (Sombrero needs that) |
|STATUS_SERVER_SECRET|a secret shared with the status server to authenticate http callbacks. |
|STATUS_SERVER_URL| the url of the status server ending with a trailing slash. |


### The Sombrero status server
The sombrero status server is is an integration of this featuredeploy command line interface with github.
Its source code can be found here: [https://github.com/resmio/sombrero](https://github.com/resmio/sombrero).
The sombrero status server gets input over http callbacks and updates the pull request at github.
With the Sombrero integration you can start the deployment of the last commit of a github pull request by just adding a label to it.
The status of the deployment will be updated on the pull request and appropiate GIFs will be used for general amusement.

For a better overview of how sombrero plays with the featuredeploy CLI you can [open this Diagram](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1#R5VlLc5swEP41HJ0BZGN89CtpZtJpJj60PcqwBrUYuUL4kV9fCYRBxjg4sZNpk0MirVYraffbT4tioPFye8fwKvxKfYgM2%2FS3BpoYtm11kSn%2BSMkul%2FT7bi4IGPGVUimYkWdQQjUvSIkPiabIKY04WelCj8YxeFyTYcboRldb0EhfdYUDqAlmHo7q0u%2FE52EudXtmKf8CJAiLlS1Tjcyx9ztgNI3VeoaNFtlPPrzEhS2ln4TYp5uKCE0NNGaU8ry13I4hkr4t3JbPu20Y3e%2BbQcxbTXDUPviuODv4whWqSxkPaUBjHE1L6Sg7H0gLpuiFfBmJpiWav4DznYomTjkVotLCA6UrpZevKRdq3LYSJTRlntLqKiBgFoDS6u1dJqAIdAmc7YQKgwhzstatY4WJYK%2Bnpg4Zw7uKwoqSmCcVy49SIBQUvFGBUgVuu3%2Fg4%2FP0RSPfQdGrHKUUZXFriOEgN7%2FGUaqOPF2DPAIaGrYTCV%2BNfLIWzUA2IzzPshX7MoZqXKxRUTkxi8GSrpvnHWCJw5brEGGQkGc8zxQkepSzhXZvZPQmQoIjEsRCEMFCzl0D40Rk5lCJl8T3MxRmOxrt821MI8qyVYuMK%2FYjLcDWOMIbah9lOmoIdI6DS1kyb5yBjbTAdhVCz4NfDS%2Bdwo4y27EHugm6WCQiA3QMnYuabg00d4SH6bwWwzLbZfw2IeEwW%2BEsKTeC%2FfXwNiZyLQiNjrVNPV0sV%2FU3JRNbRcDCCgs7ZrOnNUedyiX3knwIW8J%2FSPGN5SLV%2F6nU2nKlnPMIjIijAFNzX8efFyHLGlr3uVOwW%2FcgDDlfq1llJM5l3cN1UPeyLFqYryTE0OOExsdZNF35mIO8jkL5%2B%2FHpMzCi%2BwIjmgM9cy9Ch9YBGR7A6yJk2KvFfkaXcwaMXoIOj7i7lqqt6XBfTbwLHVq181%2BEDnsVMrx%2B4dg3aoVjA5JbQ7W1A%2B0GVmkozsYMMlrJB%2BbsREX2lFVipwu4%2F5mMTqeNICPX6r2NgArKQVdgHNR03TQAw4dVRHctyvVKfJ0%2FqfyOHMkwd1TchG0zC91%2BtLDCTuLp2iwglURs2a4yJLsfxhBvrZbaMkS%2FhoNbQQEpAz3iVY54uG8ZpY%2B%2Bq7rOe95V6BootaoYzWB5XSS6l0fi6x45HD2UDnrhkcO5bnlu1b9XTz1yTBmjrPXjxiz1PEiS1voTSDiju8%2FxDIJOpnzHvLEPnyvedutudTPFZ6V9hUvYrWFqQgLCsdT55gGOj8T%2BPk44jgVc%2FhEOdszrcbDolk%2FVuf%2FL%2Fweg6V8%3D)

### Misc notes
Featuredeploy is used regularly at [resmio](https://resmio.com/) and designed as a general purpose application, nevertheless the [The Rule of Three](https://blog.codinghorror.com/rule-of-three/) applies.
Meaning that it fits very well the needs of the company it was designed for but may need adaptations to work for you. Also note that the code did not get more dedication than it needs to fulfill its purpose. Also note furthermore that of course the digital ocean account associated with the digital ocean token from the configuration file will be billed. There is no rate limiting of deployment invocations by adding the github label or calling the featuredeploy CLI directly.
