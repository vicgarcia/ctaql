pipeline {
    agent any
    stages {

        stage('Run Tests') {
            steps {
                script {
                    def testImage = docker.build('test-image', '--target test .')
                    testImage.inside('--user 0:0') {
                        sh 'cd /code && pipenv run pytest'
                    }
                }
            }
        }

        stage('Deploy Infrastructure') {
            steps {
                sh 'echo "todo: terraform here"'
                sh 'echo "vpc, alb, fargate"'
            }
        }

        stage('Build Containers') {
            steps {
                sh 'echo "todo: build production container"'
                sh 'echo "todo: push container to ECR"'
                script {
                    def prodImage = docker.build('prod-image', '--target prod .')
                }
            }
        }

    }
}