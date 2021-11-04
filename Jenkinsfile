pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs  '--target build'
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