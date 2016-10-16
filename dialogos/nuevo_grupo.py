from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit,
                                QHBoxLayout, QVBoxLayout, QSpinBox)


class NewGroupDialog(QDialog):

    def __init__(self, agenda):
        super(NewGroupDialog, self).__init__()
        self.setMinimumSize(300, 150)
        self.setMaximumSize(300, 150)
        self.setWindowTitle(self.tr("Nuevo Grupo"))

        self.agenda = agenda

        self.dibujar()
        self.layouts()

        self.btn_salir.clicked.connect(self.cerrar)
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_guardar_y_continuar.clicked.connect(self.guardar_y_continuar)

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
        self.btn_guardar_y_continuar = QPushButton(self.tr("Guardar y continuar"),
                                                    self)

    def layouts(self):

        layouts_label_edit = QHBoxLayout()
        layouts_label_edit.addWidget(self.label_nombre_grupo)
        layouts_label_edit.addWidget(self.edit_nombre_grupo)

        layouts_label_edit1 = QHBoxLayout()
        layouts_label_edit1.addWidget(self.label_id_grupo)
        layouts_label_edit1.addWidget(self.edit_id_grupo)

        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.btn_guardar)
        layout_btns.addWidget(self.btn_guardar_y_continuar)
        layout_btns1 = QVBoxLayout()
        layout_btns1.addLayout(layout_btns)
        layout_btns1.addWidget(self.btn_salir)

        layout_grl = QVBoxLayout(self)
        layout_grl.addSpacing(10)
        layout_grl.addLayout(layouts_label_edit1)
        layout_grl.addLayout(layouts_label_edit)
        layout_grl.addSpacing(15)
        layout_grl.addLayout(layout_btns1)

        self.setLayout(layout_grl)

    def cerrar(self):
        self.close()

    def guardar(self):
        self._guardar()
        self.cerrar()

    def guardar_y_continuar(self):
        self._guardar()
        self.edit_nombre_grupo.setText("")
        self.edit_id_grupo.setValue(0)
        self.edit_id_grupo.setFocus()

    def _guardar(self):

        id_grupo = self.edit_id_grupo.value()
        nombre = self.edit_nombre_grupo.text()

        self.agenda.nuevo_grupo(id_grupo, nombre)
        self.agenda.db.save()
