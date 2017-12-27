#!/usr/bin/python
# <*******************
# 
# Copyright 2018 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 
# *******************>
"""
    Python module containing all NITA commands and CONSTANTS
"""

# CONSTANTS
KEY_SEPARATOR = ' '
PROJECT_PATH = '/Users/jizquierdo/Documents/Juniper/Projects/NITA/virtualdc'

# COMMANDS TREE
COMMANDS = {
    'nita': {
        'containers': 'docker ps --filter "label=net.juniper.framework=NITA"',
        'images':     'docker images --filter "label=net.juniper.framework=NITA"',
        'stats':      'docker stats webapp jenkins tacacs radius ntp dns --no-stream',
        'jenkins': {
            'jobs': {
                'ls':     'docker exec -it jenkins list_jenkins_jobs.py',
                'remove': 'docker exec -it jenkins remove_from_jenkins.py -y --regex REGEX'
            },
            'cli': {
                'jenkins': 'docker exec -it -u jenkins jenkins /bin/bash',
                'root':    'docker exec -it -u root jenkins /bin/bash'
            },
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' jenkins',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' jenkins',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' jenkins | jq',
            'logs': 'docker logs jenkins --tail 200'
        },
        'ansible': {
            'run': {
                'noob':  'docker run --rm --volumes-from jenkins -v %s:/project registry.juniper.net/nita/ansible:latest ./noob.sh',
                'build': 'docker run --rm --volumes-from jenkins -v %s:/project registry.juniper.net/nita/ansible:latest ./build.sh'
            },
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' ansible',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' ansible',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' ansible | jq',
            'cli':  'docker run -d --rm --name ansible -it --volumes-from jenkins -v %s:/project registry.juniper.net/nita/ansible:latest /bin/sh ; docker attach ansible'
        },
        'robot': {
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' robot',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' robot',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' robot | jq',
            'cli':  'docker run -d --rm --name robot -it --volumes-from jenkins -v %s:/project registry.juniper.net/nita/robot:latest /bin/sh ; docker attach robot'
        },
        'webapp': {
            'logs': 'docker logs webapp --tail 200',
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' webapp',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' webapp',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' webapp | jq',
            'cli':  'docker exec -it webapp /bin/bash'
        },
        'tacacs': {
            'logs': 'docker run -it tacacs tail -200 /var/log/tacacs.log',
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' tacacs',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' tacacs',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' tacacs | jq',
            'cli':  'docker exec -it tacacs /bin/bash'
        },
        'radius': {
            'logs': 'docker logs radius --tail 200',
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' radius',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' radius',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' radius | jq',
            'cli':  'docker exec -it radius /bin/bash'
        },
        'ntp': {
            'logs': 'docker logs ntp --tail 200',
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' ntp',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' ntp',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' ntp | jq',
            'cli':  'docker exec -it ntp /bin/sh'
        },
        'dns': {
            'logs': 'docker logs dns --tail 200',
            'ip': 'docker inspect --format=\'{{range .NetworkSettings.Networks}}   {{.IPAddress}}{{end}}\' dns',
            'ports': 'docker inspect --format=\'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}\' dns',
            'volumes': 'docker inspect --format \'{{json .Mounts}}\' dns | jq',
            'cli':  'docker exec -it dns /bin/sh'
        },
        # 'project': {
        #     'new': 'mkdir -p %s/build %s/doc %s/group_vars %s/host_vars %s/jenkins %s/noob %s/roles %s/test/configs %s/test/libraries %s/test/outputs %s/test/resource_files %s/test/scripts %s/test/suites %s/test/templates %s/test/variables_file'
        # },
        'license':"""
# <*******************
# 
# Copyright 2018 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 
# *******************>
# """
    }
}

# HELP TREE
HELP = {
    'nita': {
        'containers': 'Lists all NITA containers.',
        'images':     'Lists all NITA images.',
        'stats':      'Displays the NITA containers resource usage statistics.',
        'jenkins': {
            'jobs': {
                'ls':     'Lists all Jenkins jobs.',
                'remove': 'Removes Jenkins jobs containing REGEX. Assume "yes" as answer to all prompts and run non-interactively.'
            },
            'cli': {
                'jenkins': 'Attaches local standard input, output, and error streams to jenkins running container with "jenkins" user.',
                'root':    'Attaches local standard input, output, and error streams to jenkins running container with "root" user.'
            },
            'ip':      'Returns IPs information on jenkins container.',
            'ports':   'Returns mapped ports information on jenkins container.',
            'volumes': 'Returns shared volumes information on jenkins container.',
            'logs':    'Fetches the logs of jenkins container.'
        },
        'ansible': {
            'run': {
                'noob':  'Runs NOOB process (./noob.sh script) on /project located at $PROJECT_PATH.',
                'build': 'Runs Build process (./build.sh script) on /project located at $PROJECT_PATH.'
            },
            'ip':      'Returns IPs information on ansible container.',
            'ports':   'Returns mapped ports information on ansible container.',
            'volumes': 'Returns shared volumes information on ansible container.',
            'cli':     'Attaches local standard input, output, and error streams to ansible running container.'
        },
        'robot': {
            'ip':      'Returns IPs information on robot container.',
            'ports':   'Returns mapped ports information on robot container.',
            'volumes': 'Returns shared volumes information on robot container.',
            'cli':     'Attaches local standard input, output, and error streams to robot running container.'
        },
        'webapp': {
            'logs':    'Fetches the logs of webapp container.',
            'ip':      'Returns IPs information on webapp container.',
            'ports':   'Returns mapped ports information on webapp container.',
            'volumes': 'Returns shared volumes information on webapp container.',
            'cli':     'Attaches local standard input, output, and error streams to webapp running container.'
        },
        'tacacs': {
            'logs':    'Fetches the logs of tacacs container.',
            'ip':      'Returns IPs information on tacacs container.',
            'ports':   'Returns mapped ports information on tacacs container.',
            'volumes': 'Returns shared volumes information on tacacs container.',
            'cli':     'Attaches local standard input, output, and error streams to tacacs running container.'
        },
        'radius': {
            'logs':    'Fetches the logs of radius container.',
            'ip':      'Returns IPs information on radius container.',
            'ports':   'Returns mapped ports information on radius container.',
            'volumes': 'Returns shared volumes information on radius container.',
            'cli':     'Attaches local standard input, output, and error streams to radius running container.'
        },
        'ntp': {
            'logs':    'Fetches the logs of ntp container.',
            'ip':      'Returns IPs information on ntp container.',
            'ports':   'Returns mapped ports information on ntp container.',
            'volumes': 'Returns shared volumes information on ntp container.',
            'cli':     'Attaches local standard input, output, and error streams to ntp running container.'
        },
        'dns': {
            'logs':    'Fetches the logs of dns container.',
            'ip':      'Returns IPs information on dns container.',
            'ports':   'Returns mapped ports information on dns container.',
            'volumes': 'Returns shared volumes information on dns container.',
            'cli':     'Attaches local standard input, output, and error streams to dns running container.'
        },
        # 'project': {
        #     'new': 'mkdir -p %s/build %s/doc %s/group_vars %s/host_vars %s/jenkins %s/noob %s/roles %s/test/configs %s/test/libraries %s/test/outputs %s/test/resource_files %s/test/scripts %s/test/suites %s/test/templates %s/test/variables_file'
        # },
        'license': 'Displays the NITA License.'
    }
}

# docker run --rm --volumes-from jenkins -v PROJECT_PATH:/project registry.juniper.net/nita/ansible:latest ./noob.sh
# docker run --rm --volumes-from jenkins -v PROJECT_PATH:/project registry.juniper.net/nita/ansible:latest ./build.sh
# mkdir -p ${PWD}/output/${BUILD_NUMBER} ; docker run --rm --volumes-from jenkins -v PROJECT_PATH:/project -e ROBOT_OPTIONS=&quot;-d ${PWD}/output/${BUILD_NUMBER}&quot; registry.juniper.net/nita/robot:latest ./test.sh
