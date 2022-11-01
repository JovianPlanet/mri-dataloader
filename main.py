#-*- coding: utf-8 -*-
#
#          ITM           #
#        Catedra         #
# David Jimenez Murillo  #

# Anadir checkbox para incluir o descartar slices de solo background
# Cambiar tipo de dato de la imagen?
# Checkbox para resize antes de especificar nuevo tamano?

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
        self.dir = None

    def get_dir(self):

        self.dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Directory')
        self.path_edit.setText(self.dir)

        return

    def update_gui(self):

        if self.bgnd_cb.isChecked():
            self.up_slice_sb.setEnabled(False)
            self.low_slice_sb.setEnabled(False)
            self.crop_cb.setEnabled(False)
        else:
            self.up_slice_sb.setEnabled(True)
            self.low_slice_sb.setEnabled(True)
            self.crop_cb.setEnabled(True)

        if self.crop_cb.isChecked():
            self.bgnd_cb.setEnabled(False)
        else:
            self.bgnd_cb.setEnabled(True)


    def make_dl(self):

        with open('template.txt', 'r') as template:
            
            with open('dl.py', 'x') as dl:

                for line in template:

                    if "self.path = 'dir_path'" in line:

                        dl.write(line.replace('dir_path', self.dir))#(''.join(l[:-1], self.dir))

                    break

                if self.resize_cb.isChecked():

                    for line in template:

                        if 'self.dims = (dims)' in line:

                            dl.write(line.replace('(dims)', 
                                                  f'({self.width_spinbox.value()}, {self.height_spinbox.value()})', 
                                                  -1)
                            )

                else:

                    for line in template:

                        if 'self.dims = (dims)' in line or 'image = image.resize(self.dims)' in line:

                            dl.write(line.replace(''))


                    # elif 'self.ext = []' in line:

                    #     ext = []
                    #     s = ', '

                    #     if self.png_cb.isChecked():
                    #         ext.append("'png'")
                    #     if self.jpg_cb.isChecked():
                    #         ext.append("'jpg'")
                    #     if self.bmp_cb.isChecked():
                    #         ext.append("'bmp'")

                    #     dl.write(line.replace('[]', '[{}]'.format(s.join(ext))))

                    # elif 'self.transform = transforms' in line:

                    #     tr = []
                    #     s = ', '

                    #     if self.toGS_cb.isChecked():
                    #         tr.append('transforms.Grayscale()')
                    #     if self.toTensor_cb.isChecked():
                    #         tr.append('transforms.ToTensor()')

                    #     dl.write(line.replace('transforms', 'transforms.Compose([{}])'.format(s.join(tr))))

                    # else:

                    #     dl.write(line)

        return

def main():

    app = QtWidgets.QApplication(sys.argv)
    form = GUI()
    form.show()
    app.exec_()

if __name__ == '__main__':

    main()
