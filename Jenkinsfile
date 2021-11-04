pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs  '--target build'
            args '--user 0:0'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'pipenv run pytest'
            }
        }
    }
}