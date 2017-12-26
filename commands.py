#!/usr/bin/python
"""
    Python module containing all NITA commands and CONSTANTS
"""
KEY_SEPARATOR = ' '
PROJECT_PATH = '/Users/jizquierdo/Documents/Juniper/Projects/NITA/virtualdc'
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
            'logs': 'docker logs jenkins --tail 200'
        },
        'ansible': {
            'run': {
                'noob':  'docker run --rm --volumes-from jenkins -v %s:/project registry.juniper.net/nita/ansible:latest ./noob.sh',
                'build': 'docker run --rm --volumes-from jenkins -v %s:/project registry.juniper.net/nita/ansible:latest ./build.sh'
            },
            'cli':  'docker run -d --rm --name ansible -it --volumes-from jenkins -v %s:/project registry.juniper.net/nita/ansible:latest /bin/sh ; docker attach ansible'
        },
        'robot': {
            'cli':  'docker run -d --rm --name robot -it --volumes-from jenkins -v %s:/project registry.juniper.net/nita/ansible:latest /bin/sh ; docker attach robot'
        },
        'webapp': {
            'logs': 'docker logs webapp --tail 200',
            'cli':  'docker exec -it webapp /bin/bash'
        },
        'tacacs': {
            'logs': 'docker run -it tacacs tail -200 /var/log/tacacs.log',
            'cli':  'docker exec -it tacacs /bin/bash'
        },
        'radius': {
            'logs': 'docker logs radius --tail 200',
            'cli':  'docker exec -it radius /bin/bash'
        },
        'ntp': {
            'logs': 'docker logs ntp --tail 200',
            'cli':  'docker exec -it ntp /bin/sh'
        },
        'dns': {
            'logs': 'docker logs dns --tail 200',
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
# """,
    }
}

# docker run --rm --volumes-from jenkins -v PROJECT_PATH:/project registry.juniper.net/nita/ansible:latest ./noob.sh
# docker run --rm --volumes-from jenkins -v PROJECT_PATH:/project registry.juniper.net/nita/ansible:latest ./build.sh
# mkdir -p ${PWD}/output/${BUILD_NUMBER} ; docker run --rm --volumes-from jenkins -v PROJECT_PATH:/project -e ROBOT_OPTIONS=&quot;-d ${PWD}/output/${BUILD_NUMBER}&quot; registry.juniper.net/nita/robot:latest ./test.sh
