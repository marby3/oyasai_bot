import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def run():
    url = "https://www.maff.go.jp/j/seisan/ryutu/yasai/otokuyasai.html"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. テキスト情報の抽出（「今週は～」の部分）
    main_content = soup.find("div", id="main_content")
    paragraphs = main_content.find_all("p")
    
    veggie_msg = ""
    for p in paragraphs:
        text = p.get_text(strip=True)
        if "お買い得" in text:
            veggie_msg += text + "\n"

    # 2. テーブル画像（imgタグ）のURLを取得
    # alt属性に「価格表」という文字が含まれる画像を探すのが最も確実です
    img_tag = soup.find("img", alt=lambda x: x and "価格表" in x)
    
    img_url = None
    if img_tag:
        # 相対パスを絶対パスに変換 (例: /img/table.jpg -> https://www.maff.go.jp/.../table.jpg)
        img_url = urljoin(url, img_tag["src"])

    # 3. Discordに送信
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        payload = {
            "content": f"**【農林水産省：今週のお手頃野菜】**\n\n{veggie_msg}\n詳細はコチラ: {url}"
        }
        
        if img_url:
            # 画像を一度ダウンロードして送信
            img_data = requests.get(img_url).content
            files = {"file": ("table.jpg", img_data)}
            requests.post(webhook_url, data=payload, files=files)
        else:
            # 画像が見つからなかった場合はテキストのみ送信
            requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    run()