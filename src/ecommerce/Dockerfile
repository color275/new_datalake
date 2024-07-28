# FROM python:3.10
# FROM centos:8
FROM color275/python-3-10

# RUN cd /etc/yum.repos.d/
# RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
# RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

# # 필요한 패키지 설치
# RUN yum update -y && yum install -y gcc openssl-devel bzip2-devel libffi-devel wget make mysql-devel bind-utils ncurses jq

# # Python 3.10 다운로드 및 설치
# RUN wget https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz
# RUN tar xzf Python-3.10.2.tgz
# RUN cd Python-3.10.2 && ./configure --enable-optimizations && make altinstall

# # pip 설치
# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# RUN python3.10 get-pip.py

# RUN yum install -y mysql-devel
# RUN pip3.10 install mysqlclient

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

WORKDIR /app

COPY . .

# 해당 명령어를 실행해라
RUN pip3.10 install -r requirements.txt

# opne port 문서화
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# cmd


# docker build -t color275/ecommerce-linux --platform linux/amd64 .
# docker push color275/ecommerce-linux

# docker build --no-cache -t color275/ecommerce-linux --platform linux/amd64 .
# docker push color275/ecommerce-linux

# docker exec -it ecommerce bash

# docker logs -f ecommerce

# docker run --name ecommerce --add-host=host.docker.internal:host-gateway --env-file=.env -p 8000:8000 -d color275/ecommerce-mac

# .env

# HOST_IP=$(hostname -I | awk '{print $1}')
# HOST_NAME=$(hostname)
# cat <<EOF> .env
# DBUSER=testuser
# PASSWORD=testuser
# PRIMARY_HOST=host.docker.internal
# READONLY_HOST=host.docker.internal
# PRIMARY_PORT=3306
# READONLY_PORT=3306
# PRIMARY_DBNAME="ecommerce"
# READONLY_DBNAME="ecommerce"
# EOF
# echo "HOST_IP=${HOST_IP}" >> .env
# echo "HOST_NAME=${HOST_NAME}" >> .env

# LOCAL DOCKER
# docker 통해 mac local 에서 실행
# export DBUSER="admin"
# export PASSWORD="Admin1234"
# export PRIMARY_HOST="0.0.0.0"
# export READONLY_HOST="0.0.0.0"
# export PRIMARY_PORT=33061
# export READONLY_PORT=33061
# export PRIMARY_DBNAME="ecommerce"
# export READONLY_DBNAME="ecommerce"
# export HOST_NAME=$(hostname)
# export HOST_IP=$(hostname -I | awk '{print $1}')

# MAC LOCAL 
# local 에서 source 기반으로 실행
# export DBUSER="testuser"
# export PASSWORD="testuser"
# export PRIMARY_HOST="localhost"
# export READONLY_HOST="localhost"
# export PRIMARY_PORT=3306
# export READONLY_PORT=3306
# export PRIMARY_DBNAME="ecommerce"
# export READONLY_DBNAME="ecommerce"
# export HOST_NAME=$(hostname)
# export HOST_IP=$(hostname -I | awk '{print $1}')
# export ORDER_SERVICE="localhost"
# export CUSTOMER_SERVICE="localhost"
# export PRODUCT_SERVICE="localhost"

# EC2 LOCAL 
# local 에서 source 기반으로 실행
# export DBUSER="testuser"
# export PASSWORD="testuser"
# export PRIMARY_HOST="ecommerce.cluster-cgkgybnzurln.ap-northeast-2.rds.amazonaws.com"
# export READONLY_HOST="ecommerce.cluster-ro-cgkgybnzurln.ap-northeast-2.rds.amazonaws.com"
# export PRIMARY_PORT=3306
# export READONLY_PORT=3306
# export PRIMARY_DBNAME="ecommerce"
# export READONLY_DBNAME="ecommerce"
# export HOST_NAME=$(hostname)
# export HOST_IP=$(hostname -I | awk '{print $1}')
# export ORDER_SERVICE="localhost"
# export CUSTOMER_SERVICE="localhost"
# export PRODUCT_SERVICE="localhost"
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# uvicorn main:app --port 8000 --reload

# # 삭제
# docker stop $(docker ps -a -q)
# docker container prune