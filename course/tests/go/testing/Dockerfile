FROM golang:1.16.0-alpine3.13

WORKDIR /workdir/app

COPY test.go task.go ./

CMD ["go", "run", "./test.go"]