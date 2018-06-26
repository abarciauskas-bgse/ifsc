CREATE TABLE athletes (
    id          integer NOT NULL PRIMARY KEY,
    first_name  varchar(100) NOT NULL,
    last_name   varchar(100) NOT NULL,
    city        varchar(100) NOT NULL,
    nation      varchar(100) NOT NULL,
    federation  varchar(100) NOT NULL,
    birthdate   integer NOT NULL,
    weight      integer NOT NULL,
    height      integer NOT NULL
);