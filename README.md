# NITA CLI

NITA CLI project adds a command line interface to NITA. It is the way of interacting with NITA by using simple and very intuitive commands. It abstracts the user from the complexity of most of the commands running behind the scenes (related to docker, unix and some other tools).

## TOC

- [NITA CLI](#nita-cli)
  - [Goal](#goal)
  - [Reusability](#reusability)
  - [Prerequisites](#prerequisites)
  - [About NITA CLI](#about-nita-cli)
    - [cli.py](#clipy)
    - [nita](#nita)
  - [Installation](#installation)
  - [Customisation](#customisation)
  - [Troubleshooting](#troubleshooting)
  - [Demo](#demo)
  - [Contacts](#contacts)

## Goal

NITA CLI resolves the complexity of dealing with a lot of different technologies within the same framework by simplifying any command with its arguments, options, etc... into a single, customisable, intuitive and easy to remember command of your choice.

Imagine trying to type the following command to get jenkins container IPs:

    $ docker inspect --format='{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}' jenkins

    172.19.0.3   172.18.0.7

Is not easier and more intuitive to run the following command to get the same output? See below:

    $ nita jenkins ip

    172.19.0.3   172.18.0.7

Or this one to list all NITA containers:

    $ docker ps --filter "label=net.juniper.framework=NITA"

Compare it with this one in order to get the same output:

    $ nita containers

    command:  docker ps --filter "label=net.juniper.framework=NITA"

    CONTAINER ID        IMAGE                                     COMMAND             CREATED             STATUS              PORTS                     NAMES
    8a36d29b6b1f        registry.juniper.net/nita/jenkins:latest   "/bin/tini -- /usr..."   5 hours ago         Up 5 hours (healthy)   0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp   jenkins
    9f04684e6f82        registry.juniper.net/nita/tacacs:latest    "tacacs-runner"          5 hours ago         Up 5 hours             0.0.0.0:10049->49/tcp                              tacacs
    6a11f837b797        registry.juniper.net/nita/dns:latest       "dns-runner"             5 hours ago         Up 5 hours             0.0.0.0:53->53/udp                                 dns
    93b54c5d7a8f        registry.juniper.net/nita/radius:latest    "radius-runner"          5 hours ago         Up 5 hours             0.0.0.0:11812->1812/udp                            radius
    d224c2bdf0f5        registry.juniper.net/nita/webapp:latest    "webapp-runner"          5 hours ago         Up 5 hours             0.0.0.0:8090->8060/tcp                             webapp
    90c5c7afcace        registry.juniper.net/nita/ntp:latest       "ntp-runner"             5 hours ago         Up 5 hours             0.0.0.0:123->123/tcp                               ntp

## Reusability

These scripts are basically a wrapper to almost any command a consultant could imagine. Not only that, it is also designed in a way that if any new commands are needed is so easy to add them that anybody will be able to play with it and get it customised.

Furthermore, the way it is designed allows a user to reuse it in a different platforms. Let's say J-EDI for example. The only modification needed is to rename the `nita` script to `j-edi` and create a new tree of commands in `cli.py` file. After that, add `+x` permissions and move them to /usr/local/bin/ directory. That's all folks!!! Ready to go!!!

## Prerequisites

`jq` is a lightweight and flexible command-line JSON processor.

It is not really a prerequisite since NITA CLI runs without `jq`, but it really improves readability when using it! Here is the evidence:

It is not the same this:

    $ docker inspect --format '{{json .Mounts}}' webapp
    [{"Type":"bind","Source":"/Users/jizquierdo/Documents/Juniper/Projects/NITA/webapp_and_jenkins_shared","Destination":"/project","Mode":"rw","RW":true,"Propagation":"rprivate"}]

than this:

    $ docker inspect --format '{{json .Mounts}}' webapp | jq
    [
    {
    "Type": "bind",
    "Source": "/Users/jizquierdo/Documents/Juniper/Projects/NITA/webapp_and_jenkins_shared",
    "Destination": "/project",
    "Mode": "rw",
    "RW": true,
    "Propagation": "rprivate"
    }
    ]

It can be installed from [github](https://stedolan.github.io/jq/) or running `brew install jq` on OS X.

## About NITA CLI

It is composed of two different python scripts:

### `cli.py`

It is the smart part of the cli. It is the library that converts the dictionary structures (defined below) into executable commands. This is a generic library that can be used to produce cli program to execute any terminal command.

### `nita`

This python script contains the cli commands, what those commands execute and the documentation for the commands. There are two dictionary trees that contain all this data. For it to run it imports the *cli* library and then calls `cli.main()` to do the work.

The *COMMANDS* tree is a python dictorionary and represents the hierarchycal command structure.

The *HELP* tree deals with the explanation of what each NITA CLI command does. Do not forget to populate this tree as well to keep your help/usage aligned with your script. Moreover the script will error complaining the *COMMANDS* and *HELP* structures are not in sync! An undocumented command is no command at all...

See both files on the repo for a deeper understanding:

- [nita](/nita)

- [cli.py](/cli.py)

There is a `help` implemented on the script which basically shows the commands already mapped. Here it is the `nita help` command output:

NITA CLI command | Description
-----------------|-------------------
   nita stats | Displays NITA containers runtime metrics [CPU %, MEM USAGE / LIMIT, MEM %, NET I/O, BLOCK I/O, PIDS].
   nita license | Displays the NITA License.
   nita tacacs ip | Returns IPs information on tacacs container.
   nita tacacs cli | Attaches local standard input, output, and error streams to tacacs running container.
   nita tacacs logs | Fetches the logs of tacacs container.
   nita tacacs volumes | Returns shared volumes information on tacacs container.
   nita tacacs ports | Returns mapped ports information on tacacs container.
   nita ntp ip | Returns IPs information on ntp container.
   nita ntp cli | Attaches local standard input, output, and error streams to ntp running container.
   nita ntp logs | Fetches the logs of ntp container.
   nita ntp volumes | Returns shared volumes information on ntp container.
   nita ntp ports | Returns mapped ports information on ntp container.
   nita up | Creates and starts NITA containers and networks.
   nita robot ip | Returns IPs information on robot container.
   nita robot run test | Runs Test process (./test.sh script) on /project located at $PROJECT_PATH.
   nita robot ports | Returns mapped ports information on robot container.
   nita robot volumes | Returns shared volumes information on robot container.
   nita robot cli | Attaches local standard input, output, and error streams to robot running container.
   nita down | Stops and removes NITA containers and networks.
   nita ips | Shows all NITA containers IPs
   nita ansible ip | Returns IPs information on ansible container.
   nita ansible run build | Runs Build process (./build.sh script) on /project located at $PROJECT_PATH.
   nita ansible run noob | Runs NOOB process (./noob.sh script) on /project located at $PROJECT_PATH.
   nita ansible ports | Returns mapped ports information on ansible container.
   nita ansible volumes | Returns shared volumes information on ansible container.
   nita ansible cli | Attaches local standard input, output, and error streams to ansible running container.
   nita radius ip | Returns IPs information on radius container.
   nita radius cli | Attaches local standard input, output, and error streams to radius running container.
   nita radius logs | Fetches the logs of radius container.
   nita radius volumes | Returns shared volumes information on radius container.
   nita radius ports | Returns mapped ports information on radius container.
   nita dns ip | Returns IPs information on dns container.
   nita dns cli | Attaches local standard input, output, and error streams to dns running container.
   nita dns logs | Fetches the logs of dns container.
   nita dns volumes | Returns shared volumes information on dns container.
   nita dns ports | Returns mapped ports information on dns container.
   nita jenkins jobs ls | Lists all Jenkins jobs.
   nita jenkins jobs remove --regex REGEX | Removes Jenkins jobs containing REGEX. Assume "yes" as answer to all prompts and run non-interactively.
   nita jenkins logs | Fetches the logs of jenkins container.
   nita jenkins ip | Returns IPs information on jenkins container.
   nita jenkins volumes | Returns shared volumes information on jenkins container.
   nita jenkins ports | Returns mapped ports information on jenkins container.
   nita jenkins cli jenkins | Attaches local standard input, output, and error streams to jenkins running container with "jenkins" user.
   nita jenkins cli root | Attaches local standard input, output, and error streams to jenkins running container with "root" user.
   nita images ls | Lists all NITA images.
   nita images versions | Displays NITA images versions
   nita new project | Creates a new NITA project scaffolding.
   nita new role | Creates a new Ansible role scaffolding.
   nita webapp ip | Returns IPs information on webapp container.
   nita webapp cli | Attaches local standard input, output, and error streams to webapp running container.
   nita webapp logs | Fetches the logs of webapp container.
   nita webapp volumes | Returns shared volumes information on webapp container.
   nita webapp ports | Returns mapped ports information on webapp container.
   nita containers ls | Lists all running NITA containers.
   nita containers versions | Lists all running NITA containers versions.
 |

## Installation

In order to install NITA CLI, clone this project and execute `install.sh` script with sudo.

    $ sudo sh install.sh
    Password:

     >>>> Copying cli.py & nita to /usr/local/bin/

     >>>> Adding +x permissions to /usr/local/bin/nita

     >>>> NITA CLI has been installed successfully!

    $

## Customisation

See below example to understand how it works and how to customise it to fit your needs. 

Imagine this is your COMMANDS tree. This is a `hello world` example:

    COMMANDS = {
        'nita': {
            'hello': {
                'world': 'docker run hello-world'
            }
        }
    }

    HELP = {
        'nita': {
            'hello': {
                'world': 'runs a NITA hello-world example'
            }
        }
    }

Should you [install](#installation) the NITA CLI project and run it as below (you will be able to run it from wherever you want!) you will get the following output:

    $ nita hello world

    command:  docker run hello-world


    Hello from Docker!
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
        (amd64)
    3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.

    To try something more ambitious, you can run an Ubuntu container with:
    $ docker run -it ubuntu bash

    Share images, automate workflows, and more with a free Docker ID:
    https://cloud.docker.com/

    For more examples and ideas, visit:
    https://docs.docker.com/engine/userguide/

Such output is the output of the execution of a `docker run hello-world`. If you want to customise your `COMMANDS tree` then you just need to map in the python dictionary the arguments `nita ${ARG_1} ${ARG_2}` of your script as the path in the tree.

    COMMANDS = {
        'nita': {
            '${ARG_1}': {
                '${ARG_2}': '${COMMAND}'
            }
        }
    }

    HELP = {
        'nita': {
            '${ARG_1}': {
                '${ARG_2}': '${DESCRIPTION}'
            }
        }
    }

The leaf will be the value of your mapped command (e.g. `${COMMAND}`). As shown in previous example, this is the mapping taking place:

    nita hello world  >>>>  docker run hello-world

But you can grow your tree and make it as complicated as you want. Should you do that, bear in mind that some intelligence may need to be added to `nita` script, but dont let that stop you!

Here it is another example of how to grow it:

    COMMANDS = {
        'nita': {
            'hello': {
                'world': 'docker run hello-world'
            },
            'example': {
                'command': 'docker run alpine:latest cat /etc/alpine-release'
            }
        }
    }

    HELP = {
        'nita': {
            'hello': {
                'world': 'runs a NITA hello-world example'
            },
            'example': {
                'command': 'shows Linux Alpine release in an Alpine docker container'
            }
        }
    }

    $ docker run alpine:latest cat /etc/alpine-release
    3.6.2

    $ nita example command

    command:  docker run alpine:latest cat /etc/alpine-release

    3.6.2

Enjoy creating your own docker-like or VMM-like CLI interface!!!

## Troubleshooting

### Wrong command

If a wrong command is executed (i.e. there is a wrong key on the COMMANDS dictionary), NITA CLI will show you the following message:

    $ nita hello world

    'hello' key does not exist! Command: 'nita hello world' is incorrect!

     For a list of available commands, execute:

    >>>>  nita help

Please, review `nita help` output and look for the command you are looking for. If it is not there and you consider it should... submit a merge request to add it! You can always add it to your local copy if not a general purpose command!

### Missing description or mapped command

`cli.py` library has a function that checks if the nested keys of both dictionaries from `nita` (or any other file that imports the library) are the same. That is a reminder to add not only the command but also a help/usage message that will help other users take advantage of it. If keys are not the same, it will show a message explaining which commands are wrong like the one below:

    $ nita robot run test

    The following command: "nita robot run test" is missing its description!

    >>> Please add it to the HELP tree!


    The following command: "nita robot volumes" is missing its mapped command!
    The following command: "nita robot ip" is missing its mapped command!

    >>> Please add it to the COMMANDS tree!

As the output says, check the dictionaries for the keys shown and add the missing part (description or mapped command) as told by the script output.


## Demo

NITA CLI (Command Line interface) is the way of interacting with NITA by using simple and very intuitive commands. It abstracts the user from the complexity of most of the commands running behind the scenes (related to docker, unix and some other tools). 

During the demo both the NITA CLI command and its unix/docker/etc mapped command will be shown to prove the simplicity and intuition of NITA CLI.

Here they are some commands as an example:

To check docker images vs. nita images:

    docker images vs. nita images ls

To check the versions of NITA images:

    nita images versions

To check docker running containers vs. nita running containers:

    docker ps  vs. nita containers ls

To check the versions of NITA running containers:

    nita containers versions

To check docker containers statistics vs. nita containers statistics:

    docker stats  vs. nita stats

Imagine you need to know all your NITA framework IPs... See the different from these 2 commands:

    nita ips

Which port did you map your NTP port?

    nita ntp ports

Also, to check which volumes is sharing the Jenkins container:

    nita jenkins volumes

In order to check the webapp container logs

    nita webapp logs

Should you want to debug TACACS on the server side

    nita tacacs logs

Imagine login in radius container

    nita radius cli    ->  ps -fea    ->   kill PID   ->  freeradius -X

Or even run NOOB, Build and Test without needed to do it from the UI (You will save a LOT of time)

    nita ansible run noob

You are requested to create a NEW PROJECT???

    nita new project new_nita_project-12345-alt
    tree new_nita_project-12345-alt

A NEW ROLE in the project???

    cd into project and roles/ dir
    nita new role srx_cluster
    tree srx_cluster

What if I misspell a command???

    $ nita ansible abc

    'abc' key does not exist! Command: 'nita ansible abc' is incorrect!

    For a list of available commands, execute: 

    >>>>  nita help


In a nutshell, anything you want to know about what NITA CLI does, just issue the help:

    nita help

and you will get all the things that NITA CLI can do for you!!!!

_Benefits_: It is completely reusable among other products. Not tight to NITA. So it is an easy way to map complex commands to simple and intuitive ones related to your framework!

## Contacts

`Juniper Internal only`

We would like to lead you and your customers into the Network Automation world!

Get in touch with us! How?

- Write an e-mail to:

Contact Name | e-mail
---------|----------
Jose Miguel Izquierdo | jizquierdo@juniper.net
David Gethings | dgethings@juniper.net
 |

- Request access to our [Slack](https://slack.com) [NITA-dev](https://nita-dev.slack.com) workspace.

You will be sent an invitation to join us.

Share anything with us (request, issues, concerns, suggestions, etc...) on any of the different channels depending on the topic:

Channel | Description
---------|----------
\#general      | NITA Company-wide announcements and work-based matters
\#nita-dev     | NITA development channel
\#nita-support | NITA support channel
 |

Thanks for using NITA!
