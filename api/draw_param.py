# ----------------------------------------------------------------------------------------------------
# モジュールフォルダのパスを追加
# ----------------------------------------------------------------------------------------------------
import os, sys
if os.path.basename(os.getcwd()) == 'HealthMileage':
	sys.path.append('api')
elif os.path.basename(os.getcwd()) == 'test':
	os.chdir('../../')
	sys.path.append('api')
elif os.path.basename(os.getcwd()) == 'api':
	os.chdir('../')
	sys.path.append('api')
else:
	exit()


# ----------------------------------------------------------------------------------------------------
# モジュールimport
# ----------------------------------------------------------------------------------------------------
from module.Health.HealthRunParam import HealthRunParam
from module.Main.MainParam import Param as MAINPARAM


if __name__ == '__main__':

	param = HealthRunParam()
	param.RunParam()

	print('Save Success : {}'.format(MAINPARAM.PARAM_FLG_IMG_PATH))
	print('Save Success : {}'.format(MAINPARAM.PARAM_STEP_IMG_PATH))
	print('Save Success : {}'.format(MAINPARAM.PARAM_SLEEP_IMG_PATH))

