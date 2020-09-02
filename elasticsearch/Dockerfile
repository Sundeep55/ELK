ARG ELK_VERSION
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELK_VERSION}
ENV ES_JAVA_OPTS -Xms512m -Xmx512m
COPY ./config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
