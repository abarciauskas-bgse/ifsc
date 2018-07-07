# (comp table)
# id
# town
# country
# year
# month
# month_day
CREATE TABLE comps (
    id          integer NOT NULL PRIMARY KEY,
    town        varchar(100) NOT NULL,
    country     varchar(100) NOT NULL,
    year        integer NOT NULL,
    month       integer NOT NULL,
    month_day   integer NOT NULL
);
