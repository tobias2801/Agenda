# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QPushButton, QWidget, QGroupBox,
                        QRadioButton, QAction, QTableWidget, QToolBar,
                        QLineEdit, QLabel, QMessageBox, QTableWidgetItem,
                        QAbstractItemView)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt)
from agenda import Agenda
from nuevo_contacto import NewContactDialog
from nuevo_grupo import NewGroupDialog

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
                        mensaje, flags)

        if r == QMessageBox.Yes:
            return True
        elif r == QMessageBox.No:
            return False

    def delete_row(self, campo, criterio, criterio2):
        title = "Eliminar"
        message = u"Está seguro de que desea eliminar el {0}: {1} {2}"
        if self.visualizar == 'contactos':
            sms = message.format('contacto', criterio, criterio2)
        else:
            sms = message.format('grupo', criterio, criterio2)

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

        if rows:
            labels_contactos = ('Nombre', 'Apellido', 'Email', 'Teléfono', 'Grupo')
            labels_grupos = ('ID', 'Nombre')
            column_count = len(rows[0])
            self.tabla.setColumnCount(column_count)
            self.tabla.setRowCount(len(rows))

            if column_count == 5:
                self.tabla.setHorizontalHeaderLabels(labels_contactos)
            elif column_count == 2:
                self.tabla.setHorizontalHeaderLabels(labels_grupos)

            for i in range(0, len(rows)):
                fila = rows[i]

                for l in range(0, len(fila)):
                    elemento = str(fila[l])

                    nuevo_item = QTableWidgetItem(elemento)
                    self.tabla.setItem(i, l, nuevo_item)

        self.tabla.resizeColumnsToContents()

    def __mostrar(self, tabla):
        tabla = tabla
        rows = self.agenda.select_all(tabla)
        print(rows)
        self.render_tabla(rows)

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
            criterio2 = self.tabla.item(j, 1).text()
            if self.visualizar == 'contactos':
                i = self.delete_row('nombre', criterio, criterio2)
            elif self.visualizar == 'grupos':
                i = self.delete_row('nombre_grupo', criterio2, criterio)

            if i:
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
        self.mostrar_contactos()
        dialogo = NewContactDialog(self.agenda)
        dialogo.exec_()
        self.mostrar_contactos()

    def new_group(self):
        self.mostrar_grupos()
        dialogo = NewGroupDialog(self.agenda)
        dialogo.exec_()
        self.mostrar_grupos()

    def new(self):

        if self.visualizar == "contactos":
            self.new_contact()

        elif self.visualizar == "grupos":
            self.new_group()
