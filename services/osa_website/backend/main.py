from fastapi import FastAPI

app = FastAPI()

# SRE 實務：加入版本號，方便 Jenkins 部署後驗證
VERSION = "1.0.0-shadow-website"

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "osa-website-backend", 
        "version": VERSION
    }

@app.get("/api/data")
def get_public_data():
    return {
        "source": "NCU OSA Website",
        "items": ["校園新聞", "獎助學金資訊", "學生社團活動"],
        "debug_info": "Connected via shadow-network"
    }