import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary


class WebDriver:
	"""
	ChromeのWebドライバ用のクラス

	Attributes
	----------
	driver : selenium.webdriver.chrome.webdriver.WebDriver
		ChromeのWebドライバ
	wait_sec : float
		Sleep用待機時間(秒)
	"""

	def __init__(self, wait_sec=0.5, is_hidden=True):

		if is_hidden:
			chrome_options = Options()
			chrome_options.add_argument('--headless')
			chrome_options.add_argument('--no-sandbox')
			chrome_options.add_argument('--disable-dev-shm-usage')
			
		else:
			chrome_options = Options()
		
		# Heroku環境用
		try:
			chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
			chrome_options.binary_location = chrome_bin
		except:
			pass
		
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.__wait_sec = wait_sec


	def __del__(self):

		self.driver.quit()
	
	
	def Sleep(self):
		"""
		あらかじめ指定した時間だけ待機する
		"""
		time.sleep(self.__wait_sec)
