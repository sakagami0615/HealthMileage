# ----------------------------------------------------------------------------------------------------
# XPathのパラメータクラス
# ----------------------------------------------------------------------------------------------------
class XPath:

	# ----------------------------------------------------------------------------------------------------
	# ログイン関連
	# ----------------------------------------------------------------------------------------------------
	LOGIN_EMAIL			= "//input[@name='user[email]']"
	LOGIN_PSWD			= "//input[@name='user[password]']"
	LOGIN_COMMIT		= "//input[@name='commit']"
	LOGIN_CHECK_DESC	= "//html/head/meta[5]"
	LOGIN_CHECK_CONTENT	= "Pep Up（ペップアップ）"
	
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

	# ----------------------------------------------------------------------------------------------------
	# その他選択関連
	# ----------------------------------------------------------------------------------------------------
	MILLAGE_ACCESS		= "//a[@href='/scsk_mileage_campaigns']"
	MILLAGE_DAY_BUTTON	= "/html/body/div[1]/div/div[2]/div/div[2]/div/div[{}]/div[2]/div[1]/div[2]/div[2]/div[{}]/div[{}]/button"