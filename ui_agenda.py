# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget,
                        QGroupBox, QRadioButton, QHBoxLayout, QAction,
                        QTableWidget, QToolBar, QLineEdit, QLabel, QMessageBox,
                        QTableWidgetItem)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt)
from agenda import Agenda


class AgendaMainWindow(QMainWindow):

    def __init__(self):
        super(AgendaMainWindow, self).__init__()
        self.setWindowTitle(self.tr("Agenda"))
        self.setMinimumSize(600, 400)

        # Instancia clase agenda
        self.agenda = Agenda()

        # Widget Central - Tabla de grupos y contactos
        self.tabla = QTableWidget(self)
        self.setCentralWidget(self.tabla)
        self.tabla.setEditTriggers(self.tabla.EditTriggers(0))

        # Variable que contiene lo que se visualiza en la tabla, y lo pasa
        # a las acciones de la toolbar
        self.visualizar = "contactos"

        self.__mostrar(self.visualizar)

        # Menu
        menu = self.menuBar()
        self._crear_acciones()
        self._crear_menu(menu)

        # Buscar
        self.lineedit_buscar = QLineEdit()
        self.lineedit_buscar.setPlaceholderText(self.tr("Buscar"))
        self.lineedit_buscar.setClearButtonEnabled(1)
        self.lineedit_buscar.setMaximumWidth(200)

        # Toolbar
        self.toolbar = QToolBar(self)

        self.toolbar.addAction(self.nuevo)
        self.toolbar.addAction(self.editar)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.eliminar)
        self.toolbar.addSeparator()

        self.toolbar.addWidget(self.lineedit_buscar)

        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Conexiones
        self.ver_contactos.triggered.connect(self.mostrar_contactos)
        self.ver_grupos.triggered.connect(self.mostrar_grupos)
        self.eliminar.triggered.connect(self.delete_contacto)

    def _crear_acciones(self):
        self.nuevo_contacto = QAction(self.tr("Contacto"), self)
        self.nuevo_grupo = QAction(self.tr("Grupo"), self)
        self.editar_contacto = QAction(self.tr("Contacto"), self)
        self.editar_grupo = QAction(self.tr("Grupo"), self)
        self.eliminar_contacto = QAction(self.tr("Contacto"), self)
        self.eliminar_grupo = QAction(self.tr("Grupo"), self)
        self.ver_contactos = QAction(self.tr("Contactos"), self)
        self.ver_grupos = QAction(self.tr("Grupos"), self)

        self.nuevo = QAction(self.tr("Nuevo"), self)
        self.nuevo.setShortcut("Ctrl+N")
        self.nuevo.setIcon(QIcon("recursos/iconos/nuevo.png"))
        self.editar = QAction(self.tr("Editar"), self)
        self.editar.setShortcut("Ctrl+E")
        self.editar.setIcon(QIcon("recursos/iconos/editar.png"))
        self.eliminar = QAction(self.tr("Eliminar"), self)
        self.eliminar.setShortcut("Ctrl+Del")
        self.eliminar.setIcon(QIcon("recursos/iconos/eliminar.png"))
        self.buscar = QAction(self.tr("Buscar"), self)
        self.buscar.setShortcut("Ctrl+F")

    def _crear_menu(self, menu_bar):
        menu_archivo = menu_bar.addMenu(self.tr("&Nuevo"))
        menu_archivo.addAction(self.nuevo_contacto)
        menu_archivo.addAction(self.nuevo_grupo)
        menu_archivo.addAction(self.buscar)

        menu_editar = menu_bar.addMenu(self.tr("&Editar"))
        menu_editar.addAction(self.editar_contacto)
        menu_editar.addAction(self.editar_grupo)

        menu_ver = menu_bar.addMenu(self.tr("&Ver"))
        menu_ver.addAction(self.ver_contactos)
        menu_ver.addAction(self.ver_grupos)

        menu_eliminar = menu_bar.addMenu(self.tr("&Eliminar"))
        menu_eliminar.addAction(self.eliminar_contacto)
        menu_eliminar.addAction(self.eliminar_grupo)

    def __confirmar(self, titulo, mensaje):
        titulo = titulo
        mensaje = mensaje

        flags = QMessageBox.Yes
        flags |= QMessageBox.No

        r = QMessageBox.information(self, self.tr(titulo),
                        self.tr(mensaje), flags)

        if r == QMessageBox.Yes:
            return True
        else:
            return False

    def delete_row(self, campo, criterio):
        title = "Eliminar"
        message = "Está seguro de que desea eliminar el {0}: {1}"
        if self.visualizar == 'contactos':
            sms = message.format('contacto', criterio)
        else:
            sms = message.format('grupo', criterio)

        confirmacion = self.__confirmar(title, sms)

        if confirmacion == True:
            if self.visualizar == "contactos":
                self.agenda.eliminar_contacto(campo, criterio)
            elif self.visualizar == "grupos":
                self.agenda.eliminar_grupo(campo, criterio)

            return True
        else:
            return False

    def render_tabla(self, rows):
        rows = rows

        labels_contactos = ('Nombre', 'Apellido', 'Email', 'Teléfono', 'Grupo')
        labels_grupos = ('Nombre',)
        column_count = len(rows[0])
        self.tabla.setColumnCount(column_count)
        self.tabla.setRowCount(len(rows))

        if column_count == 5:
            self.tabla.setHorizontalHeaderLabels(labels_contactos)
        elif column_count == 1:
            self.tabla.setHorizontalHeaderLabels(labels_grupos)

        for i in range(0, len(rows)):
            fila = rows[i]

            for l in range(0, len(fila)):
                elemento = fila[l]

                nuevo_item = QTableWidgetItem(elemento)
                self.tabla.setItem(i, l, nuevo_item)

    def __mostrar(self, tabla):
        tabla = tabla
        self.render_tabla(self.agenda.select_all(tabla))

    def mostrar_contactos(self):
        self.visualizar = 'contactos'
        self.__mostrar('contactos')

    def mostrar_grupos(self):
        self.visualizar = 'grupos'
        self.__mostrar('grupos')

    def delete_contacto(self):
        print(str(self.tabla.currentItem()))

    def buscar(self):
        pass
