from app.src.WebDriver import WebDriver
from app.src import ErrorLog
from app.src.Parameter import PARAM
from app.src.Parameter import XPATH


class HealthLogin:
	"""
	ログインの処理を実施するクラス

	Attributes
	----------
	web_driver : WebDriver
		ChromeのWebドライバ用のクラス
	"""

	def __init__(self, web_driver):

		self.web_driver = web_driver
	
	
	def __CheckEnableLogin(self):
		"""
		ログイン成功を確認する

		Returns
		----------
		is_success : boolean
			ログイン成功フラグ(True：成功、False：失敗)
		"""
		meta = self.web_driver.driver.find_element_by_xpath(XPATH.LOGIN_CHECK_DESC)
		if meta.get_attribute('content') == XPATH.LOGIN_CHECK_CONTENT:
			is_success = True
		else:
			is_success = False
		return is_success
	

	def Login(self, user_param):
		"""
		ログインを実施する

		Parameters
		----------
		user_param : dict
			メールアドレスとパスワード
		"""
		
		# サイトにアクセス
		self.web_driver.driver.get(PARAM.PEPUP_HOME_URL)
		self.web_driver.Sleep()
		
		# ログイン処理
		if not self.__CheckEnableLogin():
			self.web_driver.driver.find_element_by_xpath(XPATH.LOGIN_EMAIL).send_keys(user_param['Address'])
			self.web_driver.driver.find_element_by_xpath(XPATH.LOGIN_PSWD).send_keys(user_param['Password'])

			self.web_driver.driver.find_element_by_xpath(XPATH.LOGIN_COMMIT).click()
			self.web_driver.Sleep()

			# ログイン成功/失敗判定
			if not self.__CheckEnableLogin():
				ErrorLog.error_log_object.Resist('')
				ErrorLog.error_log_object.Resist('■ログイン情報')
				ErrorLog.error_log_object.Resist('　Pepupへのログインに失敗しました')
				ErrorLog.error_log_object.Resist('　メールアドレス、パスワードに誤りがあるかもしれません')
				ErrorLog.error_log_object.Resist('')
				ErrorLog.error_log_object.Resist('　また、「私はロボットではありません」のチェックボックスは突破できません')
				ErrorLog.error_log_object.Resist('　チェックボックスが出ている際は、一度手動でのチェックをお願いします')
