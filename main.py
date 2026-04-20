import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def run():
    url = "https://www.maff.go.jp/j/seisan/ryutu/yasai/otokuyasai.html"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. テキスト情報の抽出
    # main_content配下をまるごと取得し、改行で区切ってリスト化します
    main_content = soup.find("div", id="main_content")
    
    # 全テキストを取得し、お買い得という文字が含まれる行だけを抽出・整形
    lines = main_content.get_text(separator="\n").splitlines()
    veggie_list = []
    
    for line in lines:
        clean_line = line.strip()
        # 「お買い得」というキーワードが含まれる行をピックアップ
        if "お買い得" in clean_line:
            # 前後の行（野菜名など）が分離している場合があるため、
            # 「今週は」から始まる文や、特定のフレーズを補足するロジック
            veggie_list.append(clean_line)

    # 重複を削除しつつ、見やすく結合
    # (農水省のサイト構造上、同じ文言が複数回ヒットすることがあるため)
    unique_veggies = []
    for v in veggie_list:
        if v not in unique_veggies:
            unique_veggies.append(v)
    
    veggie_msg = "\n".join(unique_veggies)

    # 2. テーブル画像の取得（前回同様）
    img_tag = soup.find("img", alt=lambda x: x and "価格表" in x)
    img_url = urljoin(url, img_tag["src"]) if img_tag else None

    # 3. Discordに送信
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        # メッセージ本文を構成
        # もしテキスト抽出に失敗したときのために、デフォルト文を用意
        display_text = veggie_msg if veggie_msg else "今週のお買い得野菜が更新されました！"
        
        content = f"**【農林水産省：今週のお手頃野菜】**\n\n{display_text}\n\n詳細はコチラ: {url}"
        
        payload = {"content": content}
        
        if img_url:
            img_data = requests.get(img_url).content
            files = {"file": ("table.jpg", img_data)}
            requests.post(webhook_url, data=payload, files=files)
        else:
            requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    run()