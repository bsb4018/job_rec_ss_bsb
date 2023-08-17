# Job Recommender System

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) &nbsp; ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) &nbsp; ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) &nbsp; ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) &nbsp; <br> ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) &nbsp; ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) &nbsp; ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


### Problem Statement
Job Recommender System for recommending jobs to candidates in a jobs-board-website platform
Candidates Get Recommended based on
#### 1. Key Skills that the candidates possess -> Candidates enters key skills
#### 2. Job Skills -> Key skills required for the jobs are matched with candidate key skills

### Solution Proposed
We frame the problem as a semantic search problem where we embedd job skills and index them to perform similarity search with user key skills as input query
We use MongoDB to store our jobs data for our prediction pipeline
We use pretrained SBERT model for embedding and FAISS similarity search for scalability

## Tech Stack Used
#### 1. Python 
#### 2. MongoDB
#### 3. Pytorch SBERT
#### 3. AWS
#### 4. Docker 
#### 5. Streamlit


## Infrastructure Required.
#### 1. AWS S3
#### 2. AWS ECR
#### 3. AWS EC2
#### 4. AWS Elastic IP
#### 5. Github Actions
#### 6. Terraform


## How to run?
Before we run the project, make sure that you are having MongoDB compass account since we are using MongoDB for some data storage. You also need AWS account to access S3, ECR, EC2, Elastic IP Services. You also need to have terraform installed and configured.


## Project Architecture
![image](https://github.com/bsb4018/job_rec_ss_bsb.git/blob/main/docs/hld.png)

## Deployment Architecture
![image](https://github.com/bsb4018/job_rec_ss_bsb.git/blob/main/docs/deployment.png)

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

Create a MongoDB Compass Account  
Create a project and a cluster 
Get the database connection string
MONGO_DB_URL = "database connection string"


### Step 5 – Setup Infrastructure using Terraform

Create an S3 bucket with “unique_name” from AWS Console to store terraform state
Goto infrastructure/module.tf and replace the name 
terraform {
   backend "s3" {
    bucket = “unique_name”

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
Enter yes on prompt Enter a value
```

### Step 6 - AWS EC2 setup

Open the EC2 instance page in AWS Console
Select the EC2 instance created using Terraform [Name: App Server]
Select Security -> Security Groups -> Edit inbound rules -> Add rule
Type – Custom TCP
Port – 8501
Source – 0.0.0.0/0
Select Save rules
Connect to the EC2 machine and run the following commands

```bash
sudo apt-get update -y
sudo apt-get upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

Open the repository in GitHub
Goto Settings -> Actions -> Runners -> New self-hosted runner -> Linux
Copy and run the given commands on the connected EC2 machine

When prompted to enter the name of the runner -> Enter “self-hosted”
When prompted Connected to GitHub Listening for Jobs -> Our server is ready


### Step 7 – AWS S3 Buckets setup

Open AWS Console and create AWS S3 bucket to store data
Goto src/constants/file_constants.py and replace the name DATA_BUCKET_NAME with the name of the bucket created

We will use the bucket already created by Terraform to store the model and artifacts since it forms the part of model pipeline
Goto AWS S3 console and find the S3 bucket “aws-account-num”bsb4018-job-rec-s3 and copy the name
Goto src/constants/file_constants.py and replace the name MODEL_BUCKET_NAME accordingly


### Step 8 – AWS ECR setup

Open AWS ECR Console and note the name of the ECR created using Terraform
It will of format somenum.dkr.ecr.region-name.amazonaws.com/job_rec-bsb4108-ecr
Get a note of the following two which will be our environment secrets
AWS_ECR_LOGIN_URI = somenum.dkr.ecr.region-name.amazonaws.com
ECR_REPOSITORY_NAME = job_rec-bsb4108-ecr

Additionally get a note of the following
AWS_ACCESS_KEY_ID = “secret access id of AWS account”
AWS_SECRET_ACCESS_KEY = “secret access key of AWS account”
AWS_REGION_NAME = “region-name”


### Step 9 – Add the following to GitHub Secrets

MONGO_DB_URL=<MONGO_DB_URL
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
AWS_REGION_NAME=<AWS_REGION_NAME>
AWS_ECR_LOGIN_URI = <AWS_ECR_LOGIN_URI>
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
Open the repository and run the following command
```bash
streamlit run sapp.py
```