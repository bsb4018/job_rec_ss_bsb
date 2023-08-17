# Job Recommender System

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) &nbsp; ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) &nbsp; ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) &nbsp; ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) &nbsp; <br> ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) &nbsp; ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) &nbsp; ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


## Problem Statement
Job Recommender System for recommending jobs to candidates in a jobs-board-website platform
Candidates Get Recommended based on
#### 1. Key Skills that the candidates possess -> Candidates enters key skills
#### 2. Job Skills -> Key skills required for the jobs are matched with candidate key skills

## Solution Proposed
We frame the problem as a semantic search problem where we embedd job skills and index them to perform similarity search with user key skills as input query
We use MongoDB to store our jobs data for our prediction pipeline
We use pretrained SBERT model for embedding and FAISS similarity search for scalability

## Data
We collect data including collecting Job name, Company name, Experience required, Key Skills required for the job from each broad job category like Tech and IT, Human Resources, Management etc.
We searched each category like IT, Human Resources, Sales and Management, Analytics etc. take jobs information from the results we get from various online job portals. We currently take only the Job Name, Company Name, Key Skills, and Experience Required for the position. In this project the intention to keep a short window of jobs as in a week-old job for building the recommendation system.
This could be extended for 3 weeks to up to a month since fresh jobs are out in that timeframe and we do not want to use jobs data that are older than that timeframe since most jobs usually get filled within that time frame and new fresh job openings are out. 

![image](https://github.com/bsb4018/job_rec_ss_bsb/blob/main/docs/data_img.png)

## Tech Stack Used
1. Python 
2. MongoDB
3. Pytorch SBERT
4. AWS
5. Docker
6. Streamlit


## Infrastructure Required
1. AWS S3
2. AWS ECR
3. AWS EC2
4. AWS Elastic IP
5. Github Actions
6. Terraform


## How to run?
Before running the project, we need to make sure that you are having MongoDB compass account since we are using MongoDB for some data storage. <br>
We also need AWS account to access S3, ECR, EC2, Elastic IP Services. <br>
Also terraform should be installed and configured.


## Project Architecture
![image](https://github.com/bsb4018/job_rec_ss_bsb/blob/main/docs/hld.png)

## Deployment Architecture
![image](https://github.com/bsb4018/job_rec_ss_bsb/blob/main/docs/deployment.png)

## Run Steps

### Step 1: Clone the repository
```bash
git clone https://github.com/bsb4018/job_rec_ss_bsb.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -p venv python=3.8 -y
```

```bash
conda activate venv/
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```


### Step 4 - Setup MongoDB Compass

Create a MongoDB Compass Account <br>
Create a project and a cluster <br>
Get the database connection string <br>
MONGO_DB_URL = "database connection string"


### Step 5 – Setup Infrastructure using Terraform

Create an S3 bucket with “unique_name” from AWS Console to store terraform state <br>
Goto infrastructure/module.tf and replace the name <br>
terraform { <br>
   backend "s3" { <br>
    bucket = “unique_name” <br>

Open terminal and type the following
```bash
cd infrastructure
terraform init
terraform plan
terraform apply
Enter yes on prompt Enter a value
```

### Step 6 - AWS EC2 setup

Open the EC2 instance page in AWS Console <br>
Select the EC2 instance created using Terraform [Name: App Server] <br>
Select Security -> Security Groups -> Edit inbound rules -> Add rule <br>
Type – Custom TCP <br>
Port – 8501 <br>
Source – 0.0.0.0/0 <br>
Select Save rules <br>
Connect to the EC2 machine and run the following commands

```bash
sudo apt-get update -y
sudo apt-get upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

Open the repository in GitHub <br>
Goto Settings -> Actions -> Runners -> New self-hosted runner -> Linux <br>
Copy and run the given commands on the connected EC2 machine <br>

When prompted to enter the name of the runner -> Enter “self-hosted” <br>
When prompted Connected to GitHub Listening for Jobs -> Our server is ready 


### Step 7 – AWS S3 Buckets setup
#### Data Bucket
Open AWS Console and create AWS S3 bucket to store data <br>
Create a folder with name data-v1.0 and upload the data excel file jobs_data.xlsx inside it.
Goto src/constants/file_constants.py and replace the name DATA_BUCKET_NAME with the name of the bucket created <br>
#### Model and Artifacts Bucket (For Cloud Deployment)
We will use the bucket already created by Terraform to store the model and artifacts since it forms the part of model pipeline <br>
Goto AWS S3 console and find the S3 bucket “aws-account-num”bsb4018-job-rec-s3 and copy the name <br>
Goto src/constants/file_constants.py and replace the name MODEL_BUCKET_NAME accordingly


### Step 8 – AWS ECR setup

Open AWS ECR Console and note the name of the ECR created using Terraform <br>
It will of format somenum.dkr.ecr.region-name.amazonaws.com/job_rec-bsb4108-ecr <br>
Get a note of the following two which will be our environment secrets <br>
AWS_ECR_LOGIN_URI = somenum.dkr.ecr.region-name.amazonaws.com <br>
ECR_REPOSITORY_NAME = job_rec-bsb4108-ecr <br>

Additionally get a note of the following <br>
AWS_ACCESS_KEY_ID = “secret access id of AWS account” <br>
AWS_SECRET_ACCESS_KEY = “secret access key of AWS account” <br>
AWS_REGION_NAME = “region-name”


### Step 9 – Add the following to GitHub Secrets

MONGO_DB_URL=<MONGO_DB_URL> <br>
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> <br>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> <br>
AWS_REGION_NAME=<AWS_REGION_NAME> <br>
AWS_ECR_LOGIN_URI = <AWS_ECR_LOGIN_URI> <br>
ECR_REPOSITORY_NAME = <ECR_REPOSITORY_NAME> 

### Step 10 – Deploy CICD pipeline

Push Changes to trigger CICD Pipeline
```bash
git add
git commit -m “message”
git push origin main
```

### Step 11 – Open the app using Public IP
Replace https to http and add “:8501” at the end of URL


### Step 12 – Exit and Destroy the resources

```bash
cd infrastructure
terraform destroy
Enter yes on prompt Enter a value
```

### [Extra] Step 13 - Run locally
Follow Step 1,2,3,4,7 Data Bucket Part
Open the repository and run the following command
```bash
streamlit run sapp.py
```
