import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def run():
    url = "https://www.maff.go.jp/j/seisan/ryutu/yasai/otokuyasai.html"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. テキスト情報の抽出
    main_content = soup.find("div", id="main_content")
    
    # タグの間にスペースを入れて全テキストを取得（野菜名の分離を防ぐ）
    full_text = main_content.get_text(separator=" ", strip=True)
    
    # 正規表現で「今週は」〜「お買い得となっております！」の範囲を抽出
    # ※「大変お買い得」と「もお買い得」の2文が含まれるようにします
    pattern = r"(今週は.*?となっております！)"
    matches = re.findall(pattern, full_text)
    
    if matches:
        # 抽出した文を結合し、余分な空白を詰めて読みやすく整形
        veggie_msg = "\n".join(matches)
        veggie_msg = re.sub(r' +', ' ', veggie_msg) # 連続するスペースを1つに
        veggie_msg = veggie_msg.replace("！ ", "！\n") # 句切れで改行
    else:
        veggie_msg = "今週のお買い得野菜の情報が見つかりました。"

    # 2. テーブル画像の取得
    img_tag = soup.find("img", alt=lambda x: x and "価格表" in x)
    img_url = urljoin(url, img_tag["src"]) if img_tag else None

    # 3. Discordに送信
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        # メッセージの組み立て
        content = (
            f"**【農林水産省：今週のお手頃野菜】**\n\n"
            f"{veggie_msg}\n\n"
            f"詳細はコチラ: {url}"
        )
        
        payload = {"content": content}
        
        if img_url:
            img_data = requests.get(img_url).content
            files = {"file": ("table.jpg", img_data)}
            # テキストと画像を同時に送信
            requests.post(webhook_url, data=payload, files=files)
        else:
            requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    run()