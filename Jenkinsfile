pipeline {
    agent any
    
    environment {
        project = 'pullbased'
        appName = 'pullbased'
        imageGroup = 'sharathdb'
        branchName = 'master'
        jenkinsURL = 'http://localhost:8080'
        registryURL = 'https://hub.docker.com/repository/docker/sharathdb/pullbased'
        sonarURL = 'http://localhost:9000'
        registryCredential = 'DOCKERHUB'
    }

    stages {
        stage('Build base docker image') {
            steps {
                script {
                    if (branchName ==~ '^master$') {
                        imageTag = "${imageGroup}/${appName}:${branchName}"
                    } else {
                        imageTag = "${imageGroup}/${appName}:${branchName}"
                    }
                    containerName = "${appName}.${branchName}.${env.BUILD_NUMBER}"

                    sh "docker build -f deploy/Dockerfile -t ${imageTag} ."
                }
            }
        }

        stage('Push To DockerHub') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('UNSTABLE') }
            }
            steps {
                script {
                    withDockerRegistry(credentialsId: registryCredential, url: registryURL) {
                        docker.image(imageTag).push()
                    }
                }
            }
        }
    }
}
