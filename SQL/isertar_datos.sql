insert into contactos (nombre, apellido, email, telefono, grupo) values ('joel', 'Schwarz', 'joelsch@gmail.com', '3445-181684', 'grupo1');
insert into contactos (nombre, apellido, email, telefono, grupo) values ('hugo', 'Schwarz', 'hugo@hotmail.com', '3446-685444', 'grupo2');
insert into contactos (nombre, apellido, email, telefono, grupo) values ('lorena', 'herman', 'lorenah@gmail.com', '3445-165245', 'grupo3');
insert into contactos (nombre, apellido, email, telefono, grupo) values ('pepe', 'salazar', 'ppslz@yahoo.com', '3446-687478', 'grupo3');
insert into contactos (nombre, apellido, email, telefono, grupo) values ('juan', 'gonzales', 'juancito@hotmail.com', '3442-234648', 'grupo1');

insert into grupos values (2801, 'grupo1');
insert into grupos values (2001, 'grupo2');
insert into grupos values (2903, 'grupo3');

select * from contactos;

select * from grupos;

select nombre, apellido, grupo from contactos where grupo like 'grupo_';
