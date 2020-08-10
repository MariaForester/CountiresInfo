TRUNCATE countries_organisations, countries, organisations restart identity;

INSERT INTO countries(country_name, country_code)
VALUES ('United States of America', 'USA'),
       ('Russian Federation', 'RUS'),
       ('Germany', 'DEU'),
       ('France', 'FRA'),
       ('Belarus', 'BLR'),
       ('Armenia', 'ARM'),
       ('Canada', 'CAN'),
       ('Croatia', 'HRV'),
       ('Uzbekistan', 'UZB'),
       ('Finland', 'FIN');

INSERT INTO organisations(organisation_acronym, organisation_name)
VALUES ('NATO', 'North Atlantic Treaty Organisation'),
       ('EU', 'European Union'),
       ('CSTO', 'Collective Security Treaty Organisation'),
       ('OSCE', 'Organisation for Security and Co-operation in Europe');
