# create a neo4j image which can store data
FROM neo4j

MAINTAINER harumonia
USER root

RUN apt-get update && apt-get install vim
RUN rm data && cp -r /data /neodata && chmod -R 777 /neodata
RUN ln -s  /neodata data
