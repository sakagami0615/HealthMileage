FROM python:3

# Environment variable (hide warning)
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
ENV DEBCONF_NOWARNINGS yes

WORKDIR /app/HealthMileageBot

# install Chrome
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update && apt-get install -y google-chrome-stable
#RUN apt-get update && apt-get install -y google-chrome-stable=80.0.3987.116-1

# pip upgrade
RUN pip install --upgrade pip

# install Selenium
RUN pip install selenium

# install chromedriver
# Chromeとchromedriver-binaryのバージョンが合わない場合があるので、
# google-chromeのバージョン情報からバージョンの近いものを pip installする
RUN google-chrome --version | perl -pe 's/([^0-9]+)([0-9]+\.[0-9]+).+/$2/g' > chrome-version
RUN pip install chromedriver-binary~=`cat chrome-version` && rm chrome-version

#ii  google-chrome-stable               88.0.4324.96-1               amd64        The web browser from Google
#chromedriver-binary 88.0.4324.96.0

# install in requirements.txt package
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# add font (日本語のページをスクリーンショットする場合には追加)
RUN apt-get install -y fonts-ipafont-gothic --no-install-recommends
