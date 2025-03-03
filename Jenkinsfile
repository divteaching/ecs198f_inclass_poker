pipeline {
    agent any 
    environment {
        PYTHON_ENV = 'venv'
    }
    stages {
        stage('Python Envrionment Setup') {
            steps {
                script {
                    sh "python3 -m venv ${PYTHON_ENV}"
                    sh "source ${PYTHON_ENV}/bin/activate"
                    sh "pip install -r requirements.txt"
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    sh "source ${PYTHON_ENV}/bin/activate && pytest test.py"
                }
            }
        }
    }
}