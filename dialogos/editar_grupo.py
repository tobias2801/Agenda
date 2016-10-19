# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit,
                                QHBoxLayout, QVBoxLayout, QSpinBox)


class EditGroupDialog(QDialog):

    def __init__(self, agenda, grupo_a_editar):
        super(EditGroupDialog, self).__init__()
        self.setMinimumSize(300, 150)
        self.setMaximumSize(300, 150)
        self.setWindowTitle(self.tr("Editar Grupo"))

        self.agenda = agenda
        self.grupo_a_editar = grupo_a_editar

        self.dibujar()
        self.layouts()

        self.render()

        self.btn_salir.clicked.connect(self.cerrar)
        self.btn_guardar.clicked.connect(self.guardar)

    def dibujar(self):

        self.label_id_grupo = QLabel(self.tr("ID grupo"), self)
        self.edit_id_grupo = QSpinBox(self)
        self.edit_id_grupo.setMaximum(100)
        self.edit_id_grupo.setFixedWidth(175)
        self.label_nombre_grupo = QLabel(self.tr("Nombre grupo"), self)
        self.edit_nombre_grupo = QLineEdit(self)
        self.edit_nombre_grupo.setFixedWidth(175)

        self.btn_salir = QPushButton(self.tr("Salir"), self)
        self.btn_guardar = QPushButton(self.tr("Guardar"), self)

    def layouts(self):

        layouts_label_edit = QHBoxLayout()
        layouts_label_edit.addWidget(self.label_nombre_grupo)
        layouts_label_edit.addWidget(self.edit_nombre_grupo)

        layouts_label_edit1 = QHBoxLayout()
        layouts_label_edit1.addWidget(self.label_id_grupo)
        layouts_label_edit1.addWidget(self.edit_id_grupo)

        layout_grl = QVBoxLayout(self)
        layout_grl.addSpacing(10)
        layout_grl.addLayout(layouts_label_edit1)
        layout_grl.addLayout(layouts_label_edit)
        layout_grl.addSpacing(15)
        layout_grl.addWidget(self.btn_guardar)
        layout_grl.addWidget(self.btn_salir)

        self.setLayout(layout_grl)

    def cerrar(self):
        self.close()

    def guardar(self):

        id_grupo = self.edit_id_grupo.value()
        nombre = self.edit_nombre_grupo.text()

        campo = 'nombre_grupo'
        criterio = self.grupo_a_editar[1]

        self.agenda.editar_grupo(campo, criterio, id_grupo, nombre)
        self.agenda.db.save()

        self.cerrar()

    def render(self):
        self.edit_nombre_grupo.setText(self.grupo_a_editar[1])
        self.edit_id_grupo.setValue(int((self.grupo_a_editar[0])))
