pipeline {
    // 定義在哪個節點執行，'any' 代表只要有空閒的 Agent 即可
    agent any

    environment {
        // 定義專案名稱，用於 docker-compose 的 project name (-p)
        PROJECT_NAME = "osa-shadow-system"
        // 模擬部署的連接埠（剛才 nginx 配置的 8081）
        DEPLOY_PORT = "8081"
    }

    stages {
        stage('Step 1: 準備與檢查環境') {
            steps {
                echo "--- 正在初始化部署任務 ---"
                sh "docker version"
                sh "docker-compose version"
                // 顯示當前工作目錄，確認代碼已拉取
                sh "ls -R"
            }
        }

        stage('Step 2: 並行建置服務 (Parallel Build)') {
            // 利用你的 64GB RAM 優勢，同時進行建置，縮短 CICD 時間
            parallel {
                stage('Build Website') {
                    steps {
                        echo "正在建置前台系統..."
                        // 僅構建與前台相關的服務
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
                // -d 背景執行, --remove-orphans 清理不在 compose 裡的舊容器
                sh "docker-compose -p ${PROJECT_NAME} up -d --remove-orphans"
            }
        }

        stage('Step 4: 自動化健康檢查 (SRE 核心技能)') {
            steps {
                echo "--- 等待服務啟動並進行 API 驗證 ---"
                // 稍等 5 秒讓 FastAPI 暖機
                sleep 5
                
                script {
                    // 檢查前台 API
                    def websiteStatus = sh(script: "curl -s http://localhost:${DEPLOY_PORT}/api/health", returnStatus: true)
                    if (websiteStatus == 0) {
                        echo "✅ 前台 API 連線正常"
                    } else {
                        error "❌ 前台 API 連線失敗！"
                    }

                    // 檢查後台 API (我們之前改過 Nginx 轉發，假設路徑是 /api/v1/health)
                    // 這裡的 curl 測試路徑要跟你的 nginx.conf 對應
                    sh "curl -i http://localhost:${DEPLOY_PORT}/api/health"
                }
            }
        }
    }

    post {
        success {
            echo "🎉 部署成功！請開啟瀏覽器瀏覽 http://localhost:${DEPLOY_PORT}"
            // 清理沒被標記的虛擬鏡像，釋放磁碟空間
            sh "docker image prune -f"
        }
        failure {
            echo "🚨 部署過程出現錯誤，請檢查上方階段 Log。"
        }
    }
}