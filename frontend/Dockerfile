# build stage
FROM node:22 AS build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

EXPOSE 8080

# CMD [ "npm", "run", "serve" ]