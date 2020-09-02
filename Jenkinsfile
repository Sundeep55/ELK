pipeline {
    agent any
    stages {
        // stage ('SonarQube Scan') {
        //     environment {
        //         scannerHome = tool 'SonarQube'
        //     }
        //     steps { 
        //         withSonarQubeEnv('sonarserver') {
        //             sh "${scannerHome}/bin/sonar-scanner"
        //         }
        //         timeout(time: 10, unit: 'MINUTES') {
        //             waitForQualityGate abortPipeline: true
        //         }
        //     }
        // }
        stage('Build') {
            steps {
                sh(script:  """curl "https://api.github.com/repos/Sundeep55/ELK/statuses/${GIT_COMMIT}?access_token=34d6c62a303e5a3560f5c43765ca1e385c81ff07" \
                              -H "Content-Type: application/json" \
                              -X POST \
                              -d '{"state": "pending","context": "continuous-integration/jenkins", "description": "Jenkins", "target_url": "http://15.207.4.186:8080/job/ELKStack/${BUILD_NUMBER}/console"}' """)
                sh 'docker-compose build'
                sleep(time:10,unit:"SECONDS")
            }
        }
        stage('Functional Test') {
            steps {
                sh 'docker-compose up -d'
                sleep(time:90,unit:"SECONDS")
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
                    GIT_BRANCH == 'origin/master' //Chnage me later
                }
            }
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]) {
                    script {
                        SHA = sh(returnStdout: true, script: 'git rev-parse HEAD')
                    }
                    load "${WORKSPACE}/.env"
                    sh "docker build -t ${DOCKER_USERNAME}/elk_cluster_elasticsearch:${ELK_VERSION} elasticsearch/ --build-arg ELK_VERSION=${ELK_VERSION}"
                    sh "docker build -t ${DOCKER_USERNAME}/elk_cluster_logstash:${ELK_VERSION} logstash/ --build-arg ELK_VERSION=${ELK_VERSION}"
                    sh "docker build -t ${DOCKER_USERNAME}/elk_cluster_kibana:${ELK_VERSION} kibana/ --build-arg ELK_VERSION=${ELK_VERSION}"
                    sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                    sh "docker push ${DOCKER_USERNAME}/elk_cluster_elasticsearch:${ELK_VERSION}"
                    sh "docker push ${DOCKER_USERNAME}/elk_cluster_logstash:${ELK_VERSION}"
                    sh "docker push ${DOCKER_USERNAME}/elk_cluster_kibana:${ELK_VERSION}"
                    sh "docker push ${DOCKER_USERNAME}/elk_cluster_elasticsearch:${SHA}"
                    sh "docker push ${DOCKER_USERNAME}/elk_cluster_logstash:${SHA}"
                    sh "docker push ${DOCKER_USERNAME}/elk_cluster_kibana:${SHA}"
                }
            }
            post {
                cleanup {
                    sh "docker logout"
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
                sh "minikube start --driver=docker"
                sh "kubectl apply -f k8s/"
                sleep(time:120,unit:"SECONDS")
                input 'Deploy to Production?'
            }
            post {
                cleanup {
                    sh "kubectl delete -f k8s/"
                    sh "minikube stop"
                    sh "minikube delete"
                }
            }
        }
        stage('production') {
            when {
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                ansiblePlaybook('ansible/deploy_instance.yml') {
                    inventoryPath('inventory.ini')
                }
            }
        }
    }
    post {
        success {
            sh(script:  """curl "https://api.github.com/repos/Sundeep55/ELK/statuses/${GIT_COMMIT}?access_token=34d6c62a303e5a3560f5c43765ca1e385c81ff07" \
                            -H "Content-Type: application/json" \
                            -X POST \
                            -d '{"state": "success","context": "continuous-integration/jenkins", "description": "Jenkins", "target_url": "http://15.207.4.186:8080/job/ELKStack/${BUILD_NUMBER}/console"}' """)
        }
        failure {
            sh(script:  """curl "https://api.github.com/repos/Sundeep55/ELK/statuses/${GIT_COMMIT}?access_token=34d6c62a303e5a3560f5c43765ca1e385c81ff07" \
                            -H "Content-Type: application/json" \
                            -X POST \
                            -d '{"state": "failure","context": "continuous-integration/jenkins", "description": "Jenkins", "target_url": "http://15.207.4.186:8080/job/ELKStack/${BUILD_NUMBER}/console"}' """)
        }
        aborted {
            sh(script:  """curl "https://api.github.com/repos/Sundeep55/StatusRepo/statuses/${GIT_COMMIT}?access_token=34d6c62a303e5a3560f5c43765ca1e385c81ff07" \
                            -H "Content-Type: application/json" \
                            -X POST \
                            -d '{"state": "error","context": "continuous-integration/jenkins", "description": "Jenkins", "target_url": "http://15.207.4.186:8080/job/ELKStack/${BUILD_NUMBER}/console"}' """)
        }
    }
}
