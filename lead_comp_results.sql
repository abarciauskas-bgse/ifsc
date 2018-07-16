CREATE TABLE lead_comp_results (
    id              bigint NOT NULL PRIMARY KEY,
    category        varchar(100) NOT NULL,
    comp_id         integer NOT NULL,
    comp_stage      varchar(100) NOT NULL,
    comp_stage_rank integer NOT NULL,
    athlete_id      integer NOT NULL,
    previous_heat   decimal,
    result          decimal NOT NULL 
);
