# ----------------------------------------------------------------------------------------------------
# モジュールimport
# ----------------------------------------------------------------------------------------------------
import datetime


# ----------------------------------------------------------------------------------------------------
# スケジュールのMainクラス
# ----------------------------------------------------------------------------------------------------
class Scheduler:

	def __init__(self, call_backs, event_period):
		
		# 周期処理のコールバック関数
		self.call_backs = call_backs
		# 周期時間
		self.event_period = datetime.timedelta(seconds=event_period)
		
		# ループ周期検知のため、前処理時の時間と現在の時間を保管する変数
		self.curr_date = datetime.datetime.now()
		self.prev_date = datetime.datetime.now() - self.event_period
		
	
	# ----------------------------------------------------------------------------------------------------
	# 周期処理
	# ----------------------------------------------------------------------------------------------------
	def Run(self):
		
		# 現在の時間を取得
		self.curr_date = datetime.datetime.now()
		
		# イベント周期のタイミングを検知
		if (self.curr_date - self.prev_date) >= self.event_period:
			# 周期処理
			for call_back in self.call_backs: call_back()
			# 前処理時の時間の更新
			self.prev_date = self.curr_date