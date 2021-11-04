pipeline {
    agent any
    stages {

        stage('Test') {
            steps {
                script {
                    def testImage = docker.build('test-image', '--target test .')
                    testImage.run()
                    // testImage.inside('--user 0:0') {
                    //     sh 'pwd && cd /code && pipenv run pytest'
                    // }
                }
            }
        }

        // stage('Push') {
        //     steps {
        //         script {
        //             def prodImage = docker.build('prod-image', '--target prod')
        //         }
        //     }
        // }
    }
}