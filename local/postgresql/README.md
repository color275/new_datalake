# PostgreSQL 설치

```bash
docker-compose up -d
docker ps
# password : Admin1234
docker exec -it dbt_postgres psql -U admin -d ecommerce
```

DBeaver 접속
![](./img/2024-07-16-22-43-58.png)
![](./img/2024-07-16-22-46-33.png)


DBeaver 에서 `sample_data.sql` 실행
![](2024-07-17-00-33-11.png)

데이터 발생
```bash
python gen_data.py
```
![](./img/2024-07-16-23-38-10.png)

주문 데이터 확인
![](./img/2024-07-16-23-38-38.png)

accesslog 확인
```bash
tail -f accesslog/access.log.*
```
![](./img/2024-07-16-23-39-12.png)