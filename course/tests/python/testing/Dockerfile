FROM python

WORKDIR /workdir/app

COPY test.py task.py ./

CMD ["timeout", "10", "python3", "./test.py", "-v"]