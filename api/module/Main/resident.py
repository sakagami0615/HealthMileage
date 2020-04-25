# ----------------------------------------------------------------------------------------------------
# モジュールフォルダのパスを追加
# ----------------------------------------------------------------------------------------------------
import os, sys
if sys.path.count('api/module') == 0:
	if os.path.basename(os.getcwd()) == 'HealthMileage':
		sys.path.append('api/module')
	elif os.path.basename(os.getcwd()) == 'api':
		os.chdir('../')
		sys.path.append('api/module')
	else:
		exit()


# ----------------------------------------------------------------------------------------------------
# モジュールimport
# ----------------------------------------------------------------------------------------------------
from module.Main import MainUtility
from module.Scheduler.Scheduler import Scheduler
from module.Mailler.MaillOrder import MaillOrder
from module.Mailler.MaillExtractor import MaillExtractor
from module.Request.Request import Request

from module.Main.MainParam import Param as MAINPARAM


# ----------------------------------------------------------------------------------------------------
# 本アプリの処理
# ----------------------------------------------------------------------------------------------------
def MainProcess():

	maill_order = MaillOrder()
	request = Request(maill_order)
	maill_extractor = MaillExtractor(maill_order)

	unpublish_head_date = request.LoadUnpublishMailHeadDate()
	req_info_list = maill_extractor.ExtractRequestInfoList(unpublish_head_date)

	request.RunRequest(req_info_list)

	request.SaveUnpublishMailHeadDate(req_info_list)



# ----------------------------------------------------------------------------------------------------
# run function
# ----------------------------------------------------------------------------------------------------
def Run():

	try:	
		# スケジューラクラス生成
		main_schedule = Scheduler([MainProcess], MAINPARAM.MAIN_LOOP_PERIOD_SEC)
		draw_schedule = Scheduler([MainUtility.DrawProcessNow], MAINPARAM.DRAW_LOOP_PERIOD_SEC)
		
		# ループ処理
		while True:
			main_schedule.Run()
			draw_schedule.Run()
			
	# ユーザ終了要求（Ctrl-Cを検知）
	except KeyboardInterrupt:
		pass

	# 不正動作による終了
	except Exception:
		MainUtility.DrawException()
		MainUtility.LoggingException()
