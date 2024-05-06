FROM node:20-alpine

WORKDIR /web/src/april-react

COPY ./src/april-react/package.json ./src/april-react/package-lock.json ./

RUN npm install

COPY ./src/april-react .

COPY ./src/april-react/vite.config.js .

EXPOSE 3080

CMD [ "npm", "run", "dev" ]