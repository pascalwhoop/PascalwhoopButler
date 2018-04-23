FROM python:3.6.5-stretch
RUN apt-get update && apt-get install -y --no-install-recommends texlive-xetex git
RUN pip install python-telegram-bot
WORKDIR / 
RUN git clone https://github.com/pascalwhoop/pascalwhoopbutler && cd pascalwhoopbutler
RUN apt-get install -y --no-install-recommends curl wget &&\
    curl -sSL https://get.haskellstack.org/ | sh && \
    wget https://hackage.haskell.org/package/pandoc-2.1.3/pandoc-2.1.3.tar.gz && \
    tar -xvzf pandoc-2.1.3.tar.gz 
RUN apt-get install -y --no-install-recommends unzip
RUN cd pandoc-2.1.3 && \ 
    stack setup && \
    stack install 
RUN cd /usr/bin && \
    ln -s /root/local/bin/pandoc pandoc && \
    rm -rf /root/.stack

COPY ./docker_config.json ./config.json
#starting the bot
CMD ["python", "main.py"]

