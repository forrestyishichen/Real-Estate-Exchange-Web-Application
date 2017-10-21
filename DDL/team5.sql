SET foreign_key_checks = 0;
drop database if exists teamfive;
create database teamfive;
use teamfive;

CREATE TABLE user (
  ssn        char(9) not null,
  user_name  varchar(25) not null,
  password   varchar(25) not null,
  fname      varchar(15) not null, 
  minit      varchar(1),
  lname      varchar(15) not null,
  bdate      date,
  address    varchar(50),
  email      varchar(25) not null,
  primary key (ssn),
  unique (user_name, email)
);

CREATE TABLE user_phone (
  ssn     char(9) not null,
  phone   varchar(15),
  primary key (ssn, phone),
  foreign key (ssn) references user(ssn)
   on delete cascade
);

CREATE TABLE owner (
  owner_num  varchar(15) not null,
  ssn        char(9) not null,
  buyer_num  varchar(15) not null,
  offer_num  varchar(15) not null,
  primary key (owner_num),
  foreign key (ssn) references user(ssn)
   on delete cascade,
  foreign key (buyer_num,offer_num) references offer(buyer_num,offer_num)
   on delete set null
);

CREATE TABLE agent (
  agent_num        varchar(15) not null,
  ssn              char(9) not null,
  total_commission decimal(10,2),
  commission_rate  decimal(3,2) check (commission_rate > 0 and commission_rate < 1), 
  primary key (agent_num),
  foreign key (ssn) references user(ssn)
   on delete cascade
);

CREATE TABLE buyer (
  buyer_num  varchar(15) not null,
  ssn        char(9) not null,
  primary key (buyer_num),
  foreign key (ssn) references user(ssn)
   on delete cascade
);

CREATE TABLE property (
  property_id  varchar(15) not null,
  status       varchar(15) not null,
  price        decimal(15,2) check (price > 0),
  asking_price decimal(15,2) check (asking_price > 0),
  room_num     integer,
  bath_num     integer,
  garage_num   integer,
  lot_size     integer,
  zip_code     varchar(15),
  area         varchar(15),
  list_date    date,
  sold_date    date,
  owner_num    varchar(15) not null,
  agent_num    varchar(15) not null,
  primary key (property_id),
  foreign key (owner_num) references owner(owner_num)
   on delete set null,
  foreign key (agent_num) references agent(agent_num)
   on delete set null
);

CREATE TABLE open_house (
  agent_num    varchar(15) not null,
  oh_num       varchar(15) not null,
  start_date   date,
  end_date     date,
  property_id  varchar(15) not null,
  primary key (agent_num, oh_num),
  foreign key (agent_num) references agent(agent_num)
   on delete cascade,
  foreign key (property_id) references property(property_id)
   on delete cascade
);

CREATE TABLE offer (
  buyer_num   varchar(15) not null,
  offer_num   varchar(15) not null,
  price       decimal(15,2) check (price > 0),
  status      varchar(15) not null,
  offer_date  date,
  property_id varchar(15) not null,
  agent_num   varchar(15) not null,
  primary key (buyer_num, offer_num),
  foreign key (buyer_num) references buyer(buyer_num)
   on delete cascade,
  foreign key (property_id) references property(property_id)
   on delete cascade,
  foreign key (agent_num) references agent(agent_num)
   on delete cascade
);

CREATE TABLE oh_visit (
  buyer_num   varchar(15) not null,
  agent_num    varchar(15) not null,
  oh_num       varchar(15) not null,
  primary key (buyer_num, agent_num, oh_num),
  foreign key (buyer_num) references buyer(buyer_num)
   on delete cascade,
  foreign key (agent_num, oh_num) references open_house(agent_num, oh_num)
   on delete cascade
);

#insert


SET foreign_key_checks = 1;

