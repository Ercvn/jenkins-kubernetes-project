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
        
        stage('GitOps - YAML Guncelle') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-auth', passwordVariable: 'GIT_TOKEN', usernameVariable: 'GIT_USERNAME')]) {
                    sh '''
                    # 1. Jenkins'in kendini Git'e tanıtması
                    git config user.name "Jenkins GitOps"
                    git config user.email "jenkins@local.com"

                    # 2. k8s/python-app.yaml içindeki eski imaj versiyonunu yeni Build Numarası ile değiştir
                    sed -i "s|image: ercvn/python-k8s-app:.*|image: ercvn/python-k8s-app:${BUILD_NUMBER}|g" k8s/python-app.yaml

                    # 3. Değişiklikleri onayla
                    git add k8s/python-app.yaml
                    git commit -m "CD: İmaj versiyonu ${BUILD_NUMBER} olarak güncellendi"

                    # 4. GitHub'a geri yolla 
                    git push https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/ercvn/jenkins-kubernetes-project.git HEAD:main
                    '''
                }
            }
        }
    }
}