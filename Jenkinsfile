#!groovy
  // push to staging
  project = 'pullbased'
  appName = 'pullbased'
  imageGroup = 'sharathdb'
 
  //fix branch name to be compatable with docker
  branchName = 'master'
 
  jenkinsURL = "http://localhost:8080"
  registryURL = "https://hub.docker.com/repository/docker"
  sonarURL = "http://localhost:9000"
 
  buildInfo = "Build of ${project} branch ${branchName} (build number  ${env.BUILD_NUMBER})"
  buildLink = "${jenkinsURL}/job/${project}/job/${branchName}/"
 
  //imageTag = "${registryURL}/${imageGroup}/${appName}:${branchName}.${env.BUILD_NUMBER}"
  productionLatestTag = "${registryURL}/${imageGroup}/${appName}:latest"
  stagingLatestTag = "${registryURL}/${imageGroup}/${appName}:staging"
  uatLatestTag = "${registryURL}/${imageGroup}/${appName}:uat"
  devLatestTag = "${registryURL}/${imageGroup}/${appName}:dev"
 
  isSprintBranch  = branchName ==~ "^staging\$"
  isDevBranch  = branchName ==~ "^develop\$"
  isUatBranch = branchName ==~ "^uat\$"
  isProductionBranch = branchName ==~ "^master\$"
 
  if ("${branchName}" == "production") {
      imageTag = "${registryURL}/${imageGroup}/${appName}:${branchName}.${env.BUILD_NUMBER}"
  } else {
      imageTag = "${registryURL}/${imageGroup}/${appName}:${branchName}"
  }
 
  containerName = "${appName}.${branchName}.${env.BUILD_NUMBER}"
  composeProject = "${project}${branchName}${env.BUILD_NUMBER}".replaceAll("-","").replaceAll("_","").replaceAll("\\W","")
 
  def cleanEnvironment(){
      sh("docker rmi -f ${imageTag}")
      sh("docker-compose -f docker-compose.test.yml down")
      sh("docker-compose -f docker-compose.test.yml down --rmi local -v")
      sh("docker-compose -f docker-compose.test.yml -p ${composeProject} stop")
      sh("docker-compose -f docker-compose.test.yml -p ${composeProject} down --rmi local -v")
      cleanWs()
  }
 
  def cleanUpPreTestImage(){
      sh("docker rmi -f ${imageTag}")
  }
 
  def cleanUpContainer(){
      sh("docker stop ${containerName}")
      sh("docker rm ${containerName}")
  }
 
  def failLogging(){
      sh("docker images")
      sh("df -i")
  }

 
node {
    checkout scm
 
    stage ('Build base docker image') {
        try {
            sh("docker build -f deploy/Dockerfile -t ${imageTag} .")
        } catch (e) {
            cleanUpPreTestImage()
            cleanEnvironment()
        	throw e
        }
    }
 
    stage("Code Analysis"){
        try {
          //Define Sonar Scanner Tool
          //def sonarqubeScannerHome = tool name: 'Sonar', type: 'hudson.plugins.sonar.SonarInstallation'
          withSonarQubeEnv('sonar') {
              def sonarqubeScannerHome = tool name: 'sonar', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
              sh ("cd app && ${sonarqubeScannerHome}/bin/sonar-scanner -e -X -Dsonar.host.url=${sonarURL} -Dsonar.branch=${branchName} || echo 0")
          }
      } catch (e) {
          failLogging()
          cleanEnvironment()
          throw e
      }
    }

    stage ('Clean up Testing Environment'){
          cleanEnvironment()
    }
}