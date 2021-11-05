pipeline {
    agent any
    stages {

        stage('Build Base Container') {
            steps {
                script {
                    def baseImage = docker.build('ctaql-base', '--target=base --progress=plain .')
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def testImage = docker.build('test-image', '--target=test --progress=plain .')
                    testImage.inside('--user 0:0') {
                        sh 'cd /code && pipenv run pytest'
                    }
                }
            }
        }

        stage('Update Infrastructure') {
            steps {
                sh 'echo "todo: terraform here"'
                sh 'echo "vpc, alb, fargate"'
            }
        }

        stage('Build Containers') {
            steps {
                script {
                    def prodImage = docker.build('prod-image', '--target production --progress=plain .')
                }
                sh 'echo "todo: push container to ECR"'
            }
        }

    }
}