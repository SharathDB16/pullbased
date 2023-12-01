USE provisioning_store_test;

LOCK TABLES `edge_type` WRITE;
/*!40000 ALTER TABLE `edge_type` DISABLE KEYS */;
DELETE FROM `edge_type` WHERE 1;
INSERT INTO `edge_type` VALUES (1,'test1','static','default',_binary 'file1 static default',_binary 'file2 static default','2021-01-29 06:24:33','2021-05-30 13:23:51'),(2,'test2','mid','default',_binary 'file1 mid default',_binary 'file2 mid default','2019-03-01 06:24:33','2021-06-30 13:23:51'),(3,'test3','mobile','kontronmetro',_binary 'file1 mobile kontronmetro',_binary 'file2 mobile kontronmetro','2018-01-29 06:24:33','2021-07-30 13:23:51');
/*!40000 ALTER TABLE `edge_type` ENABLE KEYS */;
UNLOCK TABLES;