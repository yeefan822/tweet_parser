import requests
from bs4 import BeautifulSoup
import webbrowser
import time

BASE_URL = 'https://blood-records.co.uk'
TARGET_URL = f"{BASE_URL}/collections/all"
KEYWORDS = ["ariana"]

def find_matching_product():
    resp = requests.get(TARGET_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    slides = soup.select("div.slideshow__slide a")
    for slide in slides:
        href = slide.get("href", "")
        full_url = BASE_URL + href
        for kw in KEYWORDS:
            if kw.lower() in href.lower():
                print(f"🎯 发现匹配商品：{full_url}")
                webbrowser.open(full_url)  # 自动打开页面
                return full_url
    print("❌ 没有找到匹配商品")
    return None

def monitor(interval=10):
    print("开始监控 Blood Records 新品...")
    last_hit = None
    while True:
        try:
            result = find_matching_product()
            if result and result != last_hit:
                last_hit = result
        except Exception as e:
            print(f'发生错误：{e}')
        time.sleep(interval)