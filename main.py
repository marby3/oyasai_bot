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

    # 1. 更新日を含んだタイトルを取得 (例: 今週のお手頃野菜(令和8年4月17日更新))
    title_element = soup.find("h1")
    if not title_element:
        return
    current_title = title_element.get_text(strip=True)

    # 2. 前回保存した日付と比較
    last_date_file = "last_date.txt"
    if os.path.exists(last_date_file):
        with open(last_date_file, "r", encoding="utf-8") as f:
            last_title = f.read().strip()
    else:
        last_title = ""

    if current_title == last_title:
        print(f"更新なし: {current_title}")
        return # 更新がなければここで終了

    # 3. テキスト情報の抽出
    main_content = soup.find("div", id="main_content")
    full_text = main_content.get_text(separator=" ", strip=True)
    pattern = r"(今週は.*?となっております！)"
    matches = re.findall(pattern, full_text)
    
    if matches:
        veggie_msg = "\n".join(matches)
        veggie_msg = re.sub(r' +', ' ', veggie_msg)
        veggie_msg = veggie_msg.replace("！ ", "！\n")
    else:
        veggie_msg = "今週のお買い得野菜の情報が更新されました。"

    # 4. テーブル画像の取得
    img_tag = soup.find("img", alt=lambda x: x and "価格表" in x)
    img_url = urljoin(url, img_tag["src"]) if img_tag else None

    # 5. Discordに送信
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        content = (
            f"**【農林水産省：今週のお手頃野菜】**\n\n"
            f"{veggie_msg}\n\n"
            f"詳細はコチラ: {url}"
        )
        payload = {"content": content}
        
        if img_url:
            img_data = requests.get(img_url).content
            files = {"file": ("table.jpg", img_data)}
            requests.post(webhook_url, data=payload, files=files)
        else:
            requests.post(webhook_url, json=payload)

        # 6. 送信に成功したら、今回のタイトルをファイルに保存
        with open(last_date_file, "w", encoding="utf-8") as f:
            f.write(current_title)
        print(f"通知を送信しました: {current_title}")

if __name__ == "__main__":
    run()