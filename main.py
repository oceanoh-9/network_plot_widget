import typing
from PyQt5.QtWidgets import QWidget
import plot as plt
import numpy as np
import skrf as rf
import matplotlib.pyplot as plt
import snp as snp

from PyQt5 import QtCore, QtGui, QtWidgets
from UI import Ui_Mainwindow


class main(QtWidgets.QMainWindow):
    # setup global variable
    Sparameter = []
    Frequency = []
    Z0 = 50
    my_Network = []
    port_num = 0

    # Create a constructor for the main class
    def __init__(self):
        # Ensure the execution of the inherited class's __init__()
        super().__init__()
        self.ui = Ui_Mainwindow()
        # setWindow
        self.ui.setupUi(self)
        # set Layout
        self.ui.spinBox_S2M_start_port.setValue(1)
        self.ui.comboBox_port_order.setItemData(0, "even_odd")
        self.ui.comboBox_port_order.setItemData(1, "seq")
        # run the setup_control function
        self.setup_control()

    # -----------end of __init__()--------

    def setup_control(self):
        # connect to the function when pushButton_Read_SnP is clicked
        self.ui.pushButton_Read_SnP.clicked.connect(self.read_SnP)
        # connect to the function when pushButton_S2Mixed is clicked
        self.ui.pushButton_S2Mixed.clicked.connect(self.S2Mixed)

    # -----------end of setup_control()--------

    def read_SnP(self):
        self.ui.Label_Status.setText("Reading SnP file...")
        SnP_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", "./", "SnP files (*.s*p)"
        )
        if SnP_file_name[0] == "":
            self.ui.Label_Status.setText("Please choose SnP file")
        else:
            self.my_Network = snp.readsnp(
                SnP_file_name[0]
            )
            self.Sparameter = self.my_Network.s
            self.Frequency = self.my_Network.f
            self.Z0 = self.my_Network.z0
            self.port_num = self.my_Network.number_of_ports

            self.ui.spinBox_S2M_start_port.setMaximum(self.port_num)
            self.ui.Label_Show_Opened_File.setText(
                f'Current File: "{SnP_file_name[0]}" '
            )
            self.ui.Label_Status.setText("SnP file readed successfully")

    # -----------end of read_SnP()--------

    def S2Mixed(self):
        self.ui.Label_Status.setText(f'order of port is "{self.ui.comboBox_port_order.currentData()}"')
    #     if self.port_num < 4:
    #         self.ui.Label_Status.setText("Please choose a SnP file which port number is more than 4")
    #     port_begin = self.ui.spinBox_S2M_start_port.value()
    #     order_of_port = self.ui.comboBox_port_order.currentData()


# -----------end of class main()--------

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mw = main()
    mw.show()
    app.exec_()
