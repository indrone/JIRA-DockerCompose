pipeline {
  agent any
  stages {
    stage("build") {
      steps {
        sh """
          pwd
        """
      }
    }
    stage("run") {
      steps {
        sh """
          docker-compose up
        """
      }
    }
  }
}