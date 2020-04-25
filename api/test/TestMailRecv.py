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
from module.Mailler.MaillOrder import MaillOrder
from module.Mailler.MaillExtractor import MaillExtractor
from module.Mailler import MailUtility

from module.Mailler.MaillParam import Param as MAILPARAM


# ----------------------------------------------------------------------------------------------------
# テストコード
# ----------------------------------------------------------------------------------------------------
def TestMailRecv():
	
	mailer = MaillOrder()
	extractor = MaillExtractor(mailer)
	recv_list = extractor.ExtractRequestInfoList(unpublish_head_date=None)

	for recv in recv_list:
		print(recv)



if __name__ == '__main__':

	TestMailRecv()
	