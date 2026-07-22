pipeline {
    agent any
    
    environment {
        // Bir önceki adımda Jenkins'e verdiğimiz şifrelerin ID'leri
        DOCKERHUB_CRED = credentials('dockerhub-cred')
        IMAGE_NAME = "ercvn/python-k8s-app" 
        TAG = "${env.BUILD_ID}"
    }

    stages {
        stage('1. Kodu Çek') {
            steps {
                checkout scm
            }
        }
        
        stage('2. Yeni İmaj Oluştur') {
            steps {
                // Hem spesifik versiyon numarasıyla hem de 'latest' olarak etiketliyoruz
                sh "docker build -t ${IMAGE_NAME}:${TAG} -t ${IMAGE_NAME}:latest ."
            }
        }
        
        stage('3. Docker Hub\'a Gönder') {
            steps {
                sh "echo \$DOCKERHUB_CRED_PSW | docker login -u \$DOCKERHUB_CRED_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}:${TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
        
        stage('4. Kubernetes\'e Dağıt (CD)') {
            steps {
                // Jenkins'e yüklediğimiz config dosyasını kullanarak K8s'e bağlanıyoruz
                withKubeConfig(credentialsId: 'k8s-config') {
                    sh "kubectl set image deployment/python-app-deployment python-app=${IMAGE_NAME}:${TAG}"
                }
            }
        }
    }
}