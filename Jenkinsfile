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
          sudo docker-compose up
        """
      }
    }
  }
}