FROM node:12

WORKDIR /workdir/app

COPY test.js task.js ./

CMD ["timeout", "10", "node", "./test.js"]