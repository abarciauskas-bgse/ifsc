CREATE TABLE athletes (
    id          integer NOT NULL PRIMARY KEY,
    first_name  varchar(100) NOT NULL,
    last_name   varchar(100) NOT NULL,
    city        varchar(100),
    nation      varchar(100),
    federation  varchar(100),
    birthdate   integer,
    weight      integer,
    height      integer
);