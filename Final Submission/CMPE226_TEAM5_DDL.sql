SET foreign_key_checks = 0;

DROP DATABASE IF EXISTS teamfive;
CREATE DATABASE teamfive;
USE teamfive;

CREATE TABLE user (
  ssn        CHAR(9) NOT NULL,
  user_name  VARCHAR(100) NOT NULL,
  password   VARCHAR(100) NOT NULL,
  bdate      DATE,
  address    VARCHAR(100),
  email      VARCHAR(100) NOT NULL,
  PRIMARY KEY (user_name),
  UNIQUE KEY (ssn),
  UNIQUE KEY (email)
);

CREATE TABLE name (
  user_name  VARCHAR(100) NOT NULL,
  fname      VARCHAR(40) NOT NULL, 
  minit      VARCHAR(10),
  lname      VARCHAR(40) NOT NULL,
  PRIMARY KEY (user_name),
  FOREIGN KEY (user_name) REFERENCES user(user_name)
        ON DELETE CASCADE
);

# fixed schema done

CREATE TABLE user_phone (
  ssn     CHAR(9) NOT NULL,
  phone   VARCHAR(15),
  PRIMARY KEY (ssn, phone),
  FOREIGN KEY (ssn) REFERENCES user(ssn)
        ON DELETE CASCADE
);

CREATE TABLE owner (
  owner_num  VARCHAR(15) NOT NULL,
  ssn        CHAR(9) NOT NULL,
  buyer_num  VARCHAR(15),
  offer_num  VARCHAR(15),
  PRIMARY KEY (owner_num),
  FOREIGN KEY (ssn) REFERENCES user(ssn)
    ON DELETE CASCADE,
  FOREIGN KEY (buyer_num, offer_num) REFERENCES offer(buyer_num,offer_num)
    ON DELETE SET NULL
);

CREATE TABLE agent (
  agent_num        VARCHAR(15) NOT NULL,
  ssn              CHAR(9) NOT NULL,
  total_commission DECIMAL(10,2),
  commission_rate  DECIMAL(3,2) CHECK (commission_rate > 0 AND commission_rate < 1), 
  PRIMARY KEY (agent_num),
  FOREIGN KEY (ssn) REFERENCES user(ssn)
        ON DELETE CASCADE
);

CREATE TABLE buyer (
  buyer_num  VARCHAR(15) NOT NULL,
  ssn        CHAR(9) NOT NULL,
  PRIMARY KEY (buyer_num),
  FOREIGN KEY (ssn) REFERENCES user(ssn)
        ON DELETE CASCADE
);

CREATE TABLE property (
  property_id  VARCHAR(15) NOT NULL,
  status       VARCHAR(15) NOT NULL,
  price        DECIMAL(15,2) CHECK (price > 0),
  asking_price DECIMAL(15,2) CHECK (asking_price > 0),
  list_date    DATE,
  sold_date    DATE,
  owner_num    VARCHAR(15) NOT NULL,
  agent_num    VARCHAR(15),
  PRIMARY KEY (property_id),
  FOREIGN KEY (owner_num) REFERENCES owner(owner_num)
    ON DELETE CASCADE,
  FOREIGN KEY (agent_num) REFERENCES agent(agent_num)
    ON DELETE SET NULL
);

CREATE TABLE property_parameter (
  property_id  VARCHAR(15) NOT NULL,
  room_num     INTEGER,
  bath_num     INTEGER,
  garage_num   INTEGER,
  lot_size     INTEGER,
  zip_code     VARCHAR(15),
  area         VARCHAR(15),
  PRIMARY KEY (property_id), 
  FOREIGN KEY (property_id) REFERENCES property (property_id)
        ON DELETE CASCADE
);

CREATE TABLE open_house (
  agent_num    VARCHAR(15) NOT NULL,
  oh_num       VARCHAR(15) NOT NULL,
  start_date   DATE,
  end_date     DATE,
  property_id  VARCHAR(15) NOT NULL,
  PRIMARY KEY (agent_num, oh_num),
  FOREIGN KEY (agent_num) REFERENCES agent(agent_num)
        ON DELETE CASCADE,
  FOREIGN KEY (property_id) REFERENCES property(property_id)
        ON DELETE CASCADE
);

CREATE TABLE offer (
  buyer_num   VARCHAR(15) NOT NULL,
  offer_num   VARCHAR(15) NOT NULL,
  price       DECIMAL(15,2) CHECK (price > 0),
  status      VARCHAR(15) NOT NULL,
  offer_date  DATE,
  property_id VARCHAR(15) NOT NULL,
  agent_num   VARCHAR(15) NOT NULL,
  PRIMARY KEY (buyer_num, offer_num),
  FOREIGN KEY (buyer_num) REFERENCES buyer(buyer_num)
        ON DELETE CASCADE,
  FOREIGN KEY (property_id) REFERENCES property(property_id)
        ON DELETE CASCADE,
  FOREIGN KEY (agent_num) REFERENCES agent(agent_num)
        ON DELETE CASCADE
);

CREATE TABLE oh_visit (
  buyer_num    VARCHAR(15) NOT NULL,
  agent_num    VARCHAR(15) NOT NULL,
  oh_num       VARCHAR(15) NOT NULL,
  PRIMARY KEY (buyer_num, agent_num, oh_num),
  FOREIGN KEY (buyer_num) REFERENCES buyer(buyer_num)
      ON DELETE CASCADE,
  FOREIGN KEY (agent_num, oh_num) REFERENCES open_house(agent_num, oh_num)
      ON DELETE CASCADE
);

INSERT user VALUES
('085669980', 'Angelic','pbkdf2:sha256:50000$UgcjLxtz$53483568040ad57f6c878319139daa41f209ac5dacf770aba33754128da95f86', '1978-05-22', '1967 Jordan, Milwaukee, WI', 'irsocorro@fafire.br'),
('235090001', 'Ochlocracy','pbkdf2:sha256:50000$XR9CZkK6$91268c20d49d090ffd10613ec0672d6e8454ae2cac8986589eec7afa3758826c', '1968-02-13', '176 Main St., Atlanta, GA', 'malak.el.10420@priceonline.co'),
('578568678', 'Epistoler','pbkdf2:sha256:50000$jxEBCK0k$936ba500cba3e8668dd08dfbe66d575d9e88e85e12828de809766413f4094ecf', '1958-01-16','134 Pelham, Milwaukee, WI', 'Trae1940@fleckens.hu'),
('036078043', 'Jointure','pbkdf2:sha256:50000$xHAHK1Mb$71e041605aff0748081409ea8ac1a039e24981fc6c1e7af72f21021788c578fc', '1954-05-22','266 McGrady, Milwaukee, WI', 'Dausle1961@rhyta.com'),
('587522934', 'Vignette','pbkdf2:sha256:50000$wfpE4NCF$a64d497232baae91dae2501c57cc61c021aa5b8424483bba27bd7b580e1b2bd6', '1966-10-10','123 Peachtree, Atlanta, GA', 'Encely93@gustr.com'),
('395404942', 'ChancemtFerial','pbkdf2:sha256:50000$0hgXxXHZ$bbbf10da2bad8459417419d9ec5d918104a8bc04a5d6c50ae0ce7fb9edd21ee2', '1966-01-12','2342 May, Atlanta, GA', 'Thint1947@teleworm.us'),
('001487368', 'Taction','pbkdf2:sha256:50000$kCT6Xdle$ec6b992914ed06eea83ec82d97c0d442a205d302ca61b02292b8d1b82e6a45ec', '1967-11-14','111 Allgood, Atlanta, GA', 'eu@nunc.com'),
('515827834', 'Cistern','pbkdf2:sha256:50000$UCPHarik$881d81772114560fa2bf8dbf24578e761ec18cbba39da6c4a727a18efbf7c980', '1975-06-30','7676 Bloomington, Sacramento, CA', 'cursus@cras.com'),
('520196480', 'Queanylu70','pbkdf2:sha256:50000$ETjt17Nb$221465a4a81b67b3c505f835016f574b94758adf1b561743d4bcf8112d741965', '1950-10-09','4333 Pillsbury, Milwaukee, WI', 'vestibulum@massa.com'),
('504342542', 'Geno50Yearn','pbkdf2:sha256:50000$ZeNEGJc2$9b64e72e441dbbce57b5609323cda7e13c156b3fc9320d14ca3d875c5cba7e6f', '1959-03-29','980 Dallas, Houston, TX', 'neque@eleifend.com'),
('021306756', 'Cyaneous','pbkdf2:sha256:50000$EK65QV1u$cc79f118eb2dfd54c6cc6b95021a022c6305d7dae04446492d5d5600be2f882f', '1962-07-31','5631 Rice, Houston, TX', 'quam@sollicitudin.com'),
('501286917', 'Adscititious','pbkdf2:sha256:50000$JvHSpM4D$f3cfd8229b0207b1304bdc9c80961ca96cd8aaf2acfe53629c328ef40b41751d', '1952-09-15','971 Fire Oak, Humble, TX', 'scelerisque@aliquam.com'),
('008849203', 'Pastichewas','pbkdf2:sha256:50000$WR94gX9c$22db8d09671d8edfe6c89cbda2f03b62d375a487db8992c79f9559099286628f', '1958-07-19','3321 Castle, Spring, TX', 'id@nulla.com'),
('577228421', 'Largesse','pbkdf2:sha256:50000$MHv6IEIy$f3fae65fca4c13bfb954f39f91ec984f84d04c2f655ca4dc2de7af60cf41bf15', '1955-01-09','731 Fondren, Houston, TX', 'aliquam@erat.com'),
('389156190', 'Amaranth','pbkdf2:sha256:50000$AWXGidZk$c3664bf3febf90d68e7152454d45ea04004367a1e711b2eadcba907addc04cbb', '1931-06-20','291 Berry, Bellaire, TX', 'mattis@commodo.com'),
('648227273', 'Coelacanth','pbkdf2:sha256:50000$jnIoYPCK$96f58b82699f25235cf059fe0528ae122643446a2da4323817534d414ea0a97f', '1945-12-08','638 Voss, Houston, TX', 'lacus@molestie.com'),
('506880757', 'Clarionwas','pbkdf2:sha256:50000$1UdD8XeS$a1358881caac9a0c057ac5de1c72a8a716d51fb5fcfdd55562cd428e1328c88a', '1927-11-10','450 Stone, Houston, TX', 'bibendum@ac.com'),
('085304579', 'Boulevard','pbkdf2:sha256:50000$2MxdrepH$87e762f855213d52d9ada950af0f11d851a83c20d4c2f2d121d803d083b4d877', '1966-12-16','112 Third St, Milwaukee, WI', 'fames@fermentum.com'),
('393309045', 'Sussurous','pbkdf2:sha256:50000$DLtH30TB$c2fa5312298d711baeb3bd31f6d33557b4ed7168974e444750067bd32024d369', '1967-11-11','263 Mayberry, Milwaukee, WI', 'tristique@sit.com'),
('522407366', 'Soliloquy','pbkdf2:sha256:50000$OENjVF0G$40343eaf38aa6febcb039016fa4ab165f72d85b4082cef5d41bc1526c3c36109', '1960-03-21','565 Jordan, Milwaukee, WI', 'pretium@malesuada.com'),
('003389041', 'Esclavage','pbkdf2:sha256:50000$OAJhNqUV$ddccb8223dc306d0b9f5f28a6a62f89db22179a938494e77ea72b2705d5a3dfe', '1970-10-23','6677 Mills Ave, Sacramento, CA', 'tortor@praesent.com'),
('640804931', 'Dissemble','pbkdf2:sha256:50000$tvJNIkgW$1f3ff35aec7de57b701b01be6c0e110fd4925c47547cfc051937736fb442c669', '1970-01-07','145 Bradbury, Sacramento, CA', 'dignissim@laoreet.com'),
('059161255', 'Lovable','pbkdf2:sha256:50000$yh7R7PC8$414950584070934cd1c021a8c23a2d578b6b290a284a32f417505b0fbd2b7325', '1956-06-19','111 Hollow, Milwaukee, WI', 'egestas@duis.com'),
('574823410', 'Melodywis5656','pbkdf2:sha256:50000$EGx0Ij0r$5a05a962d96cf4cd77ea55cc49ac8653bec8c045ddd324021b6cbdb66c6781d8', '1966-06-18','233 Solid, Milwaukee, WI', 'adipiscing@integer.com'),
('509429536', 'Nacarat','pbkdf2:sha256:50000$DjJhK8WZ$22fb3c3be7144ca1bb771e3ad8ff97dd974f00cad79b004a260bc89edf947d4a', '1977-07-31','987 Windy St, Milwaukee, WI', 'blandit@orci.com'),
('215718002', 'Cereology','pbkdf2:sha256:50000$HlbXeTFD$5d84559cb4218a9dfffeda219ea983bf807007937c3416df39fb1b72cdc34ea5', '1969-04-16','222 Howard, Sacramento, CA', 'sapien@ac.com'),
('471022680', 'Portico','pbkdf2:sha256:50000$Sra7Zmam$15b352eec748c7c16639c5556b416cf4df1ce15162f0ef0be0a8ddf1ecff2374', '1968-04-17','8794 Garfield, Chicago, IL', 'nibh@suspendisse.com'),
('396484738', 'Puregie687','pbkdf2:sha256:50000$vEn9HNqZ$1f6efe4016b792d5d671f5075bee92be56984361f37f094c69ea4a7e3cda68a0', '1966-01-14','6234 Lincoln, Chicago, IL', 'vel@dignissim.com'),
('218549970', 'Medallion','pbkdf2:sha256:50000$wQLyXYoI$d69ab3ab50e0b39ba8d4e42dc4a672930cceba86b23c37c57039745a1e042086', '1966-04-16','1976 Boone Trace, Chicago, IL', 'vulputate@malesuada.com'),
('392076224', 'Posiratio','pbkdf2:sha256:50000$2OglOIh5$8320c2d50fc3dcd45a55657f0e9b6ecf5ba73138dadc0548dbc33213520c2e0c', '1963-06-09','417 Hancock Ave, Chicago, IL', 'viverra@turpis.com');

INSERT name VALUES
('Angelic', 'Colten', 'D', 'London'),
('Ochlocracy', 'Rosella', 'F', 'Marsden'),
('Epistoler', 'Evan','E','Wallis'),
('Jointure', 'Josh','U','Zell'),
('Vignette', 'Simonne', 'A', 'Kay'),
('ChancemtFerial', 'Lance', 'G', 'Meadows'),
('Taction', 'Ahmad','V','Jabbar'),
('Cistern', 'Danille', 'H', 'Guest'),
('Queanylu70', 'Jennifer','S','Wallace'),
('Geno50Yearn', 'Franklin','T','Wong'),
('Cyaneous', 'James','E','Borg'),
('Adscititious', 'Tom','G','Brand'),
('Pastichewas', 'Jenny','F','Vos'),
('Largesse', 'Chris','A','Carter'),
('Amaranth', 'Kim','C','Grace'),
('Coelacanth', 'Jeff','H','Chase'),
('Clarionwas', 'Bonnie','S','Bays'),
('Boulevard', 'Alec','C','Best'),
('Sussurous', 'Sam','S','Snedden'),
('Soliloquy', 'Nandita','K','Ball'),
('Esclavage', 'Bob','B','Bender'),
('Dissemble', 'Jill','J','Jarvis'),
('Lovable', 'Kate','W','King'),
('Melodywis5656','Lyle','G','Leslie'),
('Nacarat', 'Billie','J','King'),
('Cereology', 'Jon','A','Kramer'),
('Portico', 'Ray','H','King'),
('Puregie687', 'Gerald','D','Small'),
('Medallion', 'Arnold','A','Head'),
('Posiratio', 'Helga','C','Pataki');

INSERT user_phone VALUES
('085669980', '518-555-0137'),
('235090001', '518-555-0160'),
('578568678', '518-555-0145'),
('036078043', '410-555-0114'),
('587522934', '410-555-0128'),
('395404942', '410-555-0146'),
('001487368', '775-555-0152'),
('515827834', '775-555-0189'),
('520196480', '775-555-0136'),
('504342542', '843-555-0187'),
('021306756', '843-555-0172'),
('501286917', '843-555-0114'),
('008849203', '843-555-0172'),
('577228421', '843-555-0164'),
('389156190', '843-555-0132'),
('648227273', '202-555-0172'),
('506880757', '202-555-0105'),
('085304579', '202-555-0145'),
('393309045', '202-555-0156'),
('522407366', '202-555-0174'),
('003389041', '617-555-0110'),
('640804931', '617-555-0169'),
('059161255', '617-555-0148'),
('574823410', '302-555-0104'),
('509429536', '302-555-0137'),
('215718002', '302-555-0174'),
('471022680', '302-555-0119'),
('396484738', '302-555-0196'),
('218549970', '614-555-0111'),
('392076224', '614-555-0152'),
('085669980', '518-555-0146'),
('235090001', '518-555-0128'),
('578568678', '518-555-0148'),
('036078043', '410-555-0141'),
('587522934', '410-555-0189'),
('395404942', '410-555-0186'),
('001487368', '775-555-0123'),
('515827834', '775-555-0195'),
('520196480', '775-555-0148'),
('504342542', '843-555-0178'),
('021306756', '843-555-0134'),
('501286917', '843-555-0179'),
('008849203', '843-575-0272'),
('577228421', '843-455-0264'),
('389156190', '843-552-0182'),
('648227273', '202-586-0172'),
('506880757', '202-955-0105'),
('085304579', '202-555-0159'),
('393309045', '202-905-0156'),
('522407366', '202-525-0174'),
('003389041', '617-945-0110'),
('640804931', '617-003-0169'),
('059161255', '617-555-0189'),
('574823410', '302-555-9104'),
('509429536', '302-535-0173'),
('215718002', '302-734-0174'),
('471022680', '302-553-0187'),
('396484738', '302-823-0296'),
('218549970', '614-555-0341'),
('392076224', '614-505-0342');

INSERT agent VALUES
('agent_1', '392076224', 222903.23, 0.03),
('agent_2', '218549970', 213223.78, 0.03),
('agent_3', '396484738', 134223.65, 0.03),
('agent_4', '471022680', 230066.40, 0.03),
('agent_5', '215718002', 118955.23, 0.03),
('agent_6', '509429536', 292429.48, 0.03);

INSERT buyer VALUES
('buyer_1', '085669980'),
('buyer_2', '235090001'),
('buyer_3', '578568678'),
('buyer_4', '036078043'),
('buyer_5', '587522934'),
('buyer_6', '395404942'),
('buyer_7', '001487368'),
('buyer_8', '515827834'),
('buyer_9', '520196480'),
('buyer_10', '504342542'),
('buyer_11', '021306756'),
('buyer_12', '501286917'),
('buyer_13', '008849203'),
('buyer_14', '577228421'),
('buyer_15', '389156190'),
('buyer_16', '648227273');

INSERT owner VALUES
('owner_1', '506880757', 'buyer_2', 'offer_1'),
('owner_2', '085304579', 'buyer_5', 'offer_4'),
('owner_3', '393309045', 'buyer_12', 'offer_3'),
('owner_4', '522407366', 'buyer_6', 'offer_6'),
('owner_5', '003389041', 'buyer_9', 'offer_2'),
('owner_6', '640804931', 'buyer_1', 'offer_7'),
('owner_7', '059161255', 'buyer_10', 'offer_5'),
('owner_8', '574823410', 'buyer_15', 'offer_8');

INSERT property VALUES
('property_1', 'Sold', 835000.00,  836000.00, '2016-10-26', '2016-11-28', 'owner_1', 'agent_1'),
('property_2', 'Sold', 1068000.00, 1065000.00, '2015-03-22', '2016-10-21', 'owner_2', 'agent_1'),
('property_3', 'On Sale', 1011169.00, 1011169.00, '2017-02-17', null, 'owner_3', 'agent_2'),
('property_4', 'Sold', 830624, 830000, '2016-11-17', '2017-01-03', 'owner_3', 'agent_2'),
('property_5', 'Sold', 1899500, 1900000, '2015-04-29', '2016-12-04', 'owner_4', 'agent_3'),
('property_6', 'On Sale', 1275000, 1275000, '2016-05-19', null, 'owner_4', 'agent_4'),
('property_7', 'Sold', 1349000, 1345000, '2015-06-05', '2016-04-05', 'owner_5', 'agent_5'),
('property_8', 'On Sale', 589529, 589529, '2017-05-12', null, 'owner_5', 'agent_4'),
('property_9', 'Sold', 776517, 780000, '2017-07-07', '2017-08-28', 'owner_6', 'agent_6'),
('property_10', 'On Sale', 1489000, 1489000, '2017-08-25', null, 'owner_7', 'agent_2'),
('property_11', 'On Sale', 1230000, 1230000, '2017-10-10', null, 'owner_7', 'agent_2'),
('property_12', 'Sold', 950000, 950000, '2017-11-02', '2017-11-14', 'owner_7', 'agent_6'),
('property_13', 'Sold', 119900, 1200000, '2016-09-06', '2017-10-29', 'owner_7', 'agent_6'),
('property_14', 'On Sale', 784990, 764990, '2016-07-04', null, 'owner_8', 'agent_3'),
('property_15', 'Sold', 815990, 780990, '2017-03-02', '2017-08-09', 'owner_8', 'agent_5'),
('property_16', 'On Sale', 870990, 830990, '2017-09-21', null, 'owner_8', 'agent_1'),
('property_17', 'On Sale', 2934789, 2934789, '2017-11-02', null, 'owner_8', 'agent_1'),
('property_18', 'On Sale', 1799000, 1789000, '2017-10-07', null, 'owner_2', 'agent_3'),
('property_19', 'On Sale', 1650000, 1555000, '2017-11-03', null, 'owner_1', 'agent_5');

INSERT property_parameter VALUES
('property_1', 5, 3, 2, 5662, 'CA 95136', 'San Jose'),
('property_2', 5, 2, 2, 3484, 'CA 95125', 'San Jose'),
('property_3', 3, 3, 2, 2761, 'CA 95120', 'San Jose'),
('property_4', 2, 2, 1, 831, 'CA 94103', 'San Francisco'),
('property_5', 3, 2, 2, 1114, 'CA 94619', 'Oakland'),
('property_6', 3, 2, 1, 1400, 'CA 94546', 'Castro Valley'),
('property_7', 2, 1, 1, 1790, 'CA 94122', 'San Francisco'),
('property_8', 3, 2, 1, 2518, 'CA 95006', 'Boulder Creek'),
('property_9', 4, 4, 2, 3740, 'WA 98116', 'Seattle'),
('property_10', 4, 4, 2, 2920, 'WA 98115', 'Seattle'),
('property_11', 2, 2, 1, 1697, 'WA 98121', 'Seattle'),
('property_12', 2, 2, 1, 1660, 'CA 91423', 'Los Angeles'),
('property_13', 2, 1, 1, 1064, 'CA 90042', 'Los Angeles'),
('property_14', 4, 3, 2, 2481, 'NV 89106', 'Las Vegas'),
('property_15', 4, 5, 3, 4544, 'NV 89144', 'Las Vegas'),
('property_16', 3, 3, 2, 1840, 'CA 94010', 'Burlingame'),
('property_17', 3, 3, 2, 1820, 'CA 94109', 'San Francisco'),
('property_18', 2, 2, 0, 1189, 'CA 94105', 'San Francisco');

INSERT open_house VALUES
('agent_2', 'oh_1', '2017-03-20', '2017-05-20', 'property_3'),
('agent_1', 'oh_2', '2016-10-28', '2016-11-16', 'property_1'),
('agent_4', 'oh_3', '2016-05-25', '2016-07-26', 'property_5'),
('agent_4', 'oh_4', '2017-05-20', '2017-08-20', 'property_7'),
('agent_2', 'oh_5', '2017-08-25', '2017-10-25', 'property_9'),
('agent_2', 'oh_6', '2017-10-10', '2017-11-10', 'property_10'),
('agent_3', 'oh_7', '2016-08-04', '2016-09-04', 'property_13'),
('agent_1', 'oh_8', '2017-09-30', '2017-10-20', 'property_15'),
('agent_1', 'oh_9', '2017-11-07', '2017-11-18', 'property_16'),
('agent_3', 'oh_10', '2017-10-07', '2017-11-07', 'property_17'),
('agent_5', 'oh_11', '2017-11-03', '2017-11-13', 'property_18');

INSERT offer VALUES
('buyer_2', 'offer_1', 835000.00, 'Deal', '2016-11-27', 'property_1', 'agent_1'),
('buyer_5', 'offer_4', 1068000.00, 'Deal', '2016-10-18', 'property_2', 'agent_1'),
('buyer_12', 'offer_3', 830624, 'Deal', '2017-01-01', 'property_4', 'agent_2'),
('buyer_6', 'offer_6', 1275000, 'Progress', '2016-07-19', 'property_6', 'agent_4'),
('buyer_9', 'offer_2', 1349000, 'Deal', '2016-03-28', 'property_7', 'agent_5'),
('buyer_1', 'offer_7', 776517, 'Deal', '2017-08-20', 'property_9', 'agent_6'),
('buyer_10', 'offer_5', 1230000, 'Progress', '2017-11-10', 'property_11', 'agent_2'),
('buyer_15', 'offer_8', 815990, 'Deal', '2017-08-01', 'property_15', 'agent_5');

/* ALTER TABLE owner ADD CONSTRAINT FK_owner_buyer_num FOREIGN KEY (buyer_num) REFERENCES offer(buyer_num);
ALTER TABLE owner ADD CONSTRAINT FK_owner_offer_num FOREIGN KEY (offer_num) REFERENCES offer(offer_num); */

INSERT oh_visit VALUES
('buyer_2', 'agent_2', 'oh_1'),
('buyer_10', 'agent_2', 'oh_1'),
('buyer_11', 'agent_1', 'oh_2'),
('buyer_3', 'agent_4', 'oh_3'),
('buyer_5', 'agent_4', 'oh_4'),
('buyer_13', 'agent_2', 'oh_5'),
('buyer_12', 'agent_2', 'oh_6'),
('buyer_9', 'agent_3', 'oh_7'),
('buyer_15', 'agent_3', 'oh_7'),
('buyer_2', 'agent_1', 'oh_8'),
('buyer_1', 'agent_1', 'oh_9'),
('buyer_14', 'agent_3', 'oh_10'),
('buyer_16', 'agent_5', 'oh_11');

/* Add View for market report */

CREATE VIEW report_sold(area,totl_num, average_soldprice)
AS SELECT area, count(*), avg(price)
   FROM property, property_parameter
   WHERE property.property_id = property_parameter.property_id
   AND status = 'Sold'
   GROUP BY area;


CREATE VIEW report_onsale(area,totl_num, average_saleprice)
AS SELECT area, count(*), avg(price)
   FROM property, property_parameter
   WHERE property.property_id = property_parameter.property_id
   AND status = 'On Sale'
   GROUP BY area;

/* Add Stored Procedure */   
DROP PROCEDURE IF EXISTS role_check;
DELIMITER //
Create Procedure role_check(IN arg1 VARCHAR(40), 
                    IN arg2 VARCHAR(40))
BEGIN
DECLARE var1 VARCHAR(40);
IF arg1 = 'owner' 
THEN 
SELECT owner_num from owner where ssn = arg2;
ELSEIF arg1 = 'buyer'
THEN
SELECT buyer_num from buyer where ssn = arg2;
ELSE SELECT agent_num from agent where ssn = arg2;
END IF;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS role_insert;
DELIMITER //
Create Procedure role_insert(IN arg1 VARCHAR(40),
                             IN arg2 VARCHAR(40), 
                           IN arg3 VARCHAR(40))
BEGIN
DECLARE var1 VARCHAR(40);
IF arg1 = 'owner' 
THEN 
INSERT INTO owner (owner_num, ssn ) VALUES (arg2, arg3);
ELSEIF arg1 = 'buyer'
THEN
INSERT INTO buyer (buyer_num, ssn ) VALUES (arg2, arg3);
ELSE 
INSERT INTO agent (agent_num, ssn, commission_rate) VALUES (arg2, arg3, 0.03);
END IF;
END//
DELIMITER ;

SET foreign_key_checks = 1;