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
                    sh "python --version"
                }
            }
        }
    }
}