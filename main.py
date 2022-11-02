#-*- coding: utf-8 -*-
#
#          ITM           #
#        Catedra         #
# David Jimenez Murillo  #

# Cambiar tipo de dato de la imagen?

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import GUI
import time

class GUI(QtWidgets.QMainWindow, GUI.Ui_Form):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.browse_button.clicked.connect(self.get_dir)
        self.generate_button.clicked.connect(self.make_dl)
        self.bgnd_cb.stateChanged.connect(self.update_gui)
        self.crop_cb.stateChanged.connect(self.update_gui)
        self.resize_cb.stateChanged.connect(self.update_gui)
        self.load_mri_cb.stateChanged.connect(self.update_gui)
        self.load_labels_cb.stateChanged.connect(self.update_gui)
        self.dir = './data/train'

    def get_dir(self):

        self.dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Directory')
        self.path_edit.setText(self.dir)
        return

    def update_gui(self):

        if self.bgnd_cb.isChecked():
            self.up_slice_sb.setEnabled(False)
            self.low_slice_sb.setEnabled(False)
            self.crop_cb.setEnabled(False)
            self.low_slice_label.setEnabled(False)
            self.up_slice_label.setEnabled(False)
        else:
            self.up_slice_sb.setEnabled(True)
            self.low_slice_sb.setEnabled(True)
            self.crop_cb.setEnabled(True)
            self.low_slice_label.setEnabled(True)
            self.up_slice_label.setEnabled(True)

        if self.crop_cb.isChecked():
            self.bgnd_cb.setEnabled(False)
            self.up_slice_sb.setEnabled(True)
            self.low_slice_sb.setEnabled(True)
            self.low_slice_label.setEnabled(True)
            self.up_slice_label.setEnabled(True)
        else:
            self.bgnd_cb.setEnabled(True)
            self.up_slice_sb.setEnabled(False)
            self.low_slice_sb.setEnabled(False)
            self.low_slice_label.setEnabled(False)
            self.up_slice_label.setEnabled(False)

        if self.resize_cb.isChecked():
            self.width_spinbox.setEnabled(True)
            self.height_spinbox.setEnabled(True)
        else:
            self.width_spinbox.setEnabled(False)
            self.height_spinbox.setEnabled(False)

        if self.load_mri_cb.isChecked():
            self.mri_name_label.setEnabled(True)
            self.mri_name_le.setEnabled(True)
        else:
            self.mri_name_label.setEnabled(False)
            self.mri_name_le.setEnabled(False)

        if self.load_labels_cb.isChecked():
            self.label_name_label.setEnabled(True)
            self.label_name_le.setEnabled(True)
            if not self.crop_cb.isChecked():
                self.bgnd_cb.setEnabled(True)
        else:
            self.label_name_label.setEnabled(False)
            self.label_name_le.setEnabled(False)
            self.bgnd_cb.setEnabled(False)
            if self.bgnd_cb.isChecked():
                self.bgnd_cb.setChecked(False)


    def make_dl(self):

        with open('template.txt', 'r') as template:
            
            with open('dl.py', 'x') as dl:

                for line in template:

                    if "self.path = './data/train'" in line:
                        dl.write(line.replace('./data/train', self.dir))

                    elif "self.mri_name = 'T1.nii'" in line:
                        if self.load_mri_cb.isChecked():
                            dl.write(line.replace('T1.nii', self.mri_name_le.text()))
                        else:
                            dl.write(line)

                    elif "self.labels_name = None" in line:
                        if self.load_labels_cb.isChecked():
                            dl.write(line.replace('None', "'"+self.label_name_le.text()+"'"))
                        else:
                            dl.write(line)

                    elif "self.dims = False" in line:
                        if self.resize_cb.isChecked():
                            dl.write(line.replace('False', f'({self.width_spinbox.value()}, {self.height_spinbox.value()})', -1))
                        else:
                            dl.write(line)

                    elif "self.remove_bgnd = False" in line:
                        if self.bgnd_cb.isChecked():
                            dl.write(line.replace('False', 'True'))
                        else:
                            dl.write(line)

                    elif "self.crop = False" in line:
                        if self.crop_cb.isChecked():
                            dl.write(line.replace('False', f'({self.low_slice_sb.value()}, {self.up_slice_sb.value()})', -1))
                        else:
                            dl.write(line)

                    else:
                        dl.write(line)

        self.close()

        return

def main():

    app = QtWidgets.QApplication(sys.argv)
    form = GUI()
    form.show()
    app.exec_()

if __name__ == '__main__':

    main()
