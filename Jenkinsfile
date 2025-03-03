pipeline {
    agent any 
    environment {
        PYTHON_ENV = 'venv'
    }
    stages {
        stage('Python Envrionment Setup') {
            steps {
                echo "Test :)"
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
    }
}