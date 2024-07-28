create database ecommerce;

create user appuser@"%" identified by "appuser";
grant all privileges on ecommerce.* to appuser@"%";

CREATE TABLE ecommerce.customer (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  password VARCHAR(128) NOT NULL,
  last_login TIMESTAMP DEFAULT NULL,
  is_superuser INT NOT NULL,
  username VARCHAR(150) NOT NULL UNIQUE,
  first_name VARCHAR(150) NOT NULL,
  last_name VARCHAR(150) NOT NULL,
  email VARCHAR(254) NOT NULL,
  is_staff INT NOT NULL,
  is_active INT NOT NULL,
  date_joined TIMESTAMP NOT NULL,
  phone_number VARCHAR(20) DEFAULT NULL,
  age INT DEFAULT NULL,
  gender VARCHAR(10) DEFAULT NULL,
  address VARCHAR(200) DEFAULT NULL,
  last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  name VARCHAR(255) DEFAULT NULL
);

INSERT INTO ecommerce.customer VALUES (1,'pbkdf2_sha256$260000$PHDOuiOQ88gcUCn0K2wscs$8KGGsXPS+j4g482xCt2cPa4YnFCDRrbqOe16Ce9SN7s=','2023-04-09 06:04:06.286033',1,'admin','admin','admin','test@gmail.com',1,1,'2023-04-08 11:19:55.000000','010-7572-2721',41,'남','서울시 영등포구 문래동 모아미래도아파트','2023-04-08 11:22:13.828765','홍길동'),(2,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-13 01:45:01.250024',1,'AWS','AWS','AWS','aws@gmail.com',1,1,'2023-04-09 03:15:42.000000','010-1234-5678',21,'남','서울시 강남구','2023-04-12 00:34:33.167432','참석자'),(3,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.450006',1,'tom','정자','이','yeonghoi@example.com',0,1,'2021-07-18 05:51:44.000000','070-7422-4046',35,'여','광주광역시 노원구 압구정가','2023-04-09 06:59:55.000000','박현숙'),(4,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:48.714066',0,'gimjieun','지원','홍','jongsugim@example.com',0,1,'2022-04-12 05:04:29.000000','011-582-0469',69,'남','부산광역시 성동구 양재천808거리','2023-04-09 06:26:24.000000','김준영'),(5,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.130501',1,'seonghoi','하은','이','hyeonu76@example.org',1,1,'2022-03-24 17:22:15.000000','016-704-3014',59,'남','인천광역시 노원구 논현1로 (상호이마을)','2023-04-08 14:30:53.000000','서정훈'),(6,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:47.875732',1,'gangyeonghyi','성민','김','wi@example.net',0,1,'2021-11-24 15:27:04.000000','031-950-6363',66,'여','제주특별자치도 하남시 선릉0길 (지우윤박마을)','2023-04-09 10:02:00.000000','구민준'),(7,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.357292',0,'bagminji','경자','김','gyeonghyigim@example.com',0,1,'2022-08-30 02:23:46.000000','063-829-4907',39,'남','부산광역시 성동구 논현708가','2023-04-09 03:07:28.000000','김현준'),(8,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:48.071190',1,'ggim','지우','양','seonghyeon12@example.org',1,1,'2021-10-12 00:02:00.000000','042-639-9480',23,'여','대구광역시 구로구 양재천4거리 (성훈심리)','2023-04-08 17:24:03.000000','김성민'),(9,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.325125',1,'sujini','종수','김','yujingim@example.com',0,1,'2021-06-12 06:37:16.000000','070-7370-7911',34,'남','전라북도 가평군 봉은사로 (순옥이읍)','2023-04-08 21:01:51.000000','박경숙'),(10,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:49.056838',0,'gyeonghyi90','현숙','신','eunyeong68@example.com',1,1,'2023-02-23 04:00:31.000000','017-631-0341',49,'여','울산광역시 북구 반포대83거리','2023-04-08 20:19:53.000000','안민지'),(11,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.156004',1,'seoyejun','민석','이','hongareum@example.net',0,1,'2022-12-31 05:00:37.000000','054-133-5836',34,'남','인천광역시 서구 석촌호수길','2023-04-09 08:20:51.000000','김상철'),(12,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.138616',1,'ijongsu','수민','강','igeonu@example.com',0,1,'2022-09-18 15:31:49.000000','062-321-5977',38,'남','세종특별자치시 남구 논현9가','2023-04-09 08:35:12.000000','강서윤'),(13,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.287721',1,'seoyun68','주원','권','yeonghogim@example.org',0,1,'2022-07-13 23:53:53.000000','011-169-4466',66,'여','대구광역시 도봉구 잠실62로','2023-04-08 17:08:38.000000','심영길'),(14,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-10 15:30:12.699812',0,'zyang','준혁','안','jseo@example.net',1,1,'2023-02-17 14:24:26.000000','017-217-7328',52,'여','경기도 횡성군 반포대가 (아름김면)','2023-04-08 18:43:56.000000','김준서'),(15,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.867959',0,'eunyeongbag','정남','박','jiyeonson@example.com',0,1,'2021-07-11 00:23:26.000000','011-330-5568',36,'남','대전광역시 송파구 압구정로','2023-04-09 01:42:29.000000','이미숙'),(16,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.157100',0,'jeongho42','상호','이','iseoyun@example.org',0,1,'2021-12-19 00:47:28.000000','062-552-0004',37,'여','전라북도 안양시 만안구 도산대길 (예원남김리)','2023-04-09 08:28:15.000000','김지혜'),(17,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.285461',0,'minjungo','도윤','최','yangjihun@example.org',0,1,'2022-04-11 10:39:52.000000','053-763-1635',66,'남','경기도 수원시 장안구 삼성3로 (정호박손읍)','2023-04-09 05:32:42.000000','박경수'),(18,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.684058',1,'ocoe','미영','이','junseoi@example.org',0,1,'2021-04-25 09:07:05.000000','052-835-3710',76,'남','충청북도 논산시 반포대로','2023-04-08 21:04:16.000000','김준영'),(19,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:48.006513',0,'gimgeonu','경수','김','sumin48@example.com',0,1,'2021-10-12 23:11:11.000000','041-891-9314',51,'여','전라북도 고성군 영동대51길 (경자지이읍)','2023-04-09 03:57:37.000000','강혜진'),(20,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.125247',0,'seongsugim','숙자','이','jongsu40@example.org',1,1,'2021-09-30 23:57:50.000000','044-327-9208',78,'여','충청남도 포천시 가락405길','2023-04-09 06:44:53.000000','강상호'),(21,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.626372',0,'yeongjin27','수빈','이','gimjunho@example.org',1,1,'2023-01-11 05:12:08.000000','042-374-8901',50,'남','세종특별자치시 양천구 선릉거리','2023-04-08 16:48:00.000000','김보람'),(22,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.850631',1,'donghyeonbag','영식','김','jieunbag@example.net',0,1,'2022-02-25 09:10:09.000000','017-572-5054',53,'여','충청남도 제천시 압구정032거리','2023-04-08 18:57:32.000000','배미경'),(23,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.214251',1,'misugan','지은','문','ogsungim@example.net',0,1,'2022-10-15 21:39:30.000000','070-1006-3214',37,'여','대전광역시 노원구 봉은사96길 (현우홍읍)','2023-04-09 03:36:41.000000','최옥순'),(24,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.216031',0,'hyeonsug05','수진','권','bagsiu@example.org',1,1,'2022-06-22 22:05:28.000000','061-321-6638',42,'남','서울특별시 중구 서초중앙로 (유진김리)','2023-04-09 12:28:34.000000','김미정'),(25,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-10 15:30:12.695072',0,'yunseonghyeon','주원','김','ggim@example.org',0,1,'2022-03-17 06:15:27.000000','018-585-2449',45,'남','광주광역시 동대문구 압구정68거리 (정훈황장면)','2023-04-08 20:26:56.000000','김성진'),(26,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.594438',0,'yeonghwanbag','서윤','이','jiyeongi@example.com',1,1,'2023-02-02 18:35:47.000000','018-990-1020',41,'여','광주광역시 송파구 강남대8로 (영호양김읍)','2023-04-08 22:46:04.000000','성종수'),(27,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.156087',1,'ieungyeong','건우','신','gimyeonghwan@example.net',1,1,'2022-08-20 01:03:48.000000','051-914-4564',78,'남','울산광역시 남구 반포대로 (민재김정읍)','2023-04-09 05:32:25.000000','이예지'),(28,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:48.747834',0,'gimjia','준혁','김','idonghyeon@example.net',1,1,'2023-04-01 22:24:00.000000','053-581-8843',61,'남','전라북도 하남시 서초대6길 (광수조마을)','2023-04-08 18:20:04.000000','황예지'),(29,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.482058',0,'jihugim','미숙','김','jongsugim@example.com',1,1,'2022-09-29 06:48:39.000000','010-7253-4105',47,'남','경상북도 안양시 동안구 오금거리','2023-04-09 02:00:09.000000','김정숙'),(30,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.167770',0,'jimingang','민준','최','mijeongan@example.com',0,1,'2022-11-11 13:32:05.000000','043-925-8468',74,'여','울산광역시 은평구 역삼15거리 (은경오김리)','2023-04-08 15:36:39.000000','최서영'),(31,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.781740',1,'ci','지원','박','ibag@example.org',0,1,'2022-07-17 11:27:30.000000','061-662-6372',79,'여','부산광역시 양천구 선릉65로','2023-04-09 01:49:28.000000','한준혁'),(32,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.163162',1,'jeongsubin','보람','김','fbag@example.org',1,1,'2022-03-26 09:02:44.000000','032-445-1543',61,'여','인천광역시 남구 오금0길','2023-04-08 19:41:58.000000','박순자'),(33,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:47.729234',0,'gangjinho','지후','김','seosunja@example.net',1,1,'2023-02-03 23:37:25.000000','053-047-5378',76,'남','전라남도 청양군 봉은사길','2023-04-08 21:07:45.000000','장민수'),(34,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.611363',0,'vgim','영진','백','whwang@example.net',0,1,'2021-11-03 16:41:14.000000','018-662-0254',36,'여','경상남도 남양주시 개포066길 (지혜이김리)','2023-04-09 03:13:06.000000','배경희'),(35,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.136306',1,'jeonghun49','도현','양','gimseoyun@example.net',0,1,'2022-11-10 05:34:19.000000','070-6772-0337',19,'남','강원도 당진시 영동대길 (서준이안면)','2023-04-09 08:14:43.000000','이광수'),(36,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.422006',1,'bjin','예진','이','wcoe@example.net',1,1,'2021-09-28 10:30:13.000000','044-997-8429',27,'남','부산광역시 강동구 언주18가','2023-04-09 10:56:37.000000','민윤서'),(37,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.177054',0,'sanghobae','지영','박','juweon69@example.net',1,1,'2023-01-27 07:17:20.000000','011-568-6723',68,'여','대구광역시 강서구 논현로','2023-04-09 09:11:24.000000','황영순'),(38,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.114161',0,'isubin','성수','박','gimyeeun@example.org',1,1,'2021-06-09 11:53:35.000000','044-323-7026',61,'여','울산광역시 구로구 테헤란9거리 (정희장마을)','2023-04-08 21:07:22.000000','엄도현'),(39,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.342602',1,'subin06','예준','신','jaehyeon51@example.net',1,1,'2022-01-27 17:19:52.000000','011-743-9140',72,'남','서울특별시 서초구 강남대35가','2023-04-09 06:54:51.000000','황옥자'),(40,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.655718',1,'qgim','옥순','오','areum46@example.com',0,1,'2022-08-25 19:21:35.000000','044-411-1469',64,'여','경기도 청주시 상당구 서초대길 (예진지박동)','2023-04-08 22:22:55.000000','김영수'),(41,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.038889',1,'hyeonjungim','상현','장','sunog74@example.org',1,1,'2021-07-07 12:08:01.000000','033-027-3672',21,'여','서울특별시 강서구 논현거리 (예진김권리)','2023-04-08 19:36:31.000000','이영희'),(42,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.618063',1,'yeonghomun','미숙','김','minsui@example.org',1,1,'2023-03-12 09:24:52.000000','031-411-2976',55,'남','울산광역시 중구 역삼거리 (병철윤김동)','2023-04-08 13:46:58.000000','이성훈'),(43,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.603173',1,'sangceol56','영식','김','zgim@example.com',0,1,'2022-06-09 09:07:08.000000','031-620-3754',61,'여','대전광역시 서초구 백제고분로','2023-04-09 01:51:03.000000','전준서'),(44,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.621247',1,'yeongjingim','예지','박','yejii@example.com',1,1,'2023-03-14 03:42:23.000000','054-355-8990',43,'여','충청북도 보은군 선릉25로 (지우윤이면)','2023-04-09 08:38:50.000000','전지훈'),(45,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.857798',0,'eunjigang','민준','김','po@example.com',0,1,'2022-06-18 23:11:35.000000','044-286-1205',50,'남','충청북도 오산시 서초대4로 (서윤김동)','2023-04-08 19:11:04.000000','신성훈'),(46,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-10 15:30:12.677545',1,'yujin78','현숙','이','jeongung62@example.net',1,1,'2022-03-30 00:31:34.000000','063-251-8810',72,'남','세종특별자치시 중랑구 백제고분로 (건우송이동)','2023-04-08 14:19:37.000000','김숙자'),(47,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.083224',0,'sangho53','영자','허','seonghomun@example.net',1,1,'2023-03-20 19:44:58.000000','053-434-8082',56,'여','울산광역시 관악구 백제고분거리','2023-04-08 17:34:57.000000','박순옥'),(48,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:49.038537',0,'gimyeonghyi','영진','김','seoyeongim@example.org',1,1,'2021-07-26 06:14:36.000000','070-3486-1679',36,'남','서울특별시 양천구 도산대848가','2023-04-08 22:37:44.000000','김성민'),(49,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:50.291928',1,'hayunseo','정훈','곽','yeongjin11@example.net',0,1,'2022-05-08 22:30:13.000000','061-609-3956',53,'여','전라북도 군포시 봉은사거리','2023-04-09 02:58:43.000000','이수빈'),(50,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:50.093300',1,'gyeongsuggim','순자','임','jeongjabag@example.com',0,1,'2021-11-16 21:51:24.000000','055-677-6685',28,'남','대전광역시 서구 삼성로','2023-04-08 13:49:39.000000','최영수'),(51,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:50.371159',1,'hwangseoyeon','은정','박','vbag@example.net',1,1,'2022-04-17 00:03:24.000000','032-594-7900',58,'남','경기도 군포시 개포0가 (지혜김양리)','2023-04-08 21:22:07.000000','이준서'),(52,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.166797',1,'li','영호','박','sanghunsim@example.net',1,1,'2021-10-05 09:00:01.000000','070-8340-6596',43,'남','제주특별자치도 화성시 오금거리','2023-04-08 18:53:39.000000','이수진'),(53,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.895133',0,'boram14','현우','심','angeonu@example.net',0,1,'2021-06-26 03:06:50.000000','018-374-0255',26,'남','전라남도 연천군 선릉거리 (정자김이읍)','2023-04-09 12:40:10.000000','김성호'),(54,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:47.516621',0,'gimeunjeong','상훈','김','zgim@example.com',0,1,'2021-07-31 07:31:07.000000','041-808-3610',45,'남','충청남도 고양시 일산서구 삼성5가 (승현김마을)','2023-04-08 15:44:21.000000','김민수'),(55,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.213630',0,'seonghyeonhwang','준영','김','jeongunggim@example.com',0,1,'2022-03-27 14:12:09.000000','019-585-0960',68,'여','제주특별자치도 안산시 오금6거리 (우진최진동)','2023-04-08 14:49:07.000000','곽경희'),(56,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.371017',0,'bagseongsu','예준','백','jgim@example.org',1,1,'2021-11-30 13:46:06.000000','064-786-8311',38,'여','전라남도 고양시 덕양구 압구정길 (지우주동)','2023-04-09 09:40:32.000000','박준서'),(57,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.574856',1,'vi','현주','김','jia46@example.com',1,1,'2021-12-04 09:07:32.000000','051-159-2896',37,'여','인천광역시 은평구 개포가','2023-04-08 15:30:46.000000','김준호'),(58,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.597577',0,'ohwang','하은','박','pheo@example.com',1,1,'2023-01-30 15:52:01.000000','044-832-7026',75,'남','충청북도 태안군 도산대621로','2023-04-09 08:11:54.000000','장명자'),(59,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.345988',0,'subin58','상현','박','ogjai@example.com',1,1,'2021-05-04 14:02:30.000000','016-496-6370',48,'남','광주광역시 동작구 선릉거리 (정호박읍)','2023-04-09 09:49:08.000000','김영길'),(60,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.223442',1,'minseobaeg','아름','김','yejin93@example.org',0,1,'2023-03-13 08:29:34.000000','054-521-2111',74,'남','전라남도 부천시 오정구 압구정96가','2023-04-08 14:14:53.000000','신건우'),(61,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.600302',0,'vcoe','상철','손','ci@example.net',1,1,'2021-10-26 06:49:23.000000','018-131-8452',22,'남','경상북도 청주시 흥덕구 강남대길 (상호홍차읍)','2023-04-09 08:34:47.000000','김민지'),(62,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:48.735169',1,'gimjihun','준서','김','jieun38@example.net',1,1,'2022-04-05 23:26:28.000000','033-690-7010',69,'여','대구광역시 동구 선릉6길','2023-04-09 10:57:15.000000','송지우'),(63,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:45.870468',1,'acoe','명숙','지','si@example.com',0,1,'2022-10-08 22:34:04.000000','031-865-9126',45,'남','경상남도 강릉시 서초대718가','2023-04-08 20:11:22.000000','김정웅'),(64,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.121803',0,'imminjae','영자','이','ygim@example.net',0,1,'2022-07-08 18:00:13.000000','054-687-3574',33,'남','부산광역시 은평구 서초중앙8길 (영일이오리)','2023-04-09 00:19:29.000000','박성현'),(65,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-10 15:30:12.733448',0,'zi','민재','김','minjae48@example.org',1,1,'2022-07-17 20:56:46.000000','061-179-0594',56,'여','경상북도 수원시 석촌호수031길','2023-04-09 02:26:03.000000','오준서'),(66,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.784365',0,'ebag','지후','손','xbag@example.org',0,1,'2021-04-26 02:41:43.000000','053-932-1843',33,'남','전라북도 광명시 영동대27가 (성훈김김리)','2023-04-09 00:25:58.000000','최영철'),(67,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.444761',0,'mijeongbag','상훈','이','jeongja14@example.org',1,1,'2021-06-20 04:02:44.000000','062-733-0363',30,'여','강원도 고양시 일산동구 양재천거리 (지원양김면)','2023-04-08 23:59:50.000000','강경숙'),(68,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.860862',1,'eunjeonggweon','준서','김','gimcunja@example.com',0,1,'2021-07-18 06:56:10.000000','017-181-6085',22,'남','경기도 홍천군 삼성538가','2023-04-08 19:23:58.000000','이현우'),(69,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.194208',0,'jeongnaman','영숙','허','yeongja40@example.org',0,1,'2021-11-26 17:10:02.000000','064-714-2318',58,'여','서울특별시 용산구 도산대617길 (지은김김동)','2023-04-08 23:16:21.000000','안미영'),(70,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.653160',1,'bcoe','도현','권','jeongjahong@example.com',0,1,'2022-03-02 10:11:41.000000','063-022-3686',72,'남','대전광역시 중구 삼성706길 (정자신김마을)','2023-04-08 22:45:56.000000','김지원'),(71,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.116396',0,'ijiyeon','지원','윤','myeongja29@example.net',0,1,'2022-09-02 23:05:39.000000','041-893-0086',46,'남','광주광역시 광진구 봉은사가','2023-04-09 07:00:52.000000','최지아'),(72,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:48.014851',0,'gcoe','명자','장','zan@example.net',1,1,'2022-05-14 15:14:24.000000','064-751-5451',72,'남','충청남도 논산시 서초대로','2023-04-08 22:27:08.000000','윤성수'),(73,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:49.073633',1,'gimmigyeong','병철','최','suminbaeg@example.net',1,1,'2021-08-19 07:21:01.000000','055-451-8864',28,'남','충청북도 안산시 상록구 석촌호수길','2023-04-08 13:55:51.000000','이현준'),(74,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.450006',1,'ken','정자','이','yeonghoi@example.com',0,1,'2021-07-18 05:51:44.000000','070-7422-4046',35,'여','광주광역시 노원구 압구정가','2023-04-09 06:59:55.000000','박현숙'),(75,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.782491',0,'cno','은주','안','pgim@example.net',0,1,'2022-08-11 14:13:20.000000','070-7661-3478',21,'남','광주광역시 강서구 백제고분거리 (미영윤면)','2023-04-09 01:15:09.000000','성성민'),(76,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-10 15:30:12.693339',1,'yunseojo','정웅','심','jieungim@example.net',1,1,'2022-11-24 12:09:21.000000','041-952-4232',79,'여','세종특별자치시 구로구 서초대4가','2023-04-08 13:21:10.000000','서서준'),(77,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.931708',0,'eunyeonggwag','중수','이','hhwang@example.org',0,1,'2022-04-25 22:20:42.000000','064-742-9335',19,'남','강원도 화성시 개포2가','2023-04-09 12:29:38.000000','이승현'),(78,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.416471',0,'ugim','현주','김','bagseoyeon@example.org',0,1,'2022-07-03 11:52:51.000000','043-953-8466',80,'남','부산광역시 송파구 역삼00길','2023-04-09 05:14:21.000000','양현우'),(79,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.778330',1,'areum31','상호','박','ijeongnam@example.com',1,1,'2021-11-19 20:36:29.000000','043-358-6875',75,'남','전라남도 동두천시 서초대길','2023-04-08 18:38:51.000000','김영숙'),(80,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.842030',1,'coesunog','수진','이','byeongceol98@example.com',1,1,'2021-05-04 05:58:46.000000','019-383-4890',32,'여','대전광역시 광진구 테헤란8길 (춘자허읍)','2023-04-08 13:06:24.000000','최영환'),(81,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.376912',1,'anminji','하윤','하','seongsu68@example.com',1,1,'2023-03-13 17:51:28.000000','019-683-2063',27,'여','제주특별자치도 계룡시 역삼3거리','2023-04-09 04:56:45.000000','김영희'),(82,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.458306',1,'ogo','병철','안','sgim@example.net',0,1,'2022-07-04 19:04:35.000000','053-072-9599',35,'여','경상북도 안성시 강남대087거리 (성현김김리)','2023-04-08 18:09:53.000000','권서준'),(83,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:49.162386',1,'gyeonghyigim','경수','김','namsugja@example.org',0,1,'2022-04-15 06:33:21.000000','010-8071-2243',27,'여','대구광역시 강북구 테헤란700길','2023-04-08 19:45:31.000000','장지현'),(84,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-10 15:30:12.458811',0,'yeongsu18','영순','최','nbag@example.net',0,1,'2021-05-01 15:09:49.000000','032-089-0254',77,'여','울산광역시 은평구 잠실로','2023-04-09 11:15:45.000000','장지은'),(85,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.153897',0,'seoyeongim','상철','하','bi@example.com',1,1,'2021-05-12 04:52:03.000000','062-757-3972',28,'여','충청북도 영월군 잠실78길','2023-04-09 02:26:37.000000','김정호'),(86,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.104268',1,'jeongsubag','정남','성','junho77@example.org',1,1,'2022-05-25 21:12:26.000000','061-446-4949',53,'여','대전광역시 서구 역삼거리 (예준차김마을)','2023-04-09 04:55:38.000000','조정자'),(87,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.215414',1,'mhan','지훈','김','gimjongsu@example.com',1,1,'2021-10-15 16:24:18.000000','031-591-8155',69,'남','경기도 홍성군 테헤란02길','2023-04-08 22:48:30.000000','김윤서'),(88,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.450006',1,'mgang','정자','이','yeonghoi@example.com',0,1,'2021-07-18 05:51:44.000000','070-7422-4046',35,'여','광주광역시 노원구 압구정가','2023-04-09 06:59:55.000000','박현숙'),(89,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.858039',1,'sanghunbag','경희','양','iyeongsun@example.org',1,1,'2022-10-30 13:33:17.000000','018-774-1477',26,'남','대구광역시 마포구 서초중앙716로','2023-04-09 01:19:37.000000','안은주'),(90,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.233218',1,'seongjin88','성훈','최','bagjihye@example.net',0,1,'2022-05-03 22:41:03.000000','010-9337-9512',59,'남','경상북도 삼척시 삼성가 (지혜김민마을)','2023-04-09 12:10:05.000000','권정수'),(91,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.157996',0,'igim','서윤','황','junhyeog60@example.com',0,1,'2021-09-06 06:39:13.000000','063-279-6822',34,'여','제주특별자치도 용인시 학동가 (명자김리)','2023-04-08 22:51:37.000000','김성현'),(92,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.602342',1,'yeeun72','민지','조','imiyeong@example.org',1,1,'2023-03-30 13:20:13.000000','019-854-0071',77,'남','서울특별시 영등포구 반포대34거리 (미영김리)','2023-04-08 17:42:29.000000','김정남'),(93,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:49.262215',0,'gimyeweon','서영','최','yeongsigjeon@example.com',0,1,'2021-04-09 22:15:08.000000','017-753-9972',61,'남','제주특별자치도 가평군 강남대로 (지혜박나면)','2023-04-09 01:34:32.000000','민정자'),(94,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:52.502199',1,'ogsun78','정남','이','gwangsubag@example.net',0,1,'2021-06-23 02:13:01.000000','051-397-3965',50,'여','충청남도 영월군 반포대72로 (예준김엄마을)','2023-04-08 21:02:02.000000','이승현'),(95,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.161185',1,'sbag','준혁','백','hi@example.com',1,1,'2021-11-07 10:05:41.000000','017-222-9085',67,'남','제주특별자치도 여주시 서초대거리 (정웅김리)','2023-04-09 04:06:34.000000','김명자'),(96,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.158833',1,'ieunju','미숙','박','yeonghoyang@example.net',0,1,'2023-01-15 15:20:56.000000','062-106-0293',62,'남','제주특별자치도 용인시 처인구 양재천길','2023-04-08 15:32:52.000000','황서영'),(97,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:51.666255',1,'lan','은정','김','jeongjuweon@example.org',1,1,'2021-05-24 04:43:32.000000','055-996-3997',44,'여','전라남도 단양군 양재천길','2023-04-08 16:42:04.000000','이현정'),(98,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:46.562647',1,'bhwang','정자','김','jiyeong96@example.com',1,1,'2022-07-01 10:00:46.000000','064-730-0917',70,'남','경기도 오산시 양재천47거리 (은경김읍)','2023-04-09 09:22:24.000000','이현지'),(99,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:53.613690',1,'yeongsig43','성민','김','zcoe@example.org',0,1,'2022-05-18 21:19:05.000000','070-9662-5162',52,'여','전라남도 동두천시 백제고분201가 (중수남읍)','2023-04-09 05:45:46.000000','김선영'),(100,'pbkdf2_sha256$260000$mexj7X6zszC2iBHFSkaZAS$Yn0sBX2MVaZzrDi5KWH5WONNDb31m3AwGNshJmv4waI=','2023-04-12 01:14:49.317076',0,'gyeongsucoe','수민','박','jieunhong@example.com',0,1,'2022-08-03 09:54:18.000000','019-749-8630',25,'남','충청남도 화천군 논현616거리','2023-04-09 09:24:30.000000','김상훈');

CREATE TABLE ecommerce.orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  promo_id VARCHAR(255) DEFAULT NULL,
  order_cnt INT NOT NULL,
  order_price INT NOT NULL,
  order_dt VARCHAR(255) NOT NULL,
  last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  customer_id INT NOT NULL,
  product_id INT NOT NULL
);


CREATE TABLE ecommerce.product (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  img_path VARCHAR(255) DEFAULT NULL,
  category VARCHAR(255) DEFAULT NULL,
  price INT NOT NULL,
  last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO ecommerce.product (product_id, name, img_path, category, price, last_update_time) VALUES
(1,'새우튀김','img/06.jpg','분식',2000,'2023-04-07 03:06:17.020331'),
(2,'김치','img/01.jpg','반찬',8000,'2023-04-07 03:11:08.706238'),
(3,'떡볶이','img/02.jpg','분식',4000,'2023-04-07 03:22:06.514964'),
(4,'삼겹살','img/04.jpg','육류',11000,'2023-04-07 14:51:54.891245'),
(5,'삼계탕','img/05.jpg','육류',15000,'2023-04-07 14:52:18.753837'),
(6,'발효빵','img/03.jpg','빵',7000,'2023-04-07 14:53:03.838920'),
(7,'고추전','img/07.jpg','분식',11000,'2023-04-07 14:53:30.601177'),
(8,'족발','img/08.jpg','안주',18000,'2023-04-07 14:53:59.291312'),
(9,'치킨','img/09.jpg','육류',18000,'2023-04-07 14:54:28.374265'),
(10,'핫도그','img/10.jpg','분식',1600,'2023-04-07 14:54:41.590185'),
(11,'쌀','img/11.jpeg','농산물',35000,'2023-04-10 14:23:58.172584'),
(12,'두부','img/12.jpeg','반찬',3500,'2023-04-10 14:24:08.273385'),
(13,'비빔밥','img/13.jpeg','분식',9000,'2023-04-10 14:24:14.862454'),
(14,'깍뚜기','img/14.jpeg','반찬',10000,'2023-04-10 14:24:38.219251'),
(15,'고추장','img/15.jpeg','반찬',12000,'2023-04-10 14:24:21.173251'),
(16,'게장','img/16.jpeg','반찬',20000,'2023-04-10 14:24:26.850835'),
(17,'된장국','img/17.jpeg','된장국',8000,'2023-04-10 14:24:30.672705'),
(18,'호박','img/18.jpeg','채소',12000,'2023-04-10 14:24:35.053926'),
(19,'계란찜','img/19.jpeg','반찬',7000,'2023-04-10 14:24:51.925492'),
(20,'짜장면','img/20.jpeg','분식',8500,'2023-04-10 14:25:33.222271');