FROM python:3


RUN apt-get update && \
	apt-get install -y unzip && \
	apt-get install -y gnupg2

# install ChromeDriver
ADD https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip

# install google-chrome
RUN sh -c 'wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -' && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable=81.0.4044.129-1

# install python-library
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir selenium
RUN pip install --no-cache-dir chromedriver-binary==81.0.4044.69


ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome
