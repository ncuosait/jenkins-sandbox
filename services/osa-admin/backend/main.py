from fastapi import FastAPI

app = FastAPI()

# 不同的版本號與服務名稱
VERSION = "1.0.0-shadow-admin"

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "osa-admin-backend", 
        "version": VERSION
    }

@app.get("/api/stats")  # 模擬管理端特有的 API
def get_admin_stats():
    return {
        "source": "NCU OSA Admin System",
        "total_users": 1250,
        "server_load": "low",
        "system_version": VERSION
    }