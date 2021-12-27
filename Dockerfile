FROM python:3.8
WORKDIR /lark-doc-blog/backend

COPY requirement.txt ./
RUN pip install -r requirement.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .
CMD ["gunicorn", "server:app", "-c", "./gunicorn.conf.py"]