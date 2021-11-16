# Crypto_Analyser-Django_ES-
# Django app to analyse crypto market via Kibana, indexing scripts 

elastic config for second host on same network: add below in  /elasticsearch.yml
transport.host: localhost
transport.tcp.port: 9300
http.port: 9200
network.host: 0.0.0.0

docker build -f Dockerfile.trading -t trading .

docker rmi $(docker images | grep '<none>' | awk '{print $3}' | tr '\n' ' ')

env vars required:
LD_LIBRARY_PATH=/usr/local/lib