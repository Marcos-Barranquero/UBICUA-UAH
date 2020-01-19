drop table if exists Informes;
drop table if exists LecturasSensores;

create table LecturasSensores (
    fecha integer not null PRIMARY KEY,
    presion1 integer not null,
    presion2 integer not null,
    presion3 integer not null,
    pulsaciones integer not null,
    sesion integer not null
);

create table Informes (
    fecha integer not null PRIMARY KEY,
    datos text not null,
    sesion integer not null
);
