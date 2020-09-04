pipeline {
    agent any
    stages {
        stage('Build') {
                        when {
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                sh(script:  """curl "https://api.github.com/repos/Sundeep55/ELK/statuses/${GIT_COMMIT}?access_token=34d6c62a303e5a3560f5c43765ca1e385c81ff07" \
                              -H "Content-Type: application/json" \
                              -X POST \
                              -d '{"state": "pending","context": "continuous-integration/jenkins", "description": "Jenkins", "target_url": "http://15.207.4.186:8080/job/ELKStack/${BUILD_NUMBER}/console"}' """)
                sh 'docker-compose build'
                sleep(time:10,unit:"SECONDS")
            }
        }
        stage('Test') {
                        when {
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
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
                }
            }
            post {
                cleanup {
                    sh "docker logout"
                }
            }
        }
        stage('Deploy in QA') {
            steps {
                sh "minikube start --driver=docker"
                sh "minikube addons enable ingress"
                sh "kubectl wait --namespace kube-system --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s"
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
                beforeAgent true
                expression {
                    GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'awscreds',
                    usernameVariable: 'AWS_ACCESS_KEY', passwordVariable: 'AWS_SECRET_KEY']]) {
                    dir('ansible') {
                        ansiblePlaybook playbook: 'deploy_instance.yml', 
                                        inventory: 'inventory.ini',
                                        extras: "-e aws_access_key=${AWS_ACCESS_KEY} aws_secret_key=${AWS_SECRET_KEY}"
                    }
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
