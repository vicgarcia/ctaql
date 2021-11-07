pipeline {
    agent any
    options {
        ansiColor('xterm')
    }
    stages {
        stage('Build Base Container') {
            steps {
                script {
                    def buildImage = docker.build('vicg4rcia/ctaql-build', '--target=build --progress=plain .')
                }
            }
        }
        stage('Run Unit Tests') {
            steps {
                script {
                    def testImage = docker.build('vicg4rcia/ctaql-test', '--target=test --progress=plain .')
                    testImage.inside('--user 0:0') {
                        sh 'cd /app && pipenv run pytest'
                    }
                }
            }
        }
        stage('Build Production Container') {
            steps {
                script {
                    def prodImage = docker.build('vicg4rcia/ctaql', '--target production --progress=plain .')
                    docker.withRegistry('', 'docker-hub-user-credentials') {
                        prodImage.push("$BUILD_NUMBER")
                        prodImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy Production Container') {
            steps {
                sh 'echo "todo: run docker compose w/ host + env vars"'
            }
        }
    }
}