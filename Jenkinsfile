pipeline {
  agent any
  stages {
    stage("build") {
      steps {
        sh """
          sudo docker build -t hello_there .
        """
      }
    }
    stage("run") {
      steps {
        sh """
          sudo docker run --rm hello_there
        """
      }
    }
  }
}