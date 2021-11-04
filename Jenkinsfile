pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs  '--target test'
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