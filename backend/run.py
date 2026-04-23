import uvicorn

if __name__ == "__main__":
    print("🚀 正在启动服务器 (支持局域网访问)...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
