# discord_security_check
AWS SecurityHubの検出結果をDiscordに通知します

【discord側の準備】<br>
+ [公式ドキュメント](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)を参考にWebhookURLを作成します。

【AWS側の準備】<br>
+ Lambda関数：discord_security_check_lambda.py<br>
   - web_hookのurlは置き換えてください。<br>
   - Lambda実行ロールはAWSマネージドの**AWSLambdaBasicExecutionRole**と**securityhub:BatchUpdateFindings**があれば動作します。<br>
+ EventBridgeルール：discord_security_check_event.json<br>
+ SecurityHubサンプル結果：security_check_sample.json<br>
   - Test実行するときのイベントとして利用できます。<br>

## 出力イメージ
![出力イメージ](image.jpg)
