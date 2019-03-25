#!groovy

@Library('PS-Shared-libs') _

node() {
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
                stage('Unit tests'){
                    echo 'Running unit tests'
                    sh 'python3 setup.py test'
                }
                stage('Install'){
                    echo 'Running a test installation'
                    sh 'pip3 install --no-binary :all: .'
                }
                stage('Autocomplete'){
                    echo 'Generate autocomplete'
                    sh 'python3 autocomplete'
                }
                stage('Test'){
                    echo 'Testing help and version'
                    sh 'nita ?'
                    sh 'nita cli version'
                }
                stage('Publish'){
                    if (env.SOURCE_BRANCH == 'refs/heads/master') {
                        echo 'Push to Artifactory'
                        sh 'python3 setup.py sdist'
                        withCredentials([file(credentialsId:'f1503ca7-3285-4ac6-ae55-5a660658c075', variable: 'PYPIRC')]) {
                            sh 'ln -s $PYPIRC $HOME/.pypirc'
                            sh 'python3 setup.py sdist upload -r local'
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
