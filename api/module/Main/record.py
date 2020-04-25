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
from module.Health.HealthRunRecord import HealthRunRecord
from module.Mailler import MailUtility

from module.Main.MainParam import Param as MAINPARAM


# ----------------------------------------------------------------------------------------------------
# run function
# ----------------------------------------------------------------------------------------------------
def Run():

	try:
		record = HealthRunRecord()
		(is_success, ack_msg) = record.RunRecord()
		ack = MailUtility.OrganizeAckinfo('record', is_success, ack_msg)
		
		MainUtility.DrawAck(ack)

	except Exception:
		MainUtility.DrawException()
		MainUtility.LoggingException()
