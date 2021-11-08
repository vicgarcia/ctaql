pipeline {
    agent any
    options {
        ansiColor('xterm')
    }
    stages {
        // stage('Build Base Container') {
        //     steps {
        //         script {
        //             def buildImage = docker.build('vicg4rcia/ctaql-build', '--target=build --progress=plain .')
        //         }
        //     }
        // }
        // stage('Run Unit Tests') {
        //     steps {
        //         script {
        //             def testImage = docker.build('vicg4rcia/ctaql-test', '--target=test --progress=plain .')
        //             testImage.inside('--user 0:0') {
        //                 sh 'cd /app && pipenv run pytest'
        //             }
        //         }
        //     }
        // }
        // stage('Build Production Container') {
        //     steps {
        //         script {
        //             def prodImage = docker.build('vicg4rcia/ctaql', '--target production --progress=plain .')
        //             docker.withRegistry('', 'docker-hub-user-credentials') {
        //                 prodImage.push("$BUILD_NUMBER")
        //                 prodImage.push('latest')
        //             }
        //         }
        //     }
        // }
        stage('Deploy Production Container') {
            environment {
                DOCKER_HOST = credentials('docker-host-ssh-connection-string')
                CTA_BUSTRACKER_API_KEY = credentials('ctaql-cta-api-key')
                DJANGO_SECRET_KEY = credentials('ctaql-django-secret-key')
            }
            steps {
                sh 'docker -H $DOCKER_HOST stop ctaql'
                sh 'docker -H $DOCKER_HOST rm ctaql'
                sh '''
                docker -H $DOCKER_HOST run -p 8001:8000 \
                --env CTA_BUSTRACKER_API_KEY=$CTA_BUSTRACKER_API_KEY \
                --env DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
                --name ctaql -d vicg4rcia/ctaql:latest
                '''
            }
        }
    }
}