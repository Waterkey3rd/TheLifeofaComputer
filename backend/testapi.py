import os
import requests
import json
import logging

# --- 配置区 (请根据实际情况修改) ---
API_KEY = r"sdffdf"
BASE_URL = "https://mcp/v1" 
MODEL = "Doubao-1.5-Pro"
# ------------------------------

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_api_connection():
    print("🚀 开始 API 连通性测试...")
    print(f"🔗 Target URL: {BASE_URL}/chat/completions")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "Ping"}],
        "max_tokens": 5
    }

    try:
        # 使用 requests 直接测试，跳过 SDK 封装以便查看原始报文
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        print(f"\n📥 [Response Status]: {response.status_code}")
        
        # 检查是否被 Cloudflare 拦截 (通常返回 HTML)
        content_type = response.headers.get("Content-Type", "")
        print(f"🏷️ [Content-Type]: {content_type}")

        if "text/html" in content_type:
            print("❌ 错误: 收到 HTML 响应！这通常意味着 Cloudflare 拦截了请求。")
            if "CF-RAY" in response.headers:
                print(f"🆔 CF-RAY ID: {response.headers['CF-RAY']}")
            print("--- 响应前100个字符 ---")
            print(response.text[:100])
            print("-----------------------")
            
        elif "application/json" in content_type:
            try:
                data = response.json()
                if response.status_code == 200:
                    print("✅ 成功! API 响应正常。")
                    print(f"🤖 AI Response: {data['choices'][0]['message']['content']}")
                else:
                    print("⚠️ API 返回了错误 JSON:")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
            except Exception:
                print("❌ 无法解析 JSON 响应内容。")
        else:
            print(f"❓ 未知响应格式: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"🚨 网络请求发生异常: {e}")

if __name__ == "__main__":
    test_api_connection()