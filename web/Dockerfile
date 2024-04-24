FROM node:20-alpine

WORKDIR /web

COPY src/april-react/package.json package-lock.json ./

RUN npm create vite@latest /app -- --template react -y

RUN npm install

COPY . /web

EXPOSE 3000

CMD [ "npm", "run", "dev" ]