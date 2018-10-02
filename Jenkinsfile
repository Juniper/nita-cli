#!groovy
/*
# Copyright 2017 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties,
# software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied.
*/
@Library('PS-Shared-libs') _

node('master') {
    try {
        stage('Checkout'){
            checkout scm
        }
        withDockerRegistry(credentialsId: 'ps-ci', toolName: 'master', url: 'https://ps-docker.artifactory.aslab.juniper.net') {
            docker.image('ps-docker.artifactory.aslab.juniper.net/py-builder:latest').inside('-u root') {
                stage('Cleanup'){
                    echo 'cleanup'
                    sh 'rm -rf dist'
                    sh 'rm -rf .pypirc'
                }
                stage('Test'){
                    echo 'Running unit tests'
                    sh 'python3 setup.py test'
                    ciSkip action: 'check'
                }
                stage('Install'){
                    echo 'Running a test installation'
                    sh 'pip3 install .'
                    ciSkip action: 'check'
                }
                stage('Autocomplete'){
                    echo 'Generate autocomplete'
                    sh 'python3 autocomplete'
                }
                stage('Publish'){
                    if (env.SOURCE_BRANCH == 'refs/heads/master') {
                        echo 'Push to Artifactory'
                        sh 'python3 setup.py sdist'
                        withCredentials([file(credentialsId:'pypirc', variable: 'PYPIRC')]) {
                            sh 'ln -s $PYPIRC $HOME/.pypirc'
                            sh 'python3 setup.py sdist upload -r artifactory'
                        }
                    }
                    else {
                        echo "Only the master branch is published to the repository"
                    }
                }
                stage('Test pull'){
                    if (env.SOURCE_BRANCH == 'refs/heads/master') {
                        echo 'Push to Artifactory'
                        sh 'pip3 install -i https://artifactory.aslab.juniper.net/artifactory/api/pypi/ps-pypi/simple nita-cli'
                    } 
                }
            }
        }
    }
    finally {
        ciSkip action: 'postProcess'
    }
}
