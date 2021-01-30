VERSION = 'v1.0.2 α'

HISTORY_LOG_LIST = {
	'v1.0.0 α (2020/11/09)': [
		'・新規作成'
	],
	'v1.0.1 α (2020/11/17)': [
		'・歩数、睡眠時間ログが複数表示されるバグを修正',
		'・前回入力値を表示する[lastmsg]コマンドを無効化',
		'・アプリの変更履歴を表示する[history]コマンドを実装'
	],
	'v1.0.2 α (2021/01/24)': [
		'・ChromeのWebドライバの作成コードに不具合があったため改修',
		'・chromedriver-binaryのバージョンアップ対応'
	]
}

HOW_TO_USE_MESSAGE_LIST = [
	'【HOW TO USE】',
	'チャットで下記項目を送信することで自動入力を実施します',
	'',
	'■メールアドレス（入力必須）',
	'　Pepupのアドレス',
	'',
	'■パスワード（入力必須）',
	'　Pepupのパスワード',
	'',
	'■歩数（入力任意）',
	'　歩数の入力値を指定',
	'　【入力例】',
	'　　・歩数:8000',
	'　　・歩数:8000-10000',
	'',
	'■睡眠時間（入力任意）',
	'　睡眠時間の入力値を指定',
	'　【入力例】',
	'　　・睡眠時間:7.5',
	'　　・睡眠時間:6-7.5',
	'',
	'■チェックの有無（入力任意）',
	'　チェック項目の入力有無を指定',
	'　【入力例】',
	'　・チェック:あり',
	'　　　※全項目チェックする',
	'　・チェック:なし',
	'　　　※チェックをしない',
	'',
	'',
	'フォーマットを送るので、ご活用ください。',
	'また、チャットを送信する際、入力任意の内容を削除すると、その項目は入力されなくなります。睡眠時間の入力等が不要の方は適宜削除お願いします。',
]

CHEAT_COMMAND_MESSAGE_LIST = [
	'【CHEAT COMMAND】',
	'version：バージョンを表示',
	'initmsg：登録時に通知した使用方法等を再通知',
	'history：アプリの変更履歴を通知'
]

FORMAT_MESSAGE_LIST = [
	'【Format】',
	'メールアドレス:your_address_here',
	'パスワード:your_password_here',
	'歩数:8000-10000',
	'睡眠時間:6-7.5',
	'チェック:あり'
]

HOW_TO_USE_MESSAGE = '\n'.join(HOW_TO_USE_MESSAGE_LIST)
CHEAT_COMMAND_MESSAGE = '\n'.join(CHEAT_COMMAND_MESSAGE_LIST)
FORMAT_MESSAGE = '\n'.join(FORMAT_MESSAGE_LIST)


def CreateHistoryMessage(history_log_list):
	history_message_list = []
	history_message_list.append('<HISTORY>')
	
	for version in list(HISTORY_LOG_LIST.keys()):
		history_message_list.append('')
		history_message_list.append('■{}'.format(version))
		history_message_list.extend(history_log_list[version])	

	history_message = '\n'.join(history_message_list)
	return history_message
	
HISTORY_LOG_MESSAGE = CreateHistoryMessage(HISTORY_LOG_LIST)
