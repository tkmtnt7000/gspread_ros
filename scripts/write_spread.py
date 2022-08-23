import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pprint

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
json_keyfile_path = '/home/tsukamoto/.config/gspread/service_account.json'

# サービスアカウントキーを読み込む
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_keyfile_path, scope)

# pydrive用にOAuth認証を行う
gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

folder_id = '1d8mzn6uICQ-cScsnZ0uhEVgsOXD1vsd_'
f = drive.CreateFile({
    'title': 'sample_spread',
    'mimeType': 'application/vnd.google-apps.spreadsheet',
    "parents": [{"id": folder_id}]})
f.Upload()

# 作成したスプレッドシートの情報を出力
pprint.pprint(f)

# gspread用に認証
gc = gspread.authorize(credentials)

# スプレッドシートのIDを指定してワークブックを選択
workbook = gc.open_by_key(f['id'])
worksheet = workbook.sheet1

# A1のセルに入力
worksheet.update_acell('A1', 'Hello World!')

# 2行目の1~3列目に入力
cell_list = worksheet.range(2, 1, 2, 3)
cell_list[0].value = '連番'
cell_list[1].value = '名前'
cell_list[2].value = '電話番号'

# スプレッドシートを更新
worksheet.update_cells(cell_list)
