pipeline {
    agent any
    environment {
        PROJECT_NAME = "osa-shadow-system"
        DEPLOY_PORT = "8081"
    }
    stages {
        stage('Step 1: 準備與檢查環境') {
            steps {
                echo "--- 正在初始化部署任務 ---"
                sh "docker version"
                sh "docker-compose version" // 使用連字號
                sh "ls -R"
            }
        }
        stage('Step 2: 並行建置服務') {
            parallel {
                stage('Build Website') {
                    steps {
                        echo "正在建置前台系統..."
                        sh "docker-compose build website-backend website-frontend"
                    }
                }
                stage('Build Admin') {
                    steps {
                        echo "正在建置後台系統..."
                        sh "docker-compose build admin-backend admin-frontend"
                    }
                }
                stage('Build Crawler') {
                    steps {
                        echo "正在建置爬蟲服務..."
                        sh "docker-compose build crawler"
                    }
                }
            }
        }
        stage('Step 3: 部署至影子環境') {
            steps {
                echo "--- 正在啟動容器服務 ---"
                sh "docker-compose -p ${PROJECT_NAME} up -d --remove-orphans"
            }
        }
        stage('Step 4: 自動化健康檢查') {
            steps {
                echo "--- 等待服務啟動 ---"
                sleep 5
                script {
                    sh "curl -i http://localhost:${DEPLOY_PORT}/api/health"
                }
            }
        }
    }
    post {
        success {
            echo "🎉 部署成功！"
            sh "docker image prune -f"
        }
    }
}