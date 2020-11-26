FROM node:14.5-alpine
WORKDIR /app
COPY package.json yarn.lock ./
COPY patches ./patches
RUN yarn
COPY . .
CMD yarn start
