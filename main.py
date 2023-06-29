import plot as fplt
import numpy as np
import skrf as rf
import matplotlib.pyplot as plt
import snp as snp

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from UI import Ui_Mainwindow


# class main(QtWidgets.QMainWindow):
class main(QtWidgets.QWidget):
    # setup global variable
    S_mag = []
    Frequency = []
    Z0 = 50
    my_Network = []
    port_num = 0

    # create a constructor for the main class
    def __init__(self):
        # ensure the execution of the inherited class's __init__()
        super().__init__()
        self.ui = Ui_Mainwindow()
        # setWindow
        self.ui.setupUi(self)
        # set main Layout
        self.setLayout(self.ui.verticalLayout_main)

        self.ui.spinBox_S2M_start_port.setMinimum(1)
        self.ui.comboBox_port_order.setItemData(0, "even_odd")
        self.ui.comboBox_port_order.setItemData(1, "seq")

        # create a matplotlib figure
        self.figure = Figure()
        self.figure.set_dpi(200)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # add the matplotlib widget to the main window
        self.ui.verticalLayout_mpl.addWidget(self.toolbar)
        self.ui.verticalLayout_mpl.addWidget(self.canvas)

        # run the setup_control function
        self.setup_control()

    # -----------end of __init__()--------

    def setup_control(self):
        self.ui.pushButton_Read_SnP.clicked.connect(self.read_SnP)
        self.ui.pushButton_S2Mixed.clicked.connect(self.S2Mixed)
        self.ui.pushButton_plot.clicked.connect(self.plot_clicked)

    # -----------end of setup_control()--------

    def read_SnP(self):
        self.ui.Label_Status.setText("Reading SnP file...")
        SnP_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", "./", "SnP files (*.s*p)"
        )
        if SnP_file_name[0] == "":
            self.ui.Label_Status.setText("Please choose SnP file")
        else:
            self.my_Network = snp.readsnp(SnP_file_name[0])
            self.S_mag = self.my_Network.s
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
        self.ui.Label_Status.setText(
            f'order of port is "{self.ui.comboBox_port_order.currentData()}"'
        )
        if self.port_num < 4:
            self.ui.Label_Status.setText("Please choose a SnP file which port number is more than 4")
        port_begin = self.ui.spinBox_S2M_start_port.value()
        order_of_port = self.ui.comboBox_port_order.currentData()

    def plot_clicked(self):
        ax = self.figure.add_subplot(111)
        ax.clear()

        if self.my_Network == []:
            self.ui.Label_Status.setText("Please choose SnP file")
            return
        else:
            fplt.first_plot(
                fig=self.figure,
                axs=ax,
                Xax=self.Frequency,
                Yax=self.S_mag[:, 0, 0],
                Xlab="Frequency (Hz)",
                Ylab="S11 (dB)",
                TitleName="Test for embedding mpl in UI",
                autolim=True,
                Legend="S11",
                Linewidth=1,
                Fontsize=10,
                marker="",
                Ticker="log",
            )
            self.ui

        # refresh canvas
        self.canvas.draw()

    # -----------end of plot_clicked()--------


# -----------end of class main()--------


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mw = main()
    mw.show()
    app.exec_()
