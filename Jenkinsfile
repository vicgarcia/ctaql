pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs  '--target test'
            args '--user 0:0'
        }
    }
    stages {
        stage('Test') {
            steps {
                dir(path: '/code') {
                    sh 'pipenv run pytest'
                }
            }
        }
    }
}