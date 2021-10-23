# Crypto_Analyser-Django_ES-
# Django app to analyse crypto market via Kibana, indexing scripts 

elastic config for second host on same network: add below in  /elasticsearch.yml
transport.host: localhost
transport.tcp.port: 9300
http.port: 9200
network.host: 0.0.0.0