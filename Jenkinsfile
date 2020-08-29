pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh(script: 'ls')
            }
        }
        stage('test') {
            steps {
                sh(script: 'pwd')
                echo "Hi"
                echo "${env.GIT_BRANCH}"
            }
        }
        stage('stage') {
            when {
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                sh(script: 'ls')
                input 'Deploy to Production?'
            }
        }
        stage('production') {
            when {
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                sh(script: 'ls')
            }
        }
    }
}