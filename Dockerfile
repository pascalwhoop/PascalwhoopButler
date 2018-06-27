FROM python:3.6.5-stretch
RUN apt-get update && apt-get install -y --no-install-recommends cron curl
RUN git clone https://github.com/pascalwhoop/pascalbrokmeier.de

#copying project files into container
RUN pip install python-telegram-bot pdfkit markdown
COPY ./python /butler
COPY ./puppeteer /puppeteer
WORKDIR /puppeteer
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs

RUN npm install puppeteer yargs
WORKDIR /butler
COPY ./python/config.json ./config.json
#starting the bot
CMD ["python", "main.py"]

