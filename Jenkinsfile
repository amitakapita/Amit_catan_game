pipeline {
    agent { docker { image 'python:3.14.3-alpine3.23' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
