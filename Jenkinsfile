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
                sleep(time:2,unit:"MINUTES")
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
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]) {
                    load "${WORKSPACE}/.env"
                    sh "docker build -t ${DOCKER_USERNAME}/elasticsearch:${ELK_VERSION} elasticsearch/ --build-arg ELK_VERSION=${ELK_VERSION}"
                    sh "docker build -t ${DOCKER_USERNAME}/logstash:${ELK_VERSION} logstash/ --build-arg ELK_VERSION=${ELK_VERSION}"
                    sh "docker build -t ${DOCKER_USERNAME}/kibana:${ELK_VERSION} kibana/ --build-arg ELK_VERSION=${ELK_VERSION}"
                    sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                    sh "docker push ${DOCKER_USERNAME}/elasticsearch:${ELK_VERSION}"
                    sh "docker push ${DOCKER_USERNAME}/logstash:${ELK_VERSION}"
                    sh "docker push ${DOCKER_USERNAME}/kibana:${ELK_VERSION}"
                }
            }
        }
        stage('Deploy in QA') {
            when {
                beforeAgent true
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                // input 'Deploy to Production?'
                sh(script: 'ls')
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