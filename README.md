# Jenkins CI/CD Sandbox: OSA 官網系統自動化遷移實驗室

## 專案簡介

本專案是一個 **概念驗證 (Proof of Concept, PoC)** 沙盒，旨在模擬將現有的官網系統從 **GitHub Actions** 環境遷移至自主控管的 **Jenkins** 自動化伺服器。透過建立「影子專案」環境，在不影響正式生產環境的前提下，實踐 SRE（網站可靠性工程）中的自動化部署、資源優化與系統可觀測性。

## 實驗目的

1. **技術遷移驗證**：評估從 SaaS 型工具 (GitHub Actions) 遷移至 Self-hosted 工具 (Jenkins) 的技術難點與流程優化。
2. **實踐 Pipeline as Code**：透過 `Jenkinsfile` 管理複雜的多模組建置流程（Monorepo 管理）。
3. **資源調度優化**：利用高效能硬體資源（如多核心 CPU 與大容量 RAM）實現**並行建置 (Parallel Build)**，縮短 CI/CD 迴圈時間。
4. **強化系統可觀測性**：在部署流程中加入自動化健康檢查 (Health Checks)，確保服務交付的穩定性。

## 系統架構

本沙盒重現了生產環境的微服務拓撲，所有組件均容器化並透過獨立的 Docker 網路進行通訊：

- **反向代理 (Nginx)**：負責流量分發，區分前台 (Website) 與後台 (Admin) 路由。
- **前台系統 (OSA Website)**：包含 Vue 3 前端與 FastAPI 後端。
- **後台系統 (OSA Admin)**：包含 Vue 3 前端與 FastAPI 後端。
- **任務服務 (Crawler)**：模擬自動化資料爬取與背景處理任務。
- **自動化引擎 (Jenkins)**：採用 Docker-outside-of-Docker (DooD) 技術，直接驅動宿主機 Docker 引擎進行構建。

## 技術特點

- **增量與並行建置**：`Jenkinsfile` 內建並行階段，可同時處理不同模組的 Docker Image 構建。
- **環境一致性**：透過 `docker-compose` 確保開發、測試與模擬環境的配置完全同步。
- **自動化驗證**：部署後自動觸發 `curl` 腳本進行 API 健康檢查，實現自動化運維。
- **資源清理機制**：任務結束後自動回收虛擬鏡像 (Dangling Images)，維持伺服器磁碟空間健康。

## 專案結構

```text
jenkins-sandbox/
├── Jenkinsfile              # 自動化流水線定義 (核心邏輯)
├── docker-compose.yml       # 多容器環境定義
├── infra/
│   └── nginx.conf           # 流量轉發與路由配置
└── services/
    ├── osa-website/         # 前台系統模組 (BE/FE)
    ├── osa-admin/           # 後台管理模組 (BE/FE)
    └── osa-crawler/         # 爬蟲任務模組
```

## 未來演進

to be continue ...
