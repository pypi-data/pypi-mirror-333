# Form implementation generated from reading ui file 'upload_config_dialog_base.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_UploadConfigDialog:
  def setupUi(self, UploadConfigDialog):
    UploadConfigDialog.setObjectName('UploadConfigDialog')
    UploadConfigDialog.resize(786, 226)
    self.verticalLayout = QtWidgets.QVBoxLayout(UploadConfigDialog)
    self.verticalLayout.setObjectName('verticalLayout')
    self.mainVerticalLayout = QtWidgets.QVBoxLayout()
    self.mainVerticalLayout.setObjectName('mainVerticalLayout')
    self.parallelUploadsHorizontalLayout = QtWidgets.QHBoxLayout()
    self.parallelUploadsHorizontalLayout.setObjectName('parallelUploadsHorizontalLayout')
    self.numParallelLabel = QtWidgets.QLabel(parent=UploadConfigDialog)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.numParallelLabel.sizePolicy().hasHeightForWidth())
    self.numParallelLabel.setSizePolicy(sizePolicy)
    self.numParallelLabel.setObjectName('numParallelLabel')
    self.parallelUploadsHorizontalLayout.addWidget(self.numParallelLabel)
    self.numParallelComboBox = QtWidgets.QComboBox(parent=UploadConfigDialog)
    self.numParallelComboBox.setObjectName('numParallelComboBox')
    self.parallelUploadsHorizontalLayout.addWidget(self.numParallelComboBox)
    self.mainVerticalLayout.addLayout(self.parallelUploadsHorizontalLayout)
    self.projectContentsScrollArea = QtWidgets.QScrollArea(parent=UploadConfigDialog)
    self.projectContentsScrollArea.setWidgetResizable(True)
    self.projectContentsScrollArea.setObjectName('projectContentsScrollArea')
    self.scrollAreaWidgetContents = QtWidgets.QWidget()
    self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 750, 159))
    self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
    self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
    self.verticalLayout_3.setObjectName('verticalLayout_3')
    self.projectItemsVerticalLayout = QtWidgets.QVBoxLayout()
    self.projectItemsVerticalLayout.setObjectName('projectItemsVerticalLayout')
    self.measurementCheckBox = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
    self.measurementCheckBox.setChecked(True)
    self.measurementCheckBox.setObjectName('measurementCheckBox')
    self.projectItemsVerticalLayout.addWidget(self.measurementCheckBox)
    self.samplesCheckBox = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
    self.samplesCheckBox.setChecked(True)
    self.samplesCheckBox.setObjectName('samplesCheckBox')
    self.projectItemsVerticalLayout.addWidget(self.samplesCheckBox)
    self.proceduresCheckBox = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
    self.proceduresCheckBox.setChecked(True)
    self.proceduresCheckBox.setObjectName('proceduresCheckBox')
    self.projectItemsVerticalLayout.addWidget(self.proceduresCheckBox)
    self.instrumentsCheckBox = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
    self.instrumentsCheckBox.setChecked(True)
    self.instrumentsCheckBox.setObjectName('instrumentsCheckBox')
    self.projectItemsVerticalLayout.addWidget(self.instrumentsCheckBox)
    self.unidentifiedCheckBox = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
    self.unidentifiedCheckBox.setChecked(True)
    self.unidentifiedCheckBox.setObjectName('unidentifiedCheckBox')
    self.projectItemsVerticalLayout.addWidget(self.unidentifiedCheckBox)
    self.verticalLayout_3.addLayout(self.projectItemsVerticalLayout)
    self.projectContentsScrollArea.setWidget(self.scrollAreaWidgetContents)
    self.mainVerticalLayout.addWidget(self.projectContentsScrollArea)
    self.verticalLayout.addLayout(self.mainVerticalLayout)
    self.buttonBox = QtWidgets.QDialogButtonBox(parent=UploadConfigDialog)
    self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
    self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Save)
    self.buttonBox.setObjectName('buttonBox')
    self.verticalLayout.addWidget(self.buttonBox)

    self.retranslateUi(UploadConfigDialog)
    self.buttonBox.accepted.connect(UploadConfigDialog.accept) # type: ignore
    self.buttonBox.rejected.connect(UploadConfigDialog.reject) # type: ignore
    QtCore.QMetaObject.connectSlotsByName(UploadConfigDialog)

  def retranslateUi(self, UploadConfigDialog):
    _translate = QtCore.QCoreApplication.translate
    UploadConfigDialog.setWindowTitle(_translate('UploadConfigDialog', 'Configure project upload'))
    UploadConfigDialog.setToolTip(_translate('UploadConfigDialog', 'Select the configuration parameters used for dataverse upload.'))
    self.numParallelLabel.setText(_translate('UploadConfigDialog', 'No of parallel uploads'))
    self.numParallelComboBox.setToolTip(_translate('UploadConfigDialog', 'Choose the number of parallel dataverse uploads.'))
    self.projectContentsScrollArea.setToolTip(_translate('UploadConfigDialog', 'Select the sub-items in a project to be uploaded to dataverse.'))
    self.measurementCheckBox.setText(_translate('UploadConfigDialog', 'Measurements'))
    self.samplesCheckBox.setText(_translate('UploadConfigDialog', 'Samples'))
    self.proceduresCheckBox.setText(_translate('UploadConfigDialog', 'Procedures'))
    self.instrumentsCheckBox.setText(_translate('UploadConfigDialog', 'Instruments'))
    self.unidentifiedCheckBox.setText(_translate('UploadConfigDialog', 'Unidentified'))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UploadConfigDialog = QtWidgets.QDialog()
    ui = Ui_UploadConfigDialog()
    ui.setupUi(UploadConfigDialog)
    UploadConfigDialog.show()
    sys.exit(app.exec())
