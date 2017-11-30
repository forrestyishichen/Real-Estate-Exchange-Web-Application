PROCEDURE `Register`(INOUT returnvalue VARCHAR(16),
                     IN ssn    CHAR(9),
                     IN uname  VARCHAR(100),
                     IN pass   VARCHAR(100),
                     IN bd     DATE,
                     IN addr   VARCHAR(100),
                     IN email  VARCHAR(100),
                     IN fn     VARCHAR(40), 
                     IN mi     VARCHAR(10),
                     IN ln     VARCHAR(40))
SET returnvalue = "failed";
IF username NOT IN (SELECT user_name FROM user) 
THEN
INSERT INTO user VALUES(ssn, uname, pass, bd, addr, email);
INSERT INTO name (uname, fn, mi, ln) 
SET returnvalue = "succeed";
END IF;
END