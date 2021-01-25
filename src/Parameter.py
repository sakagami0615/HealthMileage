
class PARAM:
	# ----------------------------------------------------------------------------------------------------
	# URL
	# ----------------------------------------------------------------------------------------------------
	PEPUP_HOME_URL = 'https://pepup.life/users/sign_in'
	MILLAGE_URL = "https://pepup.life/scsk_mileage_campaigns"
	
	# ----------------------------------------------------------------------------------------------------
	# 自動入力関連
	# ----------------------------------------------------------------------------------------------------
	# 歩数入力
	STEP_MILEAGE_TYPE = {'Name': 'StepInput', 'Id': 4}
	# 睡眠入力
	SLEEP_MILEAGE_TYPE = {'Name': 'SleepInput', 'Id': 5}
	# チェック入力
	CHECK_MILEAGE_TYPES = [
		# 睡眠チェック
		{'Name': 'SleepCheck', 'Id': 6},
		# アルコールチェック
		{'Name': 'AlcoholCheck', 'Id': 7},
		# 食生活チェック
		{'Name': 'DietCheck', 'Id': 8},
		# その他のチェック
		{'Name': 'OtherCheck', 'Id': 9}
	]


class XPATH:
	# ----------------------------------------------------------------------------------------------------
	# ログイン関連
	# ----------------------------------------------------------------------------------------------------
	LOGIN_EMAIL			= "//input[@name='user[email]']"
	LOGIN_PSWD			= "//input[@name='user[password]']"
	LOGIN_COMMIT		= "//input[@name='commit']"
	LOGIN_CHECK_DESC	= "//html/head/meta[5]"
	LOGIN_CHECK_CONTENT	= "Pep Up（ペップアップ）"
	MILLAGE_ACCESS		= "//a[@href='/scsk_mileage_campaigns']"
	
	# ----------------------------------------------------------------------------------------------------
	# 月選択のプルダウン関連
	# ----------------------------------------------------------------------------------------------------
	MONTH_SELECT_BOX	= "//html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/select"

	# ----------------------------------------------------------------------------------------------------
	# divタグのインデックス
	# ----------------------------------------------------------------------------------------------------
	DIV_FIRST_INDEX = 4
	DIV_SECOND_INDEX = 3

	# ----------------------------------------------------------------------------------------------------
	# テキスト入力関連
	# ----------------------------------------------------------------------------------------------------
	INPUT_TEXTBOX		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/form/input"
	INPUT_CANCEL_BUTTON	= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/form/div/button[2]"
	INPUT_DONE_BUTTON	= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/form/div/button[1]"


	# ----------------------------------------------------------------------------------------------------
	# チェック入力関連
	# ----------------------------------------------------------------------------------------------------
	CHECK_ATTRIBUTE     = "checked"
	CHECK_CHECKLIST		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[3]/div"
	CHECK_CHECKBOX		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[3]/div[{}]/label/input"
	CHECK_CHECKTEXT		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[3]/div[{}]/label"
	CHECK_CLOSE_BUTTON	= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[3]/div[{}]/button"

	RADIO_ATTRIBUTE     = "checked"
	RADIO_TITLETEXT		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/div[2]"
	RADIO_CHECKLIST		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/form/div[1]"
	RADIO_CHECKBOX		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/form/div[1]/div[{}]/input"
	RADIO_CHECKTEXT		= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/form/div[1]/div[{}]/label"
	RADIO_RECORD_BUTTON	= "//html/body/div[" + str(DIV_FIRST_INDEX) + "]/div[" + str(DIV_SECOND_INDEX) + "]/div[2]/form/div[2]/button[1]"


	# ----------------------------------------------------------------------------------------------------
	# その他選択関連
	# ----------------------------------------------------------------------------------------------------
	MILLAGE_ACCESS		= "//a[@href='/scsk_mileage_campaigns']"
	MILLAGE_DAY_BUTTON	= "/html/body/div[1]/div/div[2]/div/div[2]/div/div[{}]/div[2]/div[1]/div[2]/div[2]/div[{}]/div[{}]/button"
