pipeline {
    agent any
    
    environment {
        project = 'pullbased'
        appName = 'pullbased'
        imageGroup = 'sharathdb'
        branchName = 'master'
        jenkinsURL = 'http://localhost:8080'
        registryURL = 'https://registry.hub.docker.com'
        sonarURL = 'http://localhost:9000'
        registryCredential = 'DOCKERHUB'
    }

    stages {
        stage('Build base docker image') {
            steps {
                script {
                    if (branchName ==~ '^master$') {
                        imageTag = "${imageGroup}/${appName}:${branchName}.${env.BUILD_NUMBER}"
                    } else {
                        imageTag = "${imageGroup}/${appName}:${branchName}"
                    }
                    containerName = "${appName}.${branchName}.${env.BUILD_NUMBER}"

                    sh "docker build -f deploy/Dockerfile -t ${imageTag} ."
                }
            }
        }

        stage('Push To DockerHub') {
            steps {
                script {
                    withDockerRegistry(credentialsId: registryCredential, url: 'https://registry.hub.docker.com') {
                        docker.image(imageTag).push()
                    }
                }
            }
        }
    }
}
