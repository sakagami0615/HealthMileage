# **HealthMileage**

## **1. 概要**

健康入力アプリへの入力を支援します
- 現在の入力状況を確認する
- 事前に設定したパラメータに応じて自動入力する
<br>

※ 上記2点は、GMailを通じて実施することもできます
<br><br>

## **1. 注意事項**

今回の大まかなファイル構成は下記の通りです
- **api**: 本アプリのソースコード配置フォルダ
- **bat**: 実行ファイル配置フォルダ
- **userSetting**: ユーザ設定用ファイル配置フォルダ
- **log**: アプリのエラーログ等のデータ格納フォルダ

apiフォルダ内は必要がなければ内部を弄らないでください
<br><br>

## **2. 事前準備**

今回のソースを実行するために、下記ツールが必要になります
- Git
- Docker

※ Git、Dockerが無くても使えると思いますが、あった方が圧倒的に楽です
<br><br>

### **2.1 Git Install**

インストール方法は下記URLに記載してあります<br>
[ダウンロード]～[インストール方法]の手順を実施すればOKです<br>
https://eng-entrance.com/git-install

Git Bashを使用するのも良いと思いますが、<br>
TortoiseGit、Sourcetree等のGUIもあるので、自分にあったものを使いましょう！
<br><br>

### **2.2 Docker Install**

DockerはMacOS、Linux、Window Pro、Window Home等でインストール方法が異ります<br>
今回は、ターゲット層が多そうなWindow Homeのインストール方法を取り上げます<br>
(Window HomeでDockerを使用する場合は、Docker Toolboxを使用します)<br>

インストール方法は下記URLに記載してあります<br>
[CPU仮想化を有効にする]～[インストール]の手順を実施すればOKです<br>
https://qiita.com/KIYS/items/8ac37f6757a6b7f84569
<br><br>

## **3. 導入手順**

導入手順は下記の通りです
+ GitでHealthMileageリポジトリをクローンする
+ userSetting内のユーザパラメータファイルを記載する
+ Googleアカウントの設定で「安全性の低いアプリのアクセス」を有効にする
<br><br>

### **3.1 GitでHealthMileageリポジトリをクローン**

下記リポジトリをクローンする<br>
https://github.com/sakagami0615/HealthMileage

※クローンの方法等は各自調べてください
<br><br>


### **3.2 ユーザパラメータファイルを記載**

UserFile_templateフォルダにフォーマットがあるので<br>
記載した後、UserFileにファイルをコピーしてください

- **parameter/HealthParam_InputFlg.json**

	<p>各項目に対する自動入力の有効/無効を管理するパラメータ<br>
	以下のパラメータを曜日ごとに指定する(有効：1 or 無効：0)<br>

	- StepInput    ：歩数値入力の有効フラグ
	- SleepInput   ：睡眠値入力の有効フラグ
	- SleepCheck   ：睡眠チェックの有効フラグ
	- AlcoholCheck ：アルコールチェックの有効フラグ
	- DietCheck    ：食生活チェックの有効フラグ
	- DietplusCheck：食生活PLUSチェックの有効フラグ
	
	<br><パラメータ例><br>
	```python
	"Monday": {
		"StepInput"    : 0,
		"SleepInput"   : 1,
		"SleepCheck"   : 1,
		"AlcoholCheck" : 1,
		"DietCheck"    : 1,
		"DietplusCheck": 1
	}
	```
	※上記の場合、「月曜日は歩数値の自動入力以外を実施する」<br>
	<br>

- **parameter/HealthParam_SleepValueInfo.json**

	<p>睡眠値の自動入力に関わるパラメータ<br>
	以下のパラメータを曜日ごとに指定する<br>

	- Switch<br>
		自動入力を実施する条件<br>
		ここで指定した条件を満たさない場合は入力をスキップすることができる

	- Range<br>
		自動入力値のレンジ<br>
		ここで指定した条件を満たす値をランダムで決定する

	- Step<br>
		自動入力値のサンプリング間隔<br>
		0.1の場合は、0.1, 0.2, 0.3, ... のような数値がランダムに入力される

	<br><パラメータ例><br>
	```python
	"Monday": {
		"Switch": "x<6.0 or x>7.5",
		"Range" : "x>=6.0 and x<=7.5",
		"Step"  : 0.1
	}
	```
	※月曜日の入力値が「6未満もしくは7.5を超える」場合、<br>
	&emsp;6から7.5の値を入力する(サンプリング間隔は0.1)<br><br>

- **parameter/HealthParam_StepValueInfo.json**

	<p>歩数値の自動入力に関わるパラメータ<br>
	※パラメータは「HealthParam_SleepValueInfo.json」同様<br><br>

- **profile/GMailProfile.json**

	<p>Googleアカウント情報を記載するファイル<br>
	以下のパラメータを指定する<br>

	- Adress：アカウントメールアドレス
	- Password：パスワード

	<br><パラメータ例><br>
	```python
	"Adress"  : "XXXX@gmail.com",
	"Password": "123456789"
	```

- **profile/HealthProfile.json**

	<p>健康入力アプリのアカウント情報を記載するファイル<br>
	※パラメータは「GMailProfile.json」同様
<br>

### **3.3 Googleアカウントで「安全性の低いアプリのアクセス」の設定**

3.2節の「GMailProfile.json」で指定したアカウントの設定で、<br>
「安全性の低いアプリのアクセス」を有効にする<br>
(下記URLにアクセスし、設定できます)<br>
https://support.google.com/accounts/answer/6010255?p=less-secure-apps&hl=ja&visit_id=637234281504299747-1908005239&rd=1<br><br>


## **4. アプリ実行方法**

実行手順は下記の通りです
+ Docker Quickstart Terminalを実行する

+ bat/dockerフォルダの**docker_start.bat**を実行する<br>
　このバッチファイルを実行することで、dockerのコンテナが起動します

+ bat/runフォルダのXXXX.batを実行する<br>
　下記batファイルの内、目的にあったものを使用してください
	+ **draw_param.bat**:ユーザパラメータを描画した画像を作成し、保存する<br>
	　logフォルダ内にパラメータ描画画像を保存します<br>
	　※現在のパラメータを可視で確認したい場合に使用してください
	+ **run_confirm.bat**:現在の入力状況を表示する<br>
	　コマンドプロンプト上に値が表示されます
	+ **run_record.bat**:自動入力を実行する<br>
	　ユーザパラメータに応じて自動入力を実施します
	+ **run_resident.bat**:本アプリを常駐起動する<br>
	　メールで「入力状況の確認」および「自動入力」の命令が出せるようになります


## **5. その他**

+ アプリを終了する際<br>
bat/dockerフォルダの**docker_stop.bat**を実行することでアプリを終了することができます<br>
※正確に言うと、dockerのコンテナを停止します

+ その他ファイルの説明<br>
	+ **bat/docker/docker_clear.bat**<br>
	dockerのコンテナおよびイメージを全削除します<br>
	※dockerのコンテナが上手く起動しない場合に使用したりします<br>
	　他の用途でもdockerを使っている人は、実行しない方がいいと思います<br>
	　(全てのコンテナとイメージが消え去ります)

	+ **bat/test/XXXX.bat**<br>
	アプリが正常に動作するかを確認するためのbatファイルです<br>
	下記のテストbatファイルが格納されています
		+ *check_container.bat*： dockerコンテナ正常起動確認
		+ *check_version_chromedriver-binary.bat*: chromedriver-binaryバージョン確認
		+ *check_version_google-chrome-stable.bat*: chromeバージョン確認
		+ *check_version_python.bat*： pythonバージョン確認
		+ *test_helloworld.bat*: python実行可能確認
		+ *test_recv_mail.bat*： 受信メール取得機能確認
		+ *test_selenium.bat*： webスクレイピング機能確認
		+ *test_send_mail.bat*： メール送信機能確認
<br><br>
## **8. 不具合/疑問点があった際**

下記URLにアクセスし、issueを確認し、類似質問がないかを確認してください<br>
(類似質問がある際は、その質問が解決するのを待ってください)<br>
https://github.com/sakagami0615/HealthMileage/issues<br>

類似質問がない際は、不具合内容/疑問内容をissueで打ち上げてください<br>
(GitHubアカウントを持ってない人は作ってください)<br><br>

■issue作成手順<br>
+ 緑色の[**New issue**]ボタンをクリックする
+ Label項目で不具合か疑問かを指定してください<br>
	◆ 不具合：**bug**<br>
	◆ 疑問：**question**<br><br>
+ Titleは、記載内容が一目でわかるように記載してください(切実)
+ Writeには、下記の内容を記載してください<br>
	◆ 不具合<br>
	　・どんな行動をしたらエラーが発生したかを記載する<br>
	　・**log/ErrorLog.log**が生成されているのであれば、中身をコピペする<br>
	◆ 疑問<br>
	　・**README.md**のどの章、節なのかを記載する<br><br>


## **7. 備考**
フォルダツリーは下記の通りです

```
HealthMileage
    │  .gitignore
    │  docker-compose.yml
    │  Dockerfile
    │  README.md
    │  requirements.txt
    │
    ├─api
    │  │  draw_param.py
    │  │  run_confirm.py
    │  │  run_record.py
    │  │  run_resident.py
    │  │
    │  ├─data
    │  │      ※処理内で生成されたファイル保存場所
    │  │
    │  ├─module
    │  │  ├─Health
    │  │  │      HealthDriver.py
    │  │  │      HealthParam.py
    │  │  │      HealthRunConfirm.py
    │  │  │      HealthRunRecord.py
    │  │  │      HealthUtility.py
    │  │  │      HealthXPath.py
    │  │  │
    │  │  ├─Mailler
    │  │  │      MaillExtractor.py
    │  │  │      MaillOrder.py
    │  │  │      MaillParam.py
    │  │  │      MailUtility.py
    │  │  │
    │  │  ├─Main
    │  │  │      confirm.py
    │  │  │      MainParam.py
    │  │  │      MainUtility.py
    │  │  │      record.py
    │  │  │      resident.py
    │  │  │
    │  │  ├─Request
    │  │  │      Request.py
    │  │  │      RequestParam.py
    │  │  │
    │  │  └─Scheduler
    │  │          Scheduler.py
    │  │
    │  └─test
    │          TestConfirm.py
    │          TestHelloworld.py
    │          TestMailRecv.py
    │          TestMailSend.py
    │          TestRecord.py
    │          TestSelenium.py
    │
    ├─bat
    │  ├─docker
    │  │      docker_clear.bat
    │  │      docker_start.bat
    │  │      docker_stop.bat
    │  │
    │  ├─run
    │  │      draw_param.bat
    │  │      run_confirm.bat
    │  │      run_record.bat
    │  │      run_resident.bat
    │  │
    │  └─test
    │          check_container.bat
    │          check_version_chromedriver-binary.bat
    │          check_version_google-chrome-stable.bat
    │          check_version_python.bat
    │          test_helloworld.bat
    │          test_recv_mail.bat
    │          test_selenium.bat
    │          test_send_mail.bat
    │
    ├─log
    │      ※処理内で生成されたファイル保存場所
    │
    └─userSetting
        ├─UserFile
        │  ├─parameter
        │  │      ※ここに記入したjsonファイルを配置する
        │  │
        │  └─profile
        │          ※ここに記入したjsonファイルを配置する
        │
        └─UserFile_template
            ├─parameter
            │      HealthParam_InputFlg.json
            │      HealthParam_SleepValueInfo.json
            │      HealthParam_StepValueInfo.json
            │
            └─profile
                    GMailProfile.json
                    HealthProfile.json
```