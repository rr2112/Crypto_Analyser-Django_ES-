# Crypto_Analyser-Django_ES-
# Django app to analyse crypto market via Kibana, indexing scripts 

###elastic config for second host on same network: add below in  /elasticsearch.yml
transport.host: localhost
transport.tcp.port: 9300
http.port: 9200
network.host: 0.0.0.0

docker build -f Dockerfile.trading -t trading .

docker rmi $(docker images | grep '<none>' | awk '{print $3}' | tr '\n' ' ')

env vars required:
LD_LIBRARY_PATH=/usr/local/lib

###new dependency addition
 - add to requirements.in
 - pip install pip-tools
 - pip-compile requirements.in && pip install -r requirements.txt

###TA-Lib installation:
 tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --build=aarch64-unknown-linux-gnu && \
  sudo make && \
  sudo make install && pip install ta-lib
