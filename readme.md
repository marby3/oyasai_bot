# oyasai_botとは

農林水産省の[今週のお手頃野菜](https://www.maff.go.jp/j/seisan/ryutu/yasai/otokuyasai.html)のページをスクレイピングし、更新があった時にDiscordのチャンネルに投稿するbotです。

※細かい使用方法はいい感じに使ってください。

# Discordへの登録方法
## Discord編

最初に、Discord Webhookを有効にします。
特定のチャンネルにてチャンネルの編集から、連携サービスを選ぶことでwebhookのURLが取得できます。
このDicord webhookは保存しておいてください。

## Github編
### Webhookの登録
このリポジトリをクローンしてください。
その後、画面上部の「Settings」から、「Secrets and variables」>「Actions」を選び、「New repository secret」を選ぶことで、入力画面が出ます。
このNameには「DISCORD_WEBHOOK_URL」と、SecretにはDiscord編にて取得したDicord webhookを記載してください。

### Actionsの実行
画面上部の「Actions」から、「New workflow」を選びます。
その後、「set up a workflow Yourself」をクリックし、以下のコードを貼り付けて「Commit Changes」をしてください。

## 完了！
その他の細かい操作はいい感じにやってください。