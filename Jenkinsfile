#!groovy
  // push to staging
  project = 'pullbased'
  appName = 'pullbased'
  imageGroup = 'sugarbox'
 
  //fix branch name to be compatable with docker
  branchName = env.BRANCH_NAME.toLowerCase().replaceAll("/","-")
 
  jenkinsURL = "http://ci.sboxdc.com"
  registryURL = "registry.sboxdc.com"
  sonarURL = "https://sonar.sboxdc.com"
 
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

    stage ('Initilize Unit Test Env') {
        try {
            //Run test env with build option
            sh("docker-compose -f docker-compose.test.yml -p ${composeProject} up -d --build")
            // wait for test environment to come online
            sh("sleep 30s")
        } catch (e) {
            failLogging()
            cleanEnvironment()
            throw e
        }
    }

    stage ('Run Unit Tests'){
        try {
            // Run Unit tests
            sh("docker-compose -f docker-compose.test.yml -p ${composeProject} exec -T pullbased python3 -m pytest")
        } catch (e) {
            sh("docker-compose -f docker-compose.test.yml -p ${composeProject} exec -T pullbased cat /var/log/sugarbox/pullbased/application.log")
            sh("docker-compose -f docker-compose.test.yml -p ${composeProject} logs")
            failLogging()
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