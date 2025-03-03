pipeline {
    agent any 

    stages {
        stage('Build Stage') {
            steps {
                echo "Imagine a build step here."
            }
        }

        stage('Unit Tests') {
            steps {
                sh "/usr/bin/python3 --version"
                sh "/usr/bin/python3 -m venv venv"
                sh "venv/bin/pip install -r requirements.txt"
                sh "venv/bin/pytest test.py"
            }
        }

        stage('Deploy Stage') {
            steps {
                echo "Imagine we are deploying the application here"
            }
        }
    }
}