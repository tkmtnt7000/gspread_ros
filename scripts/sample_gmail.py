from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

import base64, email #デコード用
import dateutil.parser

#token.jsonを設定
tokenPath = "/home/tsukamoto/tmp/gspread/scripts/token.json"

#credentials.jsonを設定
credentialsPath = "/home/tsukamoto/tmp/gspread/scripts/credentials.json"


#メール本文のデコード
def decode(encoded):
   decoded = base64.urlsafe_b64decode(encoded).decode()
   return decoded


#初期化(from quickstart.py)
def gmail_init():
   creds = None
   # The file token.json stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists(tokenPath):
       creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               credentialsPath, SCOPES)
           creds = flow.run_local_server(port=0)
       # Save the credentials for the next run
       with open(tokenPath, 'w') as token:
           token.write(creds.to_json())
           
   service = build('gmail', 'v1', credentials=creds)
   return service


#ここからやりたい処理を書く
service = gmail_init()

#quickstart.pyと同じ処理にしてみた
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

if not labels:
   print('No labels found.')
else:
   print('Labels:')
   for label in labels:
       print(label['name'])

#メール本文の内容を配列で取得する関数
def gmail_get_messages_body(service, labelIdsValue):
   mailBody = []
   
   # メッセージの一覧を取得
   messages = service.users().messages()
   msg_list = messages.list(userId='me', labelIds=labelIdsValue).execute() 
   # msg_list = messages.list(userId='me', labelIds=labelIdsValue ,maxResults=456).execute() #最大値指定
   
   # 取得したメッセージの一覧を配列に格納
   for msg in msg_list['messages']:
       
       #メールの受信日時を取得
       date = gmail_get_messages_body_date(messages,msg)
       
       topid = msg['id']     
       msg = messages.get(userId='me', id=topid).execute()
       
       if(msg["payload"]["body"]["size"]!=0):
           mailBody.append(date+"<br>"+decode(msg["payload"]["body"]["data"]))
       else:
           #メールによっては"parts"属性の中に本文がある場合もある
           mailBody.append(date+"<br>"+decode(msg["payload"]["parts"][0]["body"]["data"]))

   return mailBody
   

#gmail_get_messages_body関数内で受信日時を取得する関数
def gmail_get_messages_body_date(messages,msg):
   msg_id = msg['id']
   m = messages.get(userId='me', id=msg_id, format='raw').execute()
   raw = base64.urlsafe_b64decode(m['raw'])
   
   # Emailを解析する
   eml = email.message_from_bytes(raw)
   
   date = dateutil.parser.parse(eml.get('Date')).strftime("%Y-%m-%d_%H-%M-%S")
   return date

#ラベルのIDやnameを表示する関数
def gmail_display_label(service):
   results = service.users().labels().list(userId='me').execute()
   labels = results.get('labels', [])

   if not labels:
       print('No labels found.')
   else:
       print('Labels:')
       for label in labels:
           print(label)

# gmail_display_label(service)
# print(gmail_get_messages_body(service, "Label_1473091227925440884"))


def get_gdrive_url(mail_body_list):
    print(mail_body_list)
    print("===================")
    for i in range(len(mail_body_list)):
        print(i)
        print(mail_body_list[i])
        gdrive_file_pair = [x for x in mail_body_list[i].splitlines() if ': https://drive.google.com' in x]
        print("gdrive_file_pair:")
        print(gdrive_file_pair)
        file_dict = {}
        for j in range(len(gdrive_file_pair)):
            gdrive_file_url = gdrive_file_pair[j].split(': ')
            tmp_dict = dict((gdrive_file_url, ))
            file_dict.update(tmp_dict)
            print(gdrive_file_url)
        print("file_dict:")
        print(file_dict)

        for k in file_dict:
            print(k)
        print("==============")
    return file_dict

mail_body_list = gmail_get_messages_body(service, "Label_1473091227925440884")
get_gdrive_url(mail_body_list)
