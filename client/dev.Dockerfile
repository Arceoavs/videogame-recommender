# base image
FROM node:12.2.0-alpine

# set working directory
WORKDIR /client

# add `/client/node_modules/.bin` to $PATH
ENV PATH /client/node_modules/.bin:$PATH

# install and cache client dependencies
COPY package.json /client/package.json
RUN npm install
RUN npm install @vue/cli@3.7.0 -g

# start client
CMD ["npm", "run", "serve"]