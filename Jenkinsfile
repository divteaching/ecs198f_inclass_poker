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
                withPythonEnv('python') {
                    sh "pip install -r requirements.txt"
                    sh "pytest test.py"
                }
            }
        }
    }
}