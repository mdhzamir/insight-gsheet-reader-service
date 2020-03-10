version: '3'

services:
  insight-gsheet-reader-service:
    container_name: insight-gsheet-reader-service
    image: 203.188.245.212:7800/IMAGE:TAG
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    restart: always
    ports:
      - 5001:5001
    networks:
      - insight-newtork 
    env_file: 
      - ./microservice-common-properties.env      
    depends_on: 
      - insight-discovery-service
networks:     
  insight-newtork:
