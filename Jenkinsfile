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
                sh 'pwd'
                sh 'cd /code'
                sh 'pwd'
                sh 'pipenv run pytest'
            }
        }
    }
}