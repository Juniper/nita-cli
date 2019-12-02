# NITA CLI
<!-- 
[![build status](https://git.juniper.net/NITA/nita-cli/badges/master/build.svg)](https://git.juniper.net/NITA/nita-cli/commits/master) -->

NITA CLI project adds a command line interface to NITA. It is the way of interacting with NITA by using simple and intuitive commands. It focusses the user on getting a task done without having to learn the complex commands that run behind the scenes (related to docker, unix and some other tools). It is a move towards user-friendly, intuitive NetDevOps.

Juniper Networks focus is on `Engineering. Simplicity`. The NITA CLI is an example of this. It is creativity with an eye toward pragmatism. It is not just innovation, but innovation applied.

## TOC

- [NITA CLI](#nita-cli)
    - [TOC](#toc)
    - [Goal](#goal)
    - [Reusability](#reusability)
    - [Autocompletion](#autocompletion)
    - [Usage](#usage)
    - [Suggestion](#suggestion)
    - [Prerequisites](#prerequisites)
        - [Basic](#basic)
        - [Autocomplete](#autocomplete)
    - [Installation](#installation)
    - [About NITA CLI](#about-nita-cli)
        - [`cli.py`](#clipy)
        - [`nita`](#nita)
        - [Documentation](#documentation)
    - [Customisation](#customisation)
    - [Continuos integration (CI)](#continuos-integration-ci)
    - [Troubleshooting](#troubleshooting)
    - [Demo](#demo)
    - [Contact](#contact)

## Goal

NITA CLI resolves the complexity of dealing with a lot of different technologies within the same framework by simplifying any command with its arguments, options, etc... into a single, customisable, intuitive and easy to remember command of your choice.

It is designed to help on:

- Support
- Operations/Engineering
- Development

so a lot of its commands come from the tasks carried out routinely on the following topics.

Imagine trying to type the following command to get jenkins container IPs:

    $ docker inspect --format='{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}' jenkins

    172.19.0.3   172.18.0.7

Is not easier and more intuitive to run the following command to get the same output? See below:

    $ nita jenkins ip

    172.19.0.3   172.18.0.7

Or this one to list all NITA containers:

    $ docker ps --filter "label=net.juniper.framework=NITA"

Compare it with this one in order to get the same output:

    $ nita containers ls
    CONTAINER ID        IMAGE                                      COMMAND                  CREATED             STATUS                       PORTS                                              NAMES
    5894c9c50d46        registry.juniper.net/nita/jenkins:latest   "/sbin/tini -- /usr/…"   About an hour ago   Up About an hour (healthy)   0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp   jenkins
    5ed87b63500f        registry.juniper.net/nita/webapp:latest    "webapp-runner"          About an hour ago   Up About an hour             0.0.0.0:8090->8060/tcp                             webapp
    714107fad380        registry.juniper.net/nita/rsyslog:latest   "rsyslog-runner"         About an hour ago   Up About an hour             0.0.0.0:514->514/udp                               rsyslog
    effe8a4a7217        registry.juniper.net/nita/ntp:latest       "ntp-runner"             About an hour ago   Up About an hour             0.0.0.0:123->123/tcp                               ntp
    00e83ef33c4f        registry.juniper.net/nita/radius:latest    "radius-runner"          About an hour ago   Up About an hour             0.0.0.0:11812->1812/udp                            radius
    79ce0367ac8a        registry.juniper.net/nita/tacacs:latest    "tacacs-runner"          About an hour ago   Up About an hour             0.0.0.0:10049->49/tcp                              tacacs
    94c5e76fe470        registry.juniper.net/nita/dns:latest       "dns-runner"             About an hour ago   Up About an hour             0.0.0.0:53->53/udp                                 dns

## Reusability

These scripts are basically a wrapper to almost any command a consultant could imagine. Not only that, it is also designed in a way that if any new commands are needed, it is so _easy_ to add them that anybody will be able to play with it and get it customised.

Furthermore, the way it is designed allows a user to reuse it in a different platforms. Let's say J-EDI for example. The only modification needed is to rename the `nita` script to `j-edi` and create a new tree of commands in `cli.py` file. After that, add `+x` permissions and move them to /usr/local/bin/ directory. That's all folks!!! Ready to go!!!

## Autocompletion

Another cool feature it has is `autocompletion`. So far, it has been tested in the following Operating Systems:

 - `Linux` (Ubuntu 16 LTS and Ubutu 18 LTS) 
 - `OS X` (Sierra, High Sierra and Mojave)
 - `Windows 10` (with [Cygwin](https://www.cygwin.com/)).

It makes use of the following links:

- https://debian-administration.org/article/316/An_introduction_to_bash_completion_part_1
- https://debian-administration.org/article/317/An_introduction_to_bash_completion_part_2

## Usage

### Help
NITA CLI comes with a bunch of pre-installed commands and a description of help features. Just by typing the root of your CLI command (e.g. `nita`) and ask for help, (e.g. `?`, `-h` or `--help`) it will list you all with a brief description of what each of them does.

NITA CLI help is context sensitive. So it matters where you use the help. You can get a list of all available commands at certain level of the commands tree, which would be a different set than from other part of the command tree. See below:

    $ nita jenkins ?

    nita jenkins cli jenkins => Attaches local standard input, output, and error streams to jenkins running container with "jenkins" user.
    nita jenkins cli root => Attaches local standard input, output, and error streams to jenkins running container with "root" user.
    nita jenkins ip => Returns IPs information on jenkins container.
    nita jenkins jobs export => Exports an existing job matched by --job <JOB> into XML format from Jenkins server.
    nita jenkins jobs import => Imports a job from XML config file by --file <FILE> (e.g. file.xml) into Jenkins server.
    nita jenkins jobs ls => Lists all Jenkins jobs.
    nita jenkins jobs remove => Removes Jenkins jobs matched by --regex <REGEX>. Assume "yes" as answer to all prompts and run non-interactively.
    nita jenkins labels => Returns labels information on jenkins container.
    nita jenkins logs => Fetches the logs of jenkins container.
    nita jenkins ports => Returns mapped ports information on jenkins container.
    nita jenkins volumes => Returns shared volumes information on jenkins container.

    $ nita rsyslog ?

    nita rsyslog cli => Attaches local standard input, output, and error streams to rsyslog running container.
    nita rsyslog ip => Returns IPs information on rsyslog container.
    nita rsyslog labels => Returns labels information on rsyslog container.
    nita rsyslog logs => Fetches the logs of rsyslog container.
    nita rsyslog ports => Returns mapped ports information on rsyslog container.
    nita rsyslog volumes => Returns shared volumes information on rsyslog container.

### Autocompletion

NITA CLI autocompletion is also context sensitive. Just by pressing `TAB` key twice at any level of the command tree, it will show you the different options you might have to autocomplete your command. For example:

    $ nita (TAB TAB)
    ansible     containers  demo        up      down ....
    ...

    $ nita tacacs (TAB TAB)
    cli      ip       labels   logs     ports    volumes

You should not worry about how it has been implemented, but as it is something integrated/reusable into any forked/branched repository, here it is a brief explanation.

When running script `./autocomplete` (as a stand alone script or as part of ./install.sh script) it renders a template `templates/*.j2` with the values obtained from the CLI COMMANDS dictionary. They are dump into a temporary file `tmp/vars.yml` and generates a bash script into `bash_completion.d/` folder.

This autocompletion script is then copied by `install.sh` script into the `/etc/bash_completion.d/` folder on the host server.

In order to __load autocompletion__ it is needed to type following commmands into your shell (It is automatically done by the script, but if you want to test it in your terminal without the need to restart it (so changes take effect right after command execution!)):

- Linux

        $ . /etc/bash_completion.d/nita

- OS X

        $ . $(brew --prefix)/etc/bash_completion.d/nita

- Windows (Cygwin)

        . /etc/bash_completion.d/nita

How do you know it works? If you type complete command grepping by your script, it should appear as below.

    $ complete -p | grep nita
    complete -F _nita nita

Also, type `nita` and then `TAB` twice and it should give you some options to autocomplete. See below:

    $ nita (TAB TAB)
    ansible     containers  demo        up      down ....
    ...

## Suggestion

Name every nested key in the CLI so they are not repeated. If repeated, autocompletion might suggest a completion with does not correspond to that command. It is not a big deal, but a known issue! See example below:

    $ nita cli
    jenkins  root     version

    $ nita cli ?

    nita cli version => Shows NITA CLI current version.

    $ nita jenkins cli ?
    
    nita jenkins cli jenkins => Attaches local stdin/stdout/stderr to jenkins running container with "jenkins" user.
    nita jenkins cli root => Attaches local stdin/stdout/stderr to jenkins running container with "root" user.


## Prerequisites

### Basic
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

It can be installed from:
- [github](https://stedolan.github.io/jq/)
- running `brew install jq` on OS X.
- running `apt-get install jq` on Linux.

### Autocomplete
Following packages are needed to make use of autocompletion:

- python3
- python3-pip
- pyYAML (pip3 package)
- Jinja2 (pip3 package)
- brew _or_ cygwin (if OS X or Windows machines)

If in `OS X`:

Install [brew](https://brew.sh/) to be able to install `bash-completion` package:

    brew install bash-completion

and before you run your first NITA CLI command, add the following tidbit to your `~/.bash_profile`: 

    if [ -f $(brew --prefix)/etc/bash_completion ]; then
    . $(brew --prefix)/etc/bash_completion
    fi

If in `Windows` ([Cygwin](https://www.cygwin.com/)), install `bash-autocomplete` package as well. Edit your `~/.bashrc` file to turn on autocompletion as below:

    # Uncomment to turn on programmable completion enhancements.
    # Any completions you add in ~/.bash_completion are sourced last.
    [[ -f /etc/bash_completion ]] && . /etc/bash_completion

## Installation

In order to install NITA CLI, use pip command and specifiy nita_cli repository with `sudo` (if needed).

`pip3 install -i https://artifactory.aslab.juniper.net/artifactory/api/pypi/ps-pypi/simple --no-binary :all: nita-cli`

    $ pip3 install -i https://artifactory.aslab.juniper.net/artifactory/api/pypi/ps-pypi/simple --no-binary :all: nita-cli

    Collecting nita-cli
    Downloading https://artifactory.aslab.juniper.net/artifactory/api/pypi/ps-pypi/packages/nita_cli/0.0.4/nita_cli-0.0.4.tar.gz
    Requirement already satisfied (use --upgrade to upgrade): pyyaml in /usr/local/lib/python3.5/dist-packages (from nita-cli)
    Requirement already satisfied (use --upgrade to upgrade): jinja2 in /usr/local/lib/python3.5/dist-packages (from nita-cli)
    Requirement already satisfied (use --upgrade to upgrade): MarkupSafe>=0.23 in /usr/local/lib/python3.5/dist-packages (from jinja2->nita-cli)
    Skipping bdist_wheel for nita-cli, due to binaries being disabled for it.
    Installing collected packages: nita-cli
      Running setup.py install for nita-cli ... done
    Successfully installed nita-cli-0.0.4

If you are a **developer** and want to test your changes on NITA CLI local, then you can clone the project and then install it with your own changes by running the following command (add -I or --ignore-installed):

`sudo pip3 install -I nita-cli/ --no-binary :all:`

    $ sudo pip3 install -I nita-cli/ --no-binary :all:
    
    Processing ./nita-cli
    Collecting pyyaml (from nita-cli==0.0.4)
    Collecting jinja2 (from nita-cli==0.0.4)
      Downloading https://files.pythonhosted.org/packages/7f/ff/ae64bacdfc95f27a016a7bed8e8686763ba4d277a78ca76f32659220a731/Jinja2-2.10-py2.py3-none-any.whl (126kB)
        100% |████████████████████████████████| 133kB 424kB/s 
    Collecting MarkupSafe>=0.23 (from jinja2->nita-cli==0.0.4)
    Installing collected packages: pyyaml, MarkupSafe, jinja2, nita-cli
      Running setup.py install for nita-cli ... done
    Successfully installed MarkupSafe-1.0 jinja2-2.10 nita-cli-0.0.4 pyyaml-3.13

## About NITA CLI

It is mainly composed of two different python scripts. There are others (like installation and autocomplete, but they are not really part of the heart of the CLI):

### `cli.py`

It is the smart part of the cli. It is the library that converts the dictionary structures (defined below) into executable commands. This is a generic library that can be used to produce cli program to execute any terminal command.

### `nita`

This python script contains the cli commands, what those commands execute and the documentation for the commands. There are two dictionary trees that contain all this data. For it to run it imports the *cli* library and then calls `cli.main()` to do the work.

The *COMMANDS* tree is a python dictorionary and represents the hierarchycal command structure.

The *HELP* tree deals with the explanation of what each NITA CLI command does. Do not forget to populate this tree as well to keep your help/usage aligned with your script. Moreover the script will error complaining the *COMMANDS* and *HELP* structures are not in sync! An undocumented command is no command at all...

See both files on the repo for a deeper understanding:

- [nita](/nita)

- [cli.py](/cli.py)

There is a `help` implemented at each level of the script which basically shows the commands mapped and what they do. Here it is the `nita help` command output (top level):

### Documentation

NITA CLI command | Description
-----------------|-------------------
   nita ansible cli |  Attaches local standard input, output, and error streams to ansible running container.
   nita ansible labels |  Returns labels information on ansible container.
   nita ansible run build console |  Runs BUILD process and writes its output to console. -- It does not trigger any Jenkins job! --
   nita ansible run build gui |  Triggers BUILD Jenkins job.
   nita ansible run noob console |  Runs NOOB process and writes its output to console. -- It does not trigger any Jenkins job! --
   nita ansible run noob gui |  Triggers NOOB Jenkins job.
   nita ansible volumes |  Returns shared volumes information on ansible container.
   nita cli version |  Shows NITA CLI current version.
   nita containers ls |  Lists all running NITA containers.
   nita containers versions |  Lists all running NITA containers versions.
   nita demo laptop |  Runs the whole NITA demo with a single script on a laptop environment. It needs to be run from nita-demo-intro/ folder.
   nita demo vmm |  Runs the whole NITA demo with a single script on VMM environment. It needs to be run from nita-demo-intro/ folder.
   nita destroy environment |  Gives the user the option to destroy either your virtual DC running on your laptop or VMM environment to run the demo.
   nita dns cli |  Attaches local standard input, output, and error streams to dns running container.
   nita dns ip |  Returns IPs information on dns container.
   nita dns labels |  Returns labels information on dns container.
   nita dns logs |  Fetches the logs of dns container.
   nita dns ports |  Returns mapped ports information on dns container.
   nita dns restart |  Restarts dns container.
   nita dns start |  Starts dns container.
   nita dns stop |  Stops dns container.
   nita dns up |  Creates and starts dns container.
   nita dns volumes |  Returns shared volumes information on dns container.
   nita down |  Stops and removes NITA containers (both Core and CaaS).
   nita images ls |  Lists all NITA images.
   nita images versions |  Displays NITA images versions.
   nita inventory create |  Creates a new 3rd-party virtual DC dynamic inventory in a couchDB container.
   nita inventory populate |  Populates virtual DC dynamic inventory with data related to NITA demo.
   nita ips |  Shows all NITA containers IPs.
   nita jenkins cli jenkins |  Attaches local standard input, output, and error streams to jenkins running container with "jenkins" user.
   nita jenkins cli root |  Attaches local standard input, output, and error streams to jenkins running container with "root" user.
   nita jenkins ip |  Returns IPs information on jenkins container.
   nita jenkins jobs export |  Exports an existing job matched by --job <JOB> into XML format from Jenkins server.
   nita jenkins jobs import |  Imports a job from XML config file by --file <FILE> (e.g. file.xml) into Jenkins server.
   nita jenkins jobs ls |  Lists all Jenkins jobs.
   nita jenkins jobs remove |  Removes Jenkins jobs matched by --regex <REGEX>. Assume "yes" as answer to all prompts and run non-interactively.
   nita jenkins labels |  Returns labels information on jenkins container.
   nita jenkins logs |  Fetches the logs of jenkins container.
   nita jenkins ports |  Returns mapped ports information on jenkins container.
   nita jenkins restart |  Restarts jenkins container.
   nita jenkins start |  Starts jenkins container.
   nita jenkins stop |  Stops jenkins container.
   nita jenkins up |  Creates and starts jenkins container.
   nita jenkins volumes |  Returns shared volumes information on jenkins container.
   nita license |  Displays the NITA License.
   nita new project |  Creates a new NITA project scaffolding.
   nita new role |  Creates a new Ansible role scaffolding.
   nita ntp cli |  Attaches local standard input, output, and error streams to ntp running container.
   nita ntp ip |  Returns IPs information on ntp container.
   nita ntp labels |  Returns labels information on ntp container.
   nita ntp logs |  Fetches the logs of ntp container.
   nita ntp ports |  Returns mapped ports information on ntp container.
   nita ntp restart |  Restarts ntp container.
   nita ntp start |  Starts ntp container.
   nita ntp stop |  Stops ntp container.
   nita ntp up |  Creates and starts ntp container.
   nita ntp volumes |  Returns shared volumes information on ntp container.
   nita radius cli |  Attaches local standard input, output, and error streams to radius running container.
   nita radius ip |  Returns IPs information on radius container.
   nita radius labels |  Returns labels information on radius container.
   nita radius logs |  Fetches the logs of radius container.
   nita radius ports |  Returns mapped ports information on radius container.
   nita radius restart |  Restarts radius container.
   nita radius start |  Starts radius container.
   nita radius stop |  Stops radius container.
   nita radius up |  Creates and starts radius container.
   nita radius volumes |  Returns shared volumes information on radius container.
   nita rsyslog cli |  Attaches local standard input, output, and error streams to rsyslog running container.
   nita rsyslog ip |  Returns IPs information on rsyslog container.
   nita rsyslog labels |  Returns labels information on rsyslog container.
   nita rsyslog logs |  Fetches the logs of rsyslog container.
   nita rsyslog ports |  Returns mapped ports information on rsyslog container.
   nita rsyslog restart |  Restarts rsyslog container.
   nita rsyslog start |  Starts rsyslog container.
   nita rsyslog stop |  Stops rsyslog container.
   nita rsyslog up |  Creates and starts rsyslog container.
   nita rsyslog volumes |  Returns shared volumes information on rsyslog container.
   nita setup all |  Execute all demo
   nita setup environment |  Gives the user the option to set up either your virtual DC running on your laptop or VMM environment to run the demo.
   nita start |  Starts NITA containers (both Core and CaaS).
   nita stats |  Displays NITA containers runtime metrics [CPU %, MEM USAGE / LIMIT, MEM %, NET I/O, BLOCK I/O, PIDS].
   nita status |  Shows the status of every NITA containers.
   nita stop |  Stops NITA containers (both Core and CaaS).
   nita tacacs cli |  Attaches local standard input, output, and error streams to tacacs running container.
   nita tacacs ip |  Returns IPs information on tacacs container.
   nita tacacs labels |  Returns labels information on tacacs container.
   nita tacacs logs |  Fetches the logs of tacacs container.
   nita tacacs ports |  Returns mapped ports information on tacacs container.
   nita tacacs restart |  Restarts tacacs container.
   nita tacacs start |  Starts tacacs container.
   nita tacacs stop |  Stops tacacs container.
   nita tacacs up |  Creates and starts tacacs container.
   nita tacacs volumes |  Returns shared volumes information on tacacs container.
   nita test cli |  Attaches local standard input, output, and error streams to test running container.
   nita test labels |  Returns labels information on test container.
   nita test pull dynamic |  Creates topology object from dynamic inventory.
   nita test pull static |  Creates topology object from static inventory.
   nita test run common firewall console |  Executes common test suite on firewall and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run common firewall gui |  Triggers vDC_FW_Common_Tests Jenkins job.
   nita test run common router console |  Executes common test suite on router and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run common router gui |  Triggers vDC_RX_Common_Tests Jenkins job.
   nita test run common switch console |  Executes common test suite on switch and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run common switch gui |  Triggers vDC_SW_Common_Tests Jenkins job.
   nita test run specific dns console |  Executes specific DNS tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific dns gui |  Triggers vDC_DNS_Tests Jenkins job.
   nita test run specific firewall console |  Executes specific firewall tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific firewall gui |  Triggers vDC_FW_Tests Jenkins job.
   nita test run specific ntp console |  Executes specific NTP tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific ntp gui |  Triggers vDC_NTP_Tests Jenkins job.
   nita test run specific radius console |  Executes specific RADIUS tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific radius gui |  Triggers vDC_RADIUS_Tests Jenkins job.
   nita test run specific router console |  Executes specific router tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific router gui |  Triggers vDC_RX_Tests Jenkins job.
   nita test run specific switch console |  Executes specific switch tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific switch gui |  Triggers vDC_SW_Tests Jenkins job.
   nita test run specific syslog console |  Executes specific SYSLOG tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific syslog gui |  Triggers vDC_SYSLOG_Tests Jenkins job.
   nita test run specific tacacs console |  Executes specific TACACS tests and writes its output to console. -- It does not trigger any Jenkins job! --
   nita test run specific tacacs gui |  Triggers vDC_TACACS_Tests Jenkins job.
   nita test volumes |  Returns shared volumes information on test container.
   nita up |  Creates and starts NITA containers (both Core and CaaS).   |

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

    $ nita -d hello world

    >>>> command:  docker run hello-world


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

    $ nita -d example command

    >>>> command:  docker run alpine:latest cat /etc/alpine-release

    3.6.2

Enjoy creating your own docker-like or VMM-like CLI interface!!!

## Continuos integration (CI)

Continuous integration is the practice of routinely integrating code changes into the main branch of a repository and testing them as soon and often as possible. Any merge request (MR) into master branch triggers a CI/CD pipeline to validate those changes. It is made up of 2 different stages:

- test
- demo

Former runs a simple test to check if all available commands are well documented and latter triggers a CI pipeline of the whole NITA demo (on virtual-network project). 

## Troubleshooting

### Wrong command

If a wrong command is executed (i.e. there is a wrong key on the COMMANDS dictionary), NITA CLI will show you the following message:

    $ nita hello world

    'hello' key does not exist! Command: 'nita hello world' is incorrect!

     For a list of available commands, execute:

    >>>>  "nita --help" or "nita -h" or "nita ?"

Please, review `nita --help` or `nita -h` or `nita ?`output and look for the command you are looking for. If it is not there and you consider it should, submit a merge request to add it! You can always add it to your local copy if not a general purpose command!

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

During the demo both the NITA CLI command and its unix/docker/etc mapped command will be shown to prove the simplicity and intuition of NITA CLI. In order to enable the debugging of the mapped command, it is needed to add the `-d` option to NITA CLI.

Without debugging option:

    $ nita cli version
    NITA CLI master branch - 0.0.4

With (`-d`) debugging option, mapped command is shown on `>>>> command`:

    $ nita -d cli version

    >>>> command: echo NITA CLI master branch - $(pip3 list | grep nita-cli | awk '{print $2}')

    NITA CLI master branch - 0.0.4

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

    >>>>  "nita --help" or "nita -h" or "nita ?"


In a nutshell, anything you want to know about what NITA CLI does, just issue the NITA CLI help command:

    "nita --help" or "nita -h" or "nita ?"

and you will get all the things that NITA CLI can do for you!!!! You can even do it at any command level:

    $ nita webapp --help

    nita webapp cli => Attaches local standard input, output, and error streams to webapp running container.
    nita webapp ip => Returns IPs information on webapp container.
    nita webapp labels => Returns labels information on webapp container.
    nita webapp volumes => Returns shared volumes information on webapp container.
    nita webapp ports => Returns mapped ports information on webapp container.
    nita webapp logs => Fetches the logs of webapp container.

or

    $ nita tacacs cli -h

    nita tacacs cli => Attaches local standard input, output, and error streams to tacacs running container.

or

    $ nita dns ?

    nita dns cli => Attaches local standard input, output, and error streams to dns running container.
    nita dns ip => Returns IPs information on dns container.
    nita dns labels => Returns labels information on dns container.
    nita dns volumes => Returns shared volumes information on dns container.
    nita dns ports => Returns mapped ports information on dns container.
    nita dns logs => Fetches the logs of dns container.

_Benefits_: It is completely reusable among other products. Not tight to NITA. So it is an easy way to map complex commands to simple and intuitive ones related to your framework!

## Contact

`Juniper Internal only`

We would like to lead you and your customers into the Network Automation world!

Get in touch with us! How?

- Submit bugs, features, roadmap items to Visual Studio Teams (VST):

    https://ps-network-automation.visualstudio.com/NITA

- Request access to our [MS Teams](https://products.office.com/en-us/microsoft-teams/group-chat-software) workspace:

    NITA team (public).

Share anything with us (request, issues, concerns, suggestions, etc...) on any of the different channels depending on the topic:

 Channel | Description
---------|----------
General  | NITA Company-wide announcements and work-based matters
Development | NITA development channel
Support | NITA support channel
 |

If none of above recommended options works for you, write an e-mail to:

Contact Name | e-mail
---------|----------
Jose Miguel Izquierdo | jizquierdo@juniper.net
Ignacio Suarez | inavas@juniper.net
Andrew Sharp | asharp@juniper.net
 |
Thanks for using NITA!
