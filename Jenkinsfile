pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                def testImage = docker.build('test-image', '--target test')
                testImage.inside {
                    sh 'pwd && cd /code && pipenv run pytest'
                }
            }
        }
    }
}