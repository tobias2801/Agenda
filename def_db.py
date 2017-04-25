# -*- coding: utf-8 -*-

import psycopg2
import json

DB_NAME = 'Agenda'
DB_USER = 'user'
DB_PASS = 'pass'


with open("querys.json") as f:
    json_querys = json.load(f)


class ConnectDB():
    """Esta clase sirve para obtener un objeto conectado a la DB, y los métodos
        necesarios para seleccionar el query necesario del archivo json,
        ejecutarlo, guardar los cambios, y cerrar la conección"""

    def __init__(self, dbname, user, password, query_s):
        data = "dbname={0} user={1} password={2}".format(dbname, user,
                                                             password)

        self.conx, self.cursor = self.__create_connection(data)
        self.op_querys = query_s

    def __create_connection(self, data):
        try:
            conx = psycopg2.connect(data)
            cursor = conx.cursor()
            return conx, cursor
        except:
            print("Error al conectarse o crear el cursor")

    def run_query(self, query):
        if query.startswith('SELECT'):
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        else:
            self.cursor.execute(query)

    def close(self):
        self.cursor.close()

    def save(self):
        self.conx.commit()

    def query(self, accion, tabla):
        if tabla == 'contactos':
            if accion == 'editar':
                query_s = self.op_querys['UPDATE'][0]['update_contactos']
            elif accion == 'buscar':
                query_s = self.op_querys['SELECT'][0]['select_contactos']
            elif accion == 'eliminar':
                query_s = self.op_querys['DELETE'][0]['delete_contactos']
            elif accion == 'insertar':
                query_s = self.op_querys['INSERT'][0]['insert_contactos']
            elif accion == 'select_all':
                query_s = self.op_querys['SELECT'][0]['select_conctactos_all']
            else:
                query_s = False

        elif tabla == 'grupos':
            if accion == 'editar':
                query_s = self.op_querys['UPDATE'][1]['update_grupos']
            elif accion == 'buscar':
                query_s = self.op_querys['SELECT'][1]['select_grupos']
            elif accion == 'eliminar':
                query_s = self.op_querys['DELETE'][1]['delete_grupos']
            elif accion == 'insertar':
                query_s = self.op_querys['INSERT'][1]['insert_grupos']
            elif accion == 'select_all':
                query_s = self.op_querys['SELECT'][1]['select_grupos_all']
            elif accion == 'nombre_grupos':
                query_s = self.op_querys['SELECT'][1]['select_nombre_grupos']
            else:
                query_s = False

        return query_s
