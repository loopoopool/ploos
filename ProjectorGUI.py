import numpy as np
import checkableComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog, doscar, canvas):
        self.doscar = doscar
        self.canvas = canvas
        self.linecounter = 0
        if not Dialog.objectName():
            Dialog.setObjectName(u"Projector")
        Dialog.resize(402, 368)
        self.horizontalLayout_3 = QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(Dialog)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setRange(1, doscar.natoms)

        self.horizontalLayout.addWidget(self.spinBox)

        self.horizontalSpacer = QSpacerItem(60, 40, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_2 = QSpinBox(Dialog)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setRange(1, doscar.natoms)

        self.horizontalLayout.addWidget(self.spinBox_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.orbitals = checkableComboBox.CheckableComboBox(Dialog) 
        self.orbitals.addItems( doscar.guiLabel )

        self.verticalLayout_2.addWidget(self.orbitals)
        
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.clicked.connect(self.clickAddLine)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.clicked.connect(self.clickRemoveLine)

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.clicked.connect(self.close)

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Projector", u"Projector", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Project onto atoms:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"from:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"to:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Project onto orbitals", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Line label:", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Add line", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Remove line", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi


    def clickAddLine(self):
        self.linecounter += 1
        atomlist = np.arange( self.spinBox.value()-1, self.spinBox_2.value() )
        orblist = self.orbitals.currentData()
        mylabel = self.lineEdit.text()
        self.canvas.axes.plot(self.doscar.energy, self.doscar.projector(atomlist, orblist), 
                color=self.canvas.colors[self.linecounter], label=mylabel)
        self.canvas.axes.legend(loc='best')
        self.canvas.draw()
        self.lineEdit.clear()

    def clickRemoveLine(self):
        if ( self.linecounter > 0 ):
            self.canvas.axes.get_legend().remove()
            self.canvas.axes.lines.pop(self.linecounter)
            self.canvas.axes.legend(loc='best')
            self.canvas.draw()
            self.linecounter -= 1


class AppProj(QDialog, Ui_Dialog):
    def __init__(self, doscar, canvas, parent=None):
        super(AppProj, self).__init__(parent)
        self.setupUi(self, doscar, canvas)

