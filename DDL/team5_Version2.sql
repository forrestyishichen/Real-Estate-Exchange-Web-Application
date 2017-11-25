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
  PRIMARY KEY (ssn),
  UNIQUE KEY (user_name),
  UNIQUE KEY(email)
);

CREATE TABLE user_name (
  user_name  VARCHAR(100) NOT NULL,
  fname      VARCHAR(40) NOT NULL, 
  minit      VARCHAR(10),
  lname      VARCHAR(40) NOT NULL,
  PRIMARY KEY (user_name),
  FOREIGN KEY (user_name) REFERENCES user(user_name)
        ON DELETE CASCADE
);

###fix diagram

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
  PRIMARY KEY (owner_num)
  FOREIGN KEY (ssn) REFERENCES user(ssn)
    ON DELETE CASCADE
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
  agent_num    VARCHAR(15) ,
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

# INSERT

INSERT user VALUES
('085669980', 'Angelic', 'kx#a@fqmH7RKYP2', '1978-05-22', '1967 Jordan, Milwaukee, WI', 'irsocorro@fafire.br'),
('235090001', 'Ochlocracy', ']~Rz`Xq!~:7T,]F', '1968-02-13', '176 Main St., Atlanta, GA', 'malak.el.10420@priceonline.co'),
('578568678', 'Epistoler', 'gV2A7B8SC{2gyth', '1958-01-16','134 Pelham, Milwaukee, WI', 'Trae1940@fleckens.hu'),
('036078043', 'Jointure', 'gw8869TB[X%f:fQ', '1954-05-22','266 McGrady, Milwaukee, WI', 'Dausle1961@rhyta.com'),
('587522934', 'Vignette', 'k3k78[o|JFUD=j6', '1966-10-10','123 Peachtree, Atlanta, GA', 'Encely93@gustr.com'),
('395404942', 'ChancemtFerial', 'v8pg85PHBR=d)*9', '1966-01-12','2342 May, Atlanta, GA', 'Thint1947@teleworm.us'),
('001487368', 'Taction', '_xT9qC63BgyJ#!6', '1967-11-14','111 Allgood, Atlanta, GA', 'eu@nunc.com'),
('515827834', 'Cistern', '6GrsP0e6CR*i:/7', '1975-06-30','7676 Bloomington, Sacramento, CA', 'cursus@cras.com'),
('520196480', 'Queanylu70', 'Ded55Hp.NtM33)%', '1950-10-09','4333 Pillsbury, Milwaukee, WI', 'vestibulum@massa.com'),
('504342542', 'Geno50Yearn', 'T78vSCj23Q,p_{n', '1959-03-29','980 Dallas, Houston, TX', 'neque@eleifend.com'),
('021306756', 'Cyaneous', '5f$3z9N;L(UEn3s', '1962-07-31','5631 Rice, Houston, TX', 'quam@sollicitudin.com'),
('501286917', 'Adscititious', 'J-719UF#0L=iylg', '1952-09-15','971 Fire Oak, Humble, TX', 'scelerisque@aliquam.com'),
('008849203', 'Pastichewas', '2,e)50R9CKNxp[t', '1958-07-19','3321 Castle, Spring, TX', 'id@nulla.com'),
('577228421', 'Largesse', 'KK,C5h96B7_u{ly', '1955-01-09','731 Fondren, Houston, TX', 'aliquam@erat.com'),
('389156190', 'Amaranth', '41c2OF-Q*kK-l5j', '1931-06-20','291 Berry, Bellaire, TX', 'mattis@commodo.com'),
('648227273', 'Coelacanth', '6kK1VCO8]5thm;?', '1945-12-08','638 Voss, Houston, TX', 'lacus@molestie.com'),
('506880757', 'Clarionwas', '_}lIR72]42JWspk', '1927-11-10','450 Stone, Houston, TX', 'bibendum@ac.com'),
('085304579', 'Boulevard', 'uSv[6_+F2HAv0l9', '1966-12-16','112 Third St, Milwaukee, WI', 'fames@fermentum.com'),
('393309045', 'Sussurous', 'sK&711gUKsh8*+S', '1967-11-11','263 Mayberry, Milwaukee, WI', 'tristique@sit.com'),
('522407366', 'Soliloquy', '9ucDs7#V8R8Px&#', '1960-03-21','565 Jordan, Milwaukee, WI', 'pretium@malesuada.com'),
('003389041', 'Esclavage', '0MYh3[9{VVhe1*q', '1970-10-23','6677 Mills Ave, Sacramento, CA', 'tortor@praesent.com'),
('640804931', 'Dissemble', 'r-fT6HC;&Q959sm', '1970-01-07','145 Bradbury, Sacramento, CA', 'dignissim@laoreet.com'),
('059161255', 'Lovable', '5pXRu$c52Y4Y@h[', '1956-06-19','111 Hollow, Milwaukee, WI', 'egestas@duis.com'),
('574823410', 'Melodywis5656', '9hPRx95N}9_kvV:', '1966-06-18','233 Solid, Milwaukee, WI', 'adipiscing@integer.com'),
('509429536', 'Nacarat', 'i3U#?I5I52ji', '1977-07-31','987 Windy St, Milwaukee, WI', 'blandit@orci.com'),
('215718002', 'Cereology', 'Y8Bq3(_00Pin', '1969-04-16','222 Howard, Sacramento, CA', 'sapien@ac.com'),
('471022680', 'Portico', 'D6u+4Z_Xx82p', '1968-04-17','8794 Garfield, Chicago, IL', 'nibh@suspendisse.com'),
('396484738', 'Puregie687', 'c1J:9]91qgNP', '1966-01-14','6234 Lincoln, Chicago, IL', 'vel@dignissim.com'),
('218549970', 'Medallion', '8:yjVDs9_89D', '1966-04-16','1976 Boone Trace, Chicago, IL', 'vulputate@malesuada.com'),
('392076224', 'Posiratio', '5L45uD5nq%M&', '1963-06-09','417 Hancock Ave, Chicago, IL', 'viverra@turpis.com');

INSERT user_name VALUES
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
('Melodywis5656'，'Lyle','G','Leslie'),
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
('587522934', '410-555-0128', '410-555-0189'),
('395404942', '410-555-0146', '410-555-0186'),
('001487368', '775-555-0152', '775-555-0123'),
('515827834', '775-555-0189', '775-555-0195'),
('520196480', '775-555-0136', '775-555-0148'),
('504342542', '843-555-0187', '843-555-0178'),
('021306756', '843-555-0172', '843-555-0134'),
('501286917', '843-555-0114', '843-555-0179'),
('008849203', '843-555-0172', '843-575-0272'),
('577228421', '843-555-0164', '843-455-0264'),
('389156190', '843-555-0132', '843-552-0182'),
('648227273', '202-555-0172', '202-586-0172'),
('506880757', '202-555-0105', '202-955-0105'),
('085304579', '202-555-0145', '202-555-0159'),
('393309045', '202-555-0156', '202-905-0156'),
('522407366', '202-555-0174', '202-525-0174'),
('003389041', '617-555-0110', '617-945-0110'),
('640804931', '617-555-0169', '617-003-0169'),
('059161255', '617-555-0148', '617-555-0189'),
('574823410', '302-555-0104', '302-555-9104'),
('509429536', '302-555-0137', '302-535-0173'),
('215718002', '302-555-0174', '302-734-0174'),
('471022680', '302-555-0119', '302-553-0187'),
('396484738', '302-555-0196', '302-823-0296'),
('218549970', '614-555-0111', '614-555-0341'),
('392076224', '614-555-0152', '614-505-0342'),

('085669980', '518-555-0137', '518-555-0146'),
('235090001', '518-555-0160', '518-555-0128'),
('578568678', '518-555-0145', '518-555-0148'),
('036078043', '410-555-0114', '410-555-0141'),
('587522934', '410-555-0128', '410-555-0189'),
('395404942', '410-555-0146', '410-555-0186'),
('001487368', '775-555-0152', '775-555-0123'),
('515827834', '775-555-0189', '775-555-0195'),
('520196480', '775-555-0136', '775-555-0148'),
('504342542', '843-555-0187', '843-555-0178'),
('021306756', '843-555-0172', '843-555-0134'),
('501286917', '843-555-0114', '843-555-0179'),
('008849203', '843-555-0172', '843-575-0272'),
('577228421', '843-555-0164', '843-455-0264'),
('389156190', '843-555-0132', '843-552-0182'),
('648227273', '202-555-0172', '202-586-0172'),
('506880757', '202-555-0105', '202-955-0105'),
('085304579', '202-555-0145', '202-555-0159'),
('393309045', '202-555-0156', '202-905-0156'),
('522407366', '202-555-0174', '202-525-0174'),
('003389041', '617-555-0110', '617-945-0110'),
('640804931', '617-555-0169', '617-003-0169'),
('059161255', '617-555-0148', '617-555-0189'),
('574823410', '302-555-0104', '302-555-9104'),
('509429536', '302-555-0137', '302-535-0173'),
('215718002', '302-555-0174', '302-734-0174'),
('471022680', '302-555-0119', '302-553-0187'),
('396484738', '302-555-0196', '302-823-0296'),
('218549970', '614-555-0111', '614-555-0341'),
('392076224', '614-555-0152', '614-505-0342');

INSERT agent VALUES
('agent_1', '392076224', 222903.23, 0.03),
('a002', '218549970', 213223.78, 0.025),
('a003', '396484738', 134223.65, 0.04),
('a004', '471022680', 230066.40, 0.0275),
('a005', '215718002', 118955.23, 0.035),
('a006', '509429536', 292429.48, 0.05);

INSERT buyer VALUES
('buyer_1', '085669980'),
('buyer_2', '235090001'),
('b003', '578568678'),
('b004', '036078043'),
('b005', '587522934'),
('b006', '395404942'),
('b007', '001487368'),
('b008', '515827834'),
('b009', '520196480'),
('b010', '504342542'),
('b011', '021306756'),
('b012', '501286917'),
('b013', '008849203'),
('b014', '577228421'),
('b015', '389156190'),
('b016', '648227273');

INSERT owner VALUES
('owner_1', '506880757', 'b002', 'offer001'),
('o002', '085304579', 'b005', 'offer004'),
('o003', '393309045', 'b012', 'offer003'),
('o004', '522407366', 'b006', 'offer006'),
('o005', '003389041', 'b009', 'offer002'),
('o006', '640804931', 'b001', 'offer007'),
('o007', '059161255', 'b010', 'offer005'),
('o008', '574823410', 'b015', 'offer008');

INSERT property VALUES
('p001', 'Sold', 835000.00,  836000.00, '2016-10-26', '2016-11-28', 'o001', 'a001'),
('p002', 'Sold', 1068000.00, 1065000.00, '2015-03-22', '2016-10-21', 'o002', 'a001'),
('p003', 'On Sale', 1011169.00, 1011169.00, '2017-02-17', null, 'o003', 'a002'),
('p004', 'Sold', 830624, 830000, '2016-11-17', '2017-01-03', 'o003', 'a002'),
('p005', 'Sold', 1899500, 1900000, '2015-04-29', '2016-12-04', 'o004', 'a003'),
('p006', 'On Sale', 1275000, 1275000, '2016-05-19', null, 'o004', 'a004'),
('p007', 'Sold', 1349000, 1345000, '2015-06-05', '2016-04-05', 'o005', 'a005'),
('p008', 'On Sale', 589529, 589529, '2017-05-12', null, 'o005', 'a004'),
('p009', 'Sold', 776517, 780000, '2017-07-07', '2017-08-28', 'o006', 'a006'),
('p010', 'On Sale', 1489000, 1489000, '2017-08-25', null, 'o007', 'a002'),
('p011', 'On Sale', 1230000, 1230000, '2017-10-10', null, 'o007', 'a002'),
('p012', 'Sold', 950000, 950000, '2017-11-02', '2017-11-14', 'o007', 'a006'),
('p013', 'Sold', 119900, 1200000, '2016-09-06', '2017-10-29', 'o007', 'a006'),
('p014', 'On Sale', 784990, 764990, '2016-07-04', null, 'o008', 'a003'),
('p015', 'Sold', 815990, 780990, '2017-03-02', '2017-08-09', 'o008', 'a005'),
('p016', 'On Sale', 870990, 830990, '2017-09-21', null, 'o008', 'a001'),
('p017', 'On Sale', 2934789, 2934789, '2017-11-02', null, 'o008', 'a001'),
('p018', 'On Sale', 1799000, 1789000, '2017-10-07', null, 'o002', 'a003'),
('p019', 'On Sale', 1650000, 1555000, '2017-11-03', null, 'o001', 'a005');

INSERT property_parameter VALUES
('p001', 5, 3, 2, 5662, 'CA 95136', 'San Jose'),
('p002', 5, 2, 2, 3484, 'CA 95125', 'San Jose'),
('p003', 3, 3, 2, 2761, 'CA 95120', 'San Jose'),
('p004', 2, 2, 1, 831, 'CA 94103', 'San Francisco'),
('p005', 3, 2, 2, 1114, 'CA 94619', 'Oakland'),
('p006', 3, 2, 1, 1400, 'CA 94546', 'Castro Valley'),
('p007', 2, 1, 1, 1790, 'CA 94122', 'San Francisco'),
('p008', 3, 2, 1, 2518, 'CA 95006', 'Boulder Creek'),
('p009', 4, 4, 2, 3740, 'WA 98116', 'Seattle'),
('p010', 4, 4, 2, 2920, 'WA 98115', 'Seattle'),
('p011', 2, 2, 1, 1697, 'WA 98121', 'Seattle'),
('p012', 2, 2, 1, 1660, 'CA 91423', 'Los Angeles'),
('p013', 2, 1, 1, 1064, 'CA 90042', 'Los Angeles'),
('p014', 4, 3, 2, 2481, 'NV 89106', 'Las Vegas'),
('p015', 4, 5, 3, 4544, 'NV 89144', 'Las Vegas'),
('p016', 3, 3, 2, 1840, 'CA 94010', 'Burlingame'),
('p017', 3, 3, 2, 1820, 'CA 94109', 'San Francisco'),
('p018', 2, 2, 0, 1189, 'CA 94105', 'San Francisco');

INSERT open_house VALUES
('a002', 'oh001', '2017-03-20', '2017-05-20', 'p003'),
('a001', 'oh002', '2016-10-28', '2016-11-16', 'p001'),
('a004', 'oh003', '2016-05-25', '2016-07-26', 'p005'),
('a004', 'oh004', '2017-05-20', '2017-08-20', 'p007'),
('a002', 'oh005', '2017-08-25', '2017-10-25', 'p009'),
('a002', 'oh006', '2017-10-10', '2017-11-10', 'p010'),
('a003', 'oh007', '2016-08-04', '2016-09-04', 'p013'),
('a001', 'oh008', '2017-09-30', '2017-10-20', 'p015'),
('a001', 'oh009', '2017-11-07', '2017-11-18', 'p016'),
('a003', 'oh010', '2017-10-07', '2017-11-07', 'p017'),
('a005', 'oh011', '2017-11-03', '2017-11-13', 'p018');

INSERT offer VALUES
('b002', 'offer001', 835000.00, 'Deal', '2016-11-27', 'p001', 'a001'),
('b005', 'offer004', 1068000.00, 'Deal', '2016-10-18', 'p002', 'a001'),
('b012', 'offer003', 830624, 'Deal', '2017-01-01', 'p004', 'a002'),
('b006', 'offer006', 1275000, 'Progress', '2016-07-19', 'p006', 'a004'),
('b009', 'offer002', 1349000, 'Deal', '2016-03-28', 'p007', 'a005'),
('b001', 'offer007', 776517, 'Deal', '2017-08-20', 'p009', 'a006'),
('b010', 'offer005', 1230000, 'Progress', '2017-11-10', 'p011', 'a002'),
('b015', 'offer008', 815990, 'Deal', '2017-08-01', 'p015', 'a005');

/* ALTER TABLE owner ADD CONSTRAINT FK_owner_buyer_num FOREIGN KEY (buyer_num) REFERENCES offer(buyer_num);
ALTER TABLE owner ADD CONSTRAINT FK_owner_offer_num FOREIGN KEY (offer_num) REFERENCES offer(offer_num); */

INSERT oh_visit VALUES
('b002', 'a002', 'oh_1'),
('b010', 'a002', 'oh001'),
('b011', 'a001', 'oh002'),
('b003', 'a004', 'oh003'),
('b005', 'a004', 'oh004'),
('b013', 'a002', 'oh005'),
('b012', 'a002', 'oh006'),
('b009', 'a003', 'oh007'),
('b017', 'a003', 'oh007'),
('b002', 'a001', 'oh008'),
('b001', 'a001', 'oh009'),
('b014', 'a003', 'oh010'),
('b016', 'a005', 'oh011');


SET foreign_key_checks = 1;
