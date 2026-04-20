import os
import requests
from bs4 import BeautifulSoup

def check_vegetables():
    # 1. ページ情報の取得
    url = "https://www.maff.go.jp/j/seisan/ryutu/yasai/otokuyasai.html"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    # 2. データの抽出
    title_text = soup.find("h1").get_text(strip=True)
    main_content = soup.find("div", id="main_content")
    paragraphs = main_content.find_all("p")
    
    veggie_msg = ""
    for p in paragraphs:
        text = p.get_text(strip=True)
        if "お買い得" in text:
            veggie_msg += text + "\n"

    # 3. メッセージ作成
    content = f"**【農林水産省：今週のお手頃野菜】**\n{title_text}\n\n{veggie_msg}\n詳細はコチラ: {url}"

    # 4. Discordに送信（環境変数からWebhook URLを取得）
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        requests.post(webhook_url, json={"content": content})

if __name__ == "__main__":
    check_vegetables()