# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QPushButton, QWidget, QGroupBox,
                        QRadioButton, QAction, QTableWidget, QToolBar,
                        QLineEdit, QLabel, QMessageBox, QTableWidgetItem,
                        QAbstractItemView)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt)
from agenda import Agenda
from dialogos.nuevo_contacto import NewContactDialog

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
            # Hace que no se puedan editar los items en la tabla
        self.tabla.setEditTriggers(self.tabla.EditTriggers(0))
            # Hace que solo se puedan seleccionar filas enteras
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
            # Contiene el modo actual de seleccion
        self.selection_mode = self.tabla.setSelectionMode(
                                            QAbstractItemView.SingleSelection)

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
        self.accion_seleccion_simple.triggered.connect(self.seleccion_simple)
        self.accion_seleccion_multiple.triggered.connect(self.seleccion_multiple)
        self.eliminar.triggered.connect(self.delete)
        self.nuevo.triggered.connect(self.new)
        self.nuevo_contacto.triggered.connect(self.new_contact)
        self.nuevo_grupo.triggered.connect(self.new_group)

    def _crear_acciones(self):
        self.nuevo_contacto = QAction(self.tr("Contacto"), self)
        self.nuevo_grupo = QAction(self.tr("Grupo"), self)

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

        self.accion_seleccion_simple = QAction(self.tr("Simple"), self)
        self.accion_seleccion_multiple = QAction(self.tr("Múltiple"), self)

    def _crear_menu(self, menu_bar):
        menu_archivo = menu_bar.addMenu(self.tr("&Nuevo"))
        menu_archivo.addAction(self.nuevo_contacto)
        menu_archivo.addAction(self.nuevo_grupo)

        menu_ver = menu_bar.addMenu(self.tr("&Ver"))
        menu_ver.addAction(self.ver_contactos)
        menu_ver.addAction(self.ver_grupos)
        menu_ver_seleccion = menu_ver.addMenu(self.tr("Selección"))
        menu_ver_seleccion.addAction(self.accion_seleccion_simple)
        menu_ver_seleccion.addAction(self.accion_seleccion_multiple)

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

    def delete(self):
        data = self.tabla.selectionModel().selectedRows()
        rows = []
        for i in data:
            rows.append(i.row())

        rows.sort(reverse=True)

        for j in rows:
            criterio = self.tabla.item(j, 0).text()
            if self.visualizar == 'contactos':
                self.delete_row('nombre', criterio)
            elif self.visualizar == 'grupos':
                self.delete_row('nombre_grupo', criterio)

            self.tabla.removeRow(j)

    def buscar(self):
        pass

    def seleccion_simple(self):
        self.selection_mode = self.tabla.setSelectionMode(
                                            QAbstractItemView.SingleSelection)

    def seleccion_multiple(self):
        self.selection_mode = self.tabla.setSelectionMode(
                                            QAbstractItemView.MultiSelection)

    def new_contact(self):
        dialogo = NewContactDialog()
        dialogo.exec_()

    def new_group(self):
        dialogo = NewGroupDialog()
        dialogo.exec_()

    def new(self):

        if self.visualizar == "contactos":
            dialogo = NewContactDialog()

        elif self.visualizar == "grupos":
            dialogo = NewGroupDialog()

        dialogo.exec_()
