pipeline {

    agent {
        label "master"
    }

    environment {
        ORG         = 'tomcusack1'
        APP_NAME    = 'ordrbook'
    }

    stages {

        stage('CI Build and push snapshot') {
            when {
                branch 'PR-*'
            }
            steps {
                container('jx-base') {
                    sh "echo 'hello'"
                }
            }
        }

        stage('Build and Push Release') {
            when {
                branch 'master'
            }
            steps {
                container('jx-base') {
                    sh "echo 'hello'"
                }
            }
        }
    }

}