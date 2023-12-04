#!groovy
  // push to staging
  project = 'pullbased'
  appName = 'pullbased'
  imageGroup = 'sharathdb'
 
  //fix branch name to be compatable with docker
  branchName = 'master'
 
  jenkinsURL = "http://localhost:8080"
  registryURL = "https://hub.docker.com/repository/docker"
  //sonarURL = "http://localhost:9000"
  registryCredential = 'DOCKERHUB'
 
  buildInfo = "Build of ${project} branch ${branchName} (build number  ${env.BUILD_NUMBER})"
  buildLink = "${jenkinsURL}/job/${project}/job/${branchName}/"
 
  //imageTag = "${registryURL}/${imageGroup}/${appName}:${branchName}.${env.BUILD_NUMBER}"
  //productionLatestTag = "${registryURL}/${imageGroup}/${appName}:latest"
  //stagingLatestTag = "${registryURL}/${imageGroup}/${appName}:staging"
  //uatLatestTag = "${registryURL}/${imageGroup}/${appName}:uat"
  //devLatestTag = "${registryURL}/${imageGroup}/${appName}:dev"
 
  isSprintBranch  = branchName ==~ "^staging\$"
  isDevBranch  = branchName ==~ "^develop\$"
  isUatBranch = branchName ==~ "^uat\$"
  isProductionBranch = branchName ==~ "^master\$"
 
  if ("${branchName}" == "production") {
      imageTag = "${imageGroup}/${appName}:${branchName}.${env.BUILD_NUMBER}"
  } else {
      imageTag = "${imageGroup}/${appName}:${branchName}"
  }
 
  containerName = "${appName}.${branchName}.${env.BUILD_NUMBER}"
  //composeProject = "${project}${branchName}${env.BUILD_NUMBER}".replaceAll("-","").replaceAll("_","").replaceAll("\\W","")
 
node {
    checkout scm
 
    stage ('Build base docker image') {
        script {
            sh("docker build -f deploy/Dockerfile -t ${imageTag} .")
        }
            
    }

    stage('Push To DockerHub') {
        script {
            docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                    docker.image("${imageTag}").push()
                }
        }
                
    }
}