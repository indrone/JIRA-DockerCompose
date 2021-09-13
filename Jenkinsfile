pipeline {
  agent any
  stages {
    stage("build") {
      steps {
        sh """
          ls
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