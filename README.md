
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

To list deployed instances run:
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
Featuredeploy is application independent, everything application specific like credentials is configured inside a `.featuredeploy` folder at the project root folder of the application you wish do deploy.

The `.featuredeploy/` folder consists of the following files:
```
.featuredeploy/
├── config.ini
├── environment.ini
└── startup
```

`.featuredeploy/startup` is an executable file that has to start your app at port 8000, you get an ubuntu 16.04 but it is recommended to only rely on the docker and docker-compose installation to run the app. Probably you also want to create test data at this step at this step.

`.featuredeploy/environment.ini`
Are optional environment variables that are exported for the startup script. This is an ad-hoc solution to maintain secret configurations, it's a vim encrypted file make sure to use the `blowfish2` encryption method or newer if available. Also put the key in an `.encrypt_key` file or in the `SECRET_KEY` environemnt variable so the configuration can be read on featuredeploy invocations.

`.featuredeploy/config.ini` are configuration keys, also vim encrypted. See the table for configuration options:

| Key | Description |
| --- | --- |
|DIGITAL_OCEAN_TOKEN| The token of a digital ocean account to start the machine where the deployment happens.|
|GITHUB_INSTALLATION_ID| A Github installation id for the featuredeploy server. |
|GIT_CLONE| The app to clone| Where to clone your app from. |
|HIPCHAT_TOKEN| A hipchat token to send a success message after deployment.|
|HIPCHAT_ROOM_ID|A Hipchat room to post the success message.|
|HTTP_AUTH_USER | the user for the http authentification.|
|HTTP_AUTH_PASS| The password for the http authentification.|
|PRIVATE_SSH_KEY| A private ssh key that you probably need for the git clone, see https://developer.github.com/v3/guides/managing-deploy-keys/ |
|STATUS_SERVER_FULL_NAME| The github user- and repo name separated by a slash, e.g. docker/compose (Sombrero needs that) |
|STATUS_SERVER_SECRET|a secret shared with the featuredeyploy server status server to authenticate http callbacks. |
|STATUS_SERVER_URL| the url of the status server ending with a trailing slash. |


### The feature deploy status server
The feature deploy status server is an integration of this featuredeploy command line interface with github.
Its source code can be found here: [https://github.com/resmio/featuredeploy-server](https://github.com/resmio/featuredeploy-server).
The feature deploy status server gets input over http callbacks and updates the pull request at github.
With the Sombrero integration you can start the deployment of the last commit of a github pull request by just adding a label to it.
The status of the deployment will be updated on the pull request and appropiate GIFs will be posted for general amusement.

For a better overview of how feature deploy server plays with the featuredeploy CLI you can [open this Diagram](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1#R1VlLc5swEP41HJPhYWNyjB9JM5NOM%2FGh7VGGNajFyBXCj%2Fz6SrAYZIJrNziJc0ik1Wol7X77aVEMZ7TY3HOyjL6yAGLDNoON4YwN27bsfl%2F%2BUZJtIXG9m0IQchqgUiWY0hdAoYnSjAaQaoqCsVjQpS70WZKALzQZ4ZytdbU5i%2FVVlySEhmDqk7gp%2FU4DERVSr29W8i9Aw6hc2TJxZEb83yFnWYLrGbYzz3%2BK4QUpbaF%2BGpGArWsiZ2I4I86YKFqLzQhi5dvSbcW8u5bR3b45JOKoCS7uQ2zLs0MgXYFdxkXEQpaQeFJJh%2Fn5QFkwZS8Si1g2Ldn8BUJsMZokE0yKKguPjC1Rr7lL3HjKMu7jPnoYd8JDQC1EldphbRqe7B7YAgTfSgUOMRF0pQeTICbCnR5OveWcbGsKS0YTkdYsPymBVEB4OyVKEdz2YM%2FHp%2BnLRrGDslc7SiXK49YSQ8ytFYkzPPJkBeoIzq1hu7F03jCgK9kMVTMmszxbSaBiiONyjZrKgVkcFmzVPm8PSwI2QocIh5S%2BkFmuoNCDzpba%2FaHRH0sJiWmYSEEMczV3BVxQmZm3KF7QIMhRmO9ouMu3EYsZz1ctM%2B5VnCHelVXYaPhALsG9afmogQtnmdfuje1oge0hZE%2BDXwMvV6UdNHtl3%2Bgm2HyeypTQMXQqanoN0NxTEWWzRgyrbFfxW0dUwHRJ8ixdS%2FbXw9ua2Q2HtzrWNvV0sTzsrysmtkr%2BjGos7JrtntYcdSiXvC75EDZU%2FFDia8tzsP8T1Y7lSjXnCTiVRwGOc4%2Fiz%2FOQZQOtu6usZLfeXhgKAsdZVSROZd39dZxetyxamq8lxK0vKEteZ9FsGRAB6n6K1O%2Bn54tlRK87RjRv9MzthA6tPTLcg1cnZNhvxH7KFjMOnH06OtxVE%2B9Ch1bj%2FJ3QYb9Ghp0XjgOjUTh6XXPh0Q60W1ilpTgbcchppRiY8QMV2XNeiR0u4C6OjNrS43%2FIyLP6byOgknKcMzCO03bdtAAjgGXMtkeU67X4un8y9R05VGG%2BwrhJ22Yeut1oaYUfxNN7sICEAd%2FWhlT31HLplNKozhCDj2KIQQMHd5ICMg56xOsc8fhwZJQ%2B%2Bq7que95VznnQKlVw2gBy06R6DWR%2BEkeOVw9lK7zj0cO97zludX8Xj30yDHhnPGjHzemme9Dmh6tP4ZUcLa94GcQp6t79sq8tvefK9526250M%2BVnpX2GS9hrYGpMQyqI0vnmA0leif1DkgqSSLhcCAe75vk4WHarp%2BrC%2F9X%2FA5zJXw%3D%3D)

### Misc notes
Featuredeploy is used regularly at [resmio](https://resmio.com/) and designed as a general purpose application, nevertheless the [The Rule of Three](https://blog.codinghorror.com/rule-of-three/) applies.
Meaning that it fits very well the needs of the company it was designed for but may need adaptations to work for you. Also note that the code did not get more dedication than it needs to fulfill its purpose. Also note furthermore that of course the digital ocean account associated with the digital ocean token from the configuration file will be billed. There is no rate limiting of deployment invocations by adding the github label or calling the featuredeploy CLI directly.
