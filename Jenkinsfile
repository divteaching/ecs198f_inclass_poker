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
                sh "/usr/bin/pip3 install -r requirements.txt"
            }
        }
    }
}