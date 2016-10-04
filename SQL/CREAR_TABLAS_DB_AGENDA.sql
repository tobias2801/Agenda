
CREATE TABLE contactos (
    id serial,
    nombre varchar(30),
    apellido varchar(30),
    email varchar(50),
    telefono varchar(11),
    grupo varchar(50)
);

CREATE TABLE grupos (
    id_grupo serial,
    nombre_grupo varchar(50)
);

ALTER TABLE contactos
ADD CONSTRAINT pk_contactos_id_tel_mail primary key (id, telefono, email);

ALTER TABLE contactos
ADD CONSTRAINT ck_email CHECK (
    email like '%@%.%'
);

ALTER TABLE contactos
ADD CONSTRAINT ck_telefono CHECK (
    -- xxxx-xxxxxx
    substring(telefono, 5, 1) in (' ', '-')
);

ALTER TABLE contactos
ADD CONSTRAINT fk_grupo foreign key(grupo) references grupos(nombre_grupo);

ALTER TABLE grupos
ADD CONSTRAINT pk_idgrupo primary key (id_grupo);

ALTER TABLE grupos
ADD CONSTRAINT uq_nombre unique(nombre_grupo);
