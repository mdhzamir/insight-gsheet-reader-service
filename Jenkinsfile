pipeline {

    agent any
    
    environment {
        REGISTRY = "203.188.245.212:7800"
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker run --rm -v /root/dashboard-work/jenkins-data/workspace/$JOB_NAME:/app -v /root/.m2/:/root/.m2/ -w /app maven:3-alpine mvn clean package -B -Dactive.profile=docker -Dmaven.test.skip=true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $REGISTRY/$JOB_NAME:$BUILD_NUMBER .'
            }
        }
        stage('Push') {
            steps {
                sh 'docker push $REGISTRY/$JOB_NAME:$BUILD_NUMBER'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                echo $BUILD_NUMBER
                cat ./deploy/gsheetservice.tm | sed 's/IMAGE/'$JOB_NAME'/'| sed 's/TAG/'$BUILD_NUMBER'/' > ./deploy/gsheetservice.yml
                cat ./deploy/publish.tm | sed 's/IMAGE/'$JOB_NAME'/' > ./deploy/publish
                cat ./deploy/gsheetservice.yml      
                cat ./deploy/publish
                ssh -i /opt/private-rsa root@192.168.152.137 "mkdir -p /tmp/$JOB_NAME/"
                scp -ri /opt/private-rsa ./deploy/ root@192.168.152.137:/tmp/$JOB_NAME/
                ssh -i /opt/private-rsa root@192.168.152.137 "chmod -R +x /tmp/$JOB_NAME"
                ssh -i /opt/private-rsa root@192.168.152.137 "/tmp/$JOB_NAME/deploy/publish"
                '''
            }
        }

    }
}
