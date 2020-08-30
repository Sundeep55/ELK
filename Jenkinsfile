pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker-compose build'
                sleep(time:30,unit:"SECONDS")
            }
        }
        stage('Functional Test') {
            steps {
                sh 'docker-compose up -d'
                sleep(time:1,unit:"MINUTES")
                sh 'pytest'
            }
            post {
                cleanup {
                    sh 'docker-compose down'
                }
            }
        }
        stage('Push to registry') {
            when {
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            environment {
                DOCKER_HUB_REPO = 'sundeep55'
            }
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'gitauth',
                    usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]) {
                    load "${WORKSPACE}/.env"
                    sh "docker build -t ${DOCKER_HUB_REPO}/elasticsearch:${ELK_VERSION} elasticsearch/"
                    sh "docker build -t ${DOCKER_HUB_REPO}/logstash:${ELK_VERSION} logstash/"
                    sh "docker build -t ${DOCKER_HUB_REPO}/kibana:${ELK_VERSION} kibana/"
                    sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                    sh "docker push ${DOCKER_HUB_REPO}/elasticsearch:${ELK_VERSION}"
                    sh "docker build ${DOCKER_HUB_REPO}/logstash:${ELK_VERSION}"
                    sh "docker build ${DOCKER_HUB_REPO}/kibana:${ELK_VERSION}"
                }
            }
        }
        stage('Deploy in QA') {
            agent {
                label "QA"
            }
            when {
                beforeAgent true
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            steps {
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