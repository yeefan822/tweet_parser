import requests
from bs4 import BeautifulSoup
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'https://blood-records.co.uk'
TARGET_URL = f"{BASE_URL}/collections/all"
KEYWORDS = ["kae", "chappell", "gaga", "ariana", "taylor", "gracie"]
EXCLUDE = ['sabrinacarpenter']

def is_excluded(text: str) -> bool:
    """判断是否命中排除项（不区分大小写）"""
    return any(ex.lower() in text.lower() for ex in EXCLUDE)

def find_matching_product():
    resp = requests.get(TARGET_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    slides = soup.select("div.slideshow__slide a")
    for slide in slides:
        href = slide.get("href", "")
        full_url = BASE_URL + href
        lower_href = href.lower()

        for kw in KEYWORDS:
            if kw.lower() in lower_href and not is_excluded(lower_href):
                print(f"🎯 发现匹配商品：{full_url}")
                check_add_to_cart(full_url)
                return full_url

    print("❌ 没有找到匹配商品")
    return None

def check_add_to_cart(url):
    # 替换为你自己的用户名（或用环境变量也可以）
    options = Options()
    options.add_argument(r"--user-data-dir=C:\Users\admin\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--profile-directory=Default")  # 可改为"Profile 1"等
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        # 等待并点击 "Add to cart"
        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to cart')]"))
        )
        print("🛒 加入购物车按钮已找到，点击中...")
        add_btn.click()

        # 等待跳转并出现 "CHECKOUT" 按钮
        checkout_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='checkout' and contains(text(), 'CHECKOUT')]"))
        )
        print("💳 结账按钮已出现，点击中...")
        checkout_btn.click()

    except Exception as e:
        print(f"❌ 操作失败: {e}")
    # driver.quit()

def print_matching_products():
    resp = requests.get(TARGET_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    slides = soup.select("div.slideshow__slide a")

    found = False
    for slide in slides:
        href = slide.get("href", "")
        full_url = BASE_URL + href
        lower_href = href.lower()

        img = slide.find("img")
        title_guess = ""
        if img:
            if img.get("alt"):
                title_guess = img["alt"]
            elif img.get("data-src"):
                title_guess = img["data-src"].split("/")[-1].split(".")[0]
            elif img.get("src"):
                title_guess = img["src"].split("/")[-1].split(".")[0]

        lower_title = title_guess.lower()

        for kw in KEYWORDS:
            if (kw.lower() in lower_href or kw.lower() in lower_title) and not (
                is_excluded(lower_href) or is_excluded(lower_title)
            ):
                print(f"🎯 找到匹配商品：{title_guess} - {full_url}")
                found = True

    if not found:
        print("❌ 没有找到匹配商品")

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