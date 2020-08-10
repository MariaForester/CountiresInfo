drop table if exists countries_organisations, countries, organisations;

create table if not exists countries
(
    country_id   serial primary key,
    country_name varchar    not null,
    country_code varchar(3) not null
);

create table if not exists organisations
(
    organisation_id   serial primary key,
    organisation_acronym varchar not null,
    organisation_name varchar not null
);

create table if not exists countries_organisations
(
    country_organisation serial primary key,
    country_id           int not null,
    organisation_id      int not null,
    foreign key (country_id) references countries (country_id) on update cascade on delete restrict ,
    foreign key (organisation_id) references organisations(organisation_id) on update cascade on delete restrict
);