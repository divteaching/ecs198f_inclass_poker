//Assume that the repository is cloned --> 
//Configure a package which will clone the repository and then start the pipeline

// Stage 1: Install all required packages (Build)

//Stage 2: Run Unit Tests (with pytest) (Testing)

//Stage 3: Review Process (Manual Review)

//Stage 4: Deploy (Upstream)

pipeline {
    agent any

    stages {
        stage('Build Stage') {
            steps {
                //Create a virtualenv first
                sh "/usr/bin/python3 -m venv venv"

                //Activate? --> Set Enivronment Variables. No need because we specify the executable path inside of venv
                sh "venv/bin/pip3 install -r requirements.txt"
            }
        }

        stage('Unit Testing') {
            steps {
                sh "venv/bin/pytest test.py"
            }
        }

        stage('Manual Review') {
            steps {
                echo 'Imagine Manual Review has passed'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Imagine Deploy is being done'
            }
        }
    }
}