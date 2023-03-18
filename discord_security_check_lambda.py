import logging
import json
import urllib
import boto3
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
def lambda_handler(event, context):
    try:
        print(event)
        messages = parse_event(event)
        result_update(event)
        web_hook(messages)
        return {
            'statusCode': 200,
            'body': 'Success Sending Discord'
        }
    except Exception as e:
        logger.exception(e)
        raise e
 
# webhookでDiscordに送信
def web_hook(messages):
    url = "https://discord.com/api/webhooks/XXXXXX"
    method = "POST"
    headers = {"Content-Type" : "application/json"}
    obj = {"content" : messages}
    json_data = json.dumps(obj).encode("utf-8")
    request = urllib.request.Request(
        url,
        json_data,
        {"User-Agent": "curl/7.64.1", "Content-Type" : "application/json"},
        method
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)

### 対象の検出項目のワークフローステータスをNOTIFIEDにする
def result_update(event):
    client = boto3.client('securityhub')
    response = client.batch_update_findings(
        FindingIdentifiers=[
            {
                'Id': event['detail']['findings'][0]['Id'],
                'ProductArn': event['detail']['findings'][0]['ProductArn']
            },
        ],
        Note={
            'Text': event['time']+'に通知済み',
            'UpdatedBy': 'discord_security_check_lambda'
        },
        Workflow={
            'Status': 'NOTIFIED'
        }
    )
    logger.info('Success Update Finding!')

### イベントからDiscordメッセージを整形
def parse_event(event):

    time = event['time']
    region = event['region']

    account = event['detail']['findings'][0]['AwsAccountId']
    description = event['detail']['findings'][0]['Description']
    title = event['detail']['findings'][0]['Title']
    findings_id = event['detail']['findings'][0]['Id']
    label = event['detail']['findings'][0]['Severity']['Label']
 
    message = f"""
    :warning: **SecurityHubのエラー通知です** :warning:\r
    【検出結果】
    ＜基本情報＞
    ▼Account ID : {account}
    ▼検知時刻 : {time}
    ▼リージョン: {region}
    
    ＜詳細情報＞
    ▼検出項目： {title}
    ▼検出内容 : {description}
    ▼検索ID : {findings_id}
    ▼重要度 : {label}
    """
    logger.info('Success Creating Discord Messages!')
 
    return message
