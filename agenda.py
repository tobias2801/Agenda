# -*- coding: utf-8 -*-

from def_db import ConnectDB, DB_NAME, DB_USER, DB_PASS, json_querys


class Agenda():
    """Esta clase contiene los métodos necesarios para realizar las acciones
        asociadas a los cambios y búsquedas en la DB, para lo cual se provee
        de un objeto con conección, y utiliza las funciones de este,
        ampliándolas, con sus propios métodos"""

    def __init__(self):
        self.db = ConnectDB(DB_NAME, DB_USER, DB_PASS, json_querys)
        self.confirmacion = False

    def nuevo_contacto(self, nombre, apellido, email, telefono, grupo):
        nombre = nombre
        apellido = apellido
        email = email
        telefono = telefono
        grupo = grupo

        q = self.db.query('insertar', 'contactos')
        sql = q.format(nombre, apellido, email, telefono, grupo)

        self.db.run_query(sql)

    def nuevo_grupo(self, id_grupo, nombre_grupo):
        id_grupo = id_grupo
        nombre_grupo = nombre_grupo

        q = self.db.query('insertar', 'grupos')
        sql = q.format(id_grupo, nombre_grupo)

        self.db.run_query(sql)

    def editar_contacto(self, nombre, apellido, email, telefono, grupo,
                            campo_busqueda1, criterio_busqueda1, campo_busqueda2,
                            criterio_busqueda2):
        campo1 = campo_busqueda1
        criterio1 = criterio_busqueda1
        campo2 = campo_busqueda2
        criterio2 = criterio_busqueda2

        nombre = nombre
        apellido = apellido
        email = email
        telefono = telefono
        grupo = grupo

        q = self.db.query('editar', 'contactos')
        sql = q.format(nombre, apellido, email, telefono,
                        grupo, campo1, criterio1, campo2, criterio2)

        self.db.run_query(sql)

    def editar_grupo(self, campo_busqueda, criterio_busqueda, id_g, nombre):
        campo = campo_busqueda
        criterio = criterio_busqueda

        id_grupo = id_g
        nombre = nombre

        q = self.db.query('editar', 'grupos')
        sql = q.format(id_grupo, nombre, campo, criterio)

        self.db.run_query(sql)

    def _eliminar(self, campo_busqueda, criterio_busqueda, tabla):
        campo = campo_busqueda
        criterio = criterio_busqueda
        tabla = tabla

        q = self.db.query('eliminar', tabla)
        sql = q.format(campo, criterio)

        self.db.run_query(sql)
        self.db.save()

    def eliminar_contacto(self, campo_busqueda, criterio_busqueda):
        campo = campo_busqueda
        criterio = criterio_busqueda
        self._eliminar(campo_busqueda, criterio_busqueda, 'contactos')

    def eliminar_grupo(self, campo_busqueda, criterio_busqueda):
        campo = campo_busqueda
        criterio = criterio_busqueda
        self._eliminar(campo_busqueda, criterio_busqueda, 'grupos')

    def _buscar(self, criterio_busqueda, tabla):
        criterio = criterio_busqueda
        tabla = tabla

        q = self.db.query('buscar', tabla)
        sql = q.format(criterio)

        rows = self.db.run_query(sql)

        return rows

    def buscar_contacto(self, criterio_busqueda):
        criterio = criterio_busqueda

        contactos = self._buscar(criterio_busqueda, 'contactos')
        return contactos

    def buscar_grupo(self, criterio_busqueda):
        criterio = criterio_busqueda

        grupos = self._buscar(criterio_busqueda, 'grupos')
        return grupos

    def select_all(self, tabla):
        tabla = tabla
        rows = None
        if tabla == 'contactos':
            sql = self.db.query('select_all', 'contactos')
            rows = self.db.run_query(sql)
        elif tabla == 'grupos':
            sql = self.db.query('select_all', 'grupos')
            rows = self.db.run_query(sql)

        return rows
