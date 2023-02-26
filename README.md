# discord_security_check
AWS SecurityHubの検出結果をDiscordに通知します

（README作成中）

【discord】<br>
webhookURLを作成します

【AWS】<br>
Lambda関数：discord_security_check_lambda.py<br>
　→web_hookのurlは置き換えてください。<br>
EventBridgeルール：discord_security_check_event.json<br>
SecurityHubサンプル結果：security_check_sample.json<br>

## 出力イメージ
![出力イメージ](image.jpg)
