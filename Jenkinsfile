pipeline {
    agent any
    stages {
        stage('Test') {
            environment {
                PIPENV_VENV_IN_PROJECT = 1
            }
            steps {
                sh """
                pipenv install --dev
                pipenv run pytest
                """.stripIndent()
            }
        }
    }
}