# Application in MAC
```bash
export DBUSER="admin"
export PASSWORD="Admin1234"
export PRIMARY_HOST="0.0.0.0"
export READONLY_HOST="0.0.0.0"
export PRIMARY_PORT=33061
export READONLY_PORT=33061
export PRIMARY_DBNAME="ecommerce"
export READONLY_DBNAME="ecommerce"
# export HOST_NAME=$(hostname)
# export HOST_IP=$(hostname -I | awk '{print $1}')
# app 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
![](./img/2024-07-22-16-37-21.png)


# EKS 실행을 위해 Docker Image 배포
```bash
docker build --no-cache -t color275/ecommerce-linux --platform linux/amd64 .
# docker build -t color275/ecommerce-linux --platform linux/amd64 .
docker push color275/ecommerce-linux
```

