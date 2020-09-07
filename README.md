# ELK Stack


"ELK" is the acronym for three open source projects: Elasticsearch, Logstash, and Kibana. 
    Elasticsearch is a search and analytics engine. 
    Logstash is a server‑side data processing pipeline that ingests data from multiple sources simultaneously, transforms it, and then sends it to a "stash" like Elasticsearch. 
    Kibana lets users visualize data with charts and graphs in Elasticsearch.

ELK Stack fulfills the need log management and analytics space. Monitoring applications and the IT infrastructure they are deployed on requires a log management and analytics solution that enables engineers to overcome the challenge of monitoring what are highly distributed, dynamic and noisy environments.

# Manual Deployment
## Environment setup

   * Install [Python](https://www.python.org/downloads/) 
   * Install [Docker](https://docs.docker.com/engine/install/)
   * Install [docker-compose](https://docs.docker.com/compose/install/)
   * Install [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) (Optional - Required only when deploying the cluster on local kubenretes)
   * Install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) (Optional - Required only when deploying the cluster in AWS)
   * Clone the repo
   * Run `cd reponame`
   * Run `pip install .`


## Config files setup

The repo uses `.env` file for building the ELK stack for a specific version; update this file with the desired verion of the ELK Stack

    "ELK_VERSION": "Desired Version of ELK"

The repo uses deploy_config.yml file for deploying the cluster on __AWS__. Update the list of host to update/create in your AWS account.

```
    ---
    hosts:
    - ClusterName1
    - ClusterName1
```

## Deployment
----------------------------------------------------------
### Docker

   * Run `docker-compose up`
   * Access the applications at below ports (http://localhost:<port>)
    
| Port | Application | 
|--|--|
| 5601 | Kibana |
| 9200 | Elasticsearch |
| 5044/9600 | Logstash |

### Kubernetes on local system

   * Run `minikube start --driver=docker`
   * Run `kubectl apply -f k8s/`
   * Add `ansible/roles/kube_init/templates/local.conf` to `/etc/nginx/conf.d/` with updated values
   * Try to access the cluster at below url endpoints (http://localhost_ip/<endpoint>)

| Endpoint | Application | 
|--|--|
| /kibana/ | Kibana |
| /elasticsearch/ | Elasticsearch |
| /logstash/ or /logstash_ui/ | Logstash |

### Deploy cluster on new EC2 instance 
 
   * Run `cd ansible`
   * Update `vars/all.yml` file with appropriate values
   * Run `ansible-playbook deploy_instalce.yml -e 'aws_access_key=ACCESS_KEY aws_secret_key=SECRET_KEY`
   * Try to access the cluster at above mentioned url endpoints replacing the localhost_ip to Public IP of the instance

----------------------------------------------------------

# Automated Deployment (CICD)

----------------------------------------------------------

## Environment setup

   * Install and Setup [Jenkins](https://www.jenkins.io/doc/book/installing/)
   * Install following plugins on Jenkins
        - Git
        - GitHub
        - Ansible
   * Configure GitHUB in Jenkins
   * Add Github Webhook to your Git repository http://<JenkinsURL>/github-webhook
   * Create a pipeline job and configure it to listen on github push requests
   * Add below mandatory credentials to jenkins
        - GitHub credentials
        - Github OAuth tocken
        - DockerHUB credentials
        - AWS Access and Secret keys

## CICD flow

CICD for the repo is in place which on a commit to dev/master branches triggers a jenkins pipeline which builds the `docker images` using the version specified in `.env` file on the time of code push. The built images are used to spin up a cluster using `docker-compose` to test if all the things are in place to build ELK cluster, once the cluster is up and running, minimal `pytests` trigger to check each and every end point is accessible. Once the minimal tests pass, the built images are pushed to `DockerHub`. Pipeline will proceed further to deploy the ELK cluster on local Kubenretes `QA` environment. 

Above stages run for all branches in the github repo and pipeline proceeds to next steps only in case of `master` branch.

After the cluster is deployed in QA, pipeline will wait for users input (proceed/abort) to proceed thus allowing the user to validate the setup from his end, once the user provides an input to pipeline, the locally deployed cluster will be destroyed and try to run Ansible deployment and provisiong tasks of a new or existing EC2 instance, once the setup is ready, ansible will run the cluster deployment process onto prod machines.

                                    BUILD --> TEST --> PUSH --> QA --> PROD

----------------------------------------------------------
