# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QPushButton, QLabel, QDialog, QLineEdit, QComboBox,
                            QVBoxLayout, QHBoxLayout, QFormLayout)

class NewContactDialog(QDialog):
    """Ventana que contiene el formulario para la creación de un
        nuevo contacto."""

    def __init__(self, agenda):
        super(NewContactDialog, self).__init__()
        self.setMinimumSize(300, 300)
        self.setMaximumSize(300, 300)

        self.agenda = agenda

        self.dibujar()
        self.layouts()

            # Agregar los nombres de los grupos al combobox
        sql = self.agenda.db.query('nombre_grupos', 'grupos')
        rows = self.agenda.db.run_query(sql)
        for i in range(len(rows)):
            nombre_grupo = str(rows[i][0])
            self.edit_grupo.addItem(nombre_grupo)

            # Connections
        self.btn_limpiar.clicked.connect(self.limpiar)
        self.btn_salir.clicked.connect(self.cerrar)
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_guardar_y_continuar.clicked.connect(self.guardar_y_continuar)

    def dibujar(self):

            # Line Edits
        self.edit_nombre = QLineEdit(self)
        self.edit_nombre.setFixedWidth(200)
        self.edit_apellido = QLineEdit(self)
        self.edit_apellido.setFixedWidth(200)
        self.edit_email = QLineEdit(self)
        self.edit_email.setFixedWidth(200)
        self.edit_telefono = QLineEdit(self)
        self.edit_telefono.setFixedWidth(200)
        self.edit_grupo = QComboBox(self)
        self.edit_grupo.setFixedWidth(200)

            # Labels
        self.label_nombre = QLabel("Nombre:", self)
        self.label_apellido = QLabel("Apellido", self)
        self.label_email = QLabel("E-mail", self)
        self.label_telefono = QLabel("Teléfono", self)
        self.label_grupo = QLabel("Grupo", self)

            # Botones
        self.btn_guardar = QPushButton(self.tr("Guardar"), self)
        self.btn_guardar_y_continuar = QPushButton(self.tr("Guardar y continuar"), self)
        self.btn_limpiar = QPushButton(self.tr("Limpiar"), self)
        self.btn_salir = QPushButton(self.tr("Salir"), self)

    def layouts(self):

            # Layouts
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.btn_guardar)
        layout_btns.addWidget(self.btn_guardar_y_continuar)
        layout_btns2 = QHBoxLayout()
        layout_btns2.addWidget(self.btn_limpiar)
        layout_btns2.addWidget(self.btn_salir)

        layout_nombre = QHBoxLayout()
        layout_nombre.addWidget(self.label_nombre)
        layout_nombre.addWidget(self.edit_nombre)

        layout_apellido = QHBoxLayout()
        layout_apellido.addWidget(self.label_apellido)
        layout_apellido.addWidget(self.edit_apellido)

        layout_email = QHBoxLayout()
        layout_email.addWidget(self.label_email)
        layout_email.addWidget(self.edit_email)

        layout_telefono = QHBoxLayout()
        layout_telefono.addWidget(self.label_telefono)
        layout_telefono.addWidget(self.edit_telefono)

        layout_grupo = QHBoxLayout()
        layout_grupo.addWidget(self.label_grupo)
        layout_grupo.addWidget(self.edit_grupo)

        layout_labels_edits = QVBoxLayout()
        layout_labels_edits.addLayout(layout_nombre)
        layout_labels_edits.addLayout(layout_apellido)
        layout_labels_edits.addLayout(layout_email)
        layout_labels_edits.addLayout(layout_telefono)
        layout_labels_edits.addLayout(layout_grupo)
        layout_labels_edits.addLayout(layout_btns)
        layout_labels_edits.addLayout(layout_btns2)

        layoutg1 = QHBoxLayout(self)
        layoutg1.addLayout(layout_labels_edits)

        self.setLayout(layoutg1)

    def cerrar(self):
        self.close()

    def limpiar(self):
        self.edit_nombre.setText("")
        self.edit_apellido.setText("")
        self.edit_email.setText("")
        self.edit_telefono.setText("")
        self.edit_grupo.setCurrentIndex(0)
        self.edit_nombre.setFocus()

    def _guardar(self):
        nombre = self.edit_nombre.text()
        apellido = self.edit_apellido.text()
        email = self.edit_email.text()
        telefono = self.edit_telefono.text()
        grupo = self.edit_grupo.currentText()

        self.agenda.nuevo_contacto(nombre, apellido, email, telefono, grupo)
        self.agenda.db.save()

    def guardar(self):
        self._guardar()
        self.cerrar()

        return True

    def guardar_y_continuar(self):
        self._guardar()
        self.limpiar()
