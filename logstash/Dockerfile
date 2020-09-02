ARG ELK_VERSION
FROM docker.elastic.co/logstash/logstash:${ELK_VERSION}
ENV LS_JAVA_OPTS: -Xmx256m -Xms256m
COPY ./config/logstash.yml /usr/share/logstash/config/logstash.yml
COPY ./pipeline/ /usr/share/logstash/pipeline/
