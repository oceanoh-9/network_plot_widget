import numpy as np
import skrf as rf
# import matplotlib.pyplot as plt
import snp as snp

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from UI import Ui_MainWidget
from plot import gui_plot


# class main(QtWidgets.QMainWindow):
class main(QtWidgets.QWidget):
    current_Network = []

    def __init__(self):
        # ensure the execution of the inherited class's __init__()
        super().__init__()
        self.ui = Ui_MainWidget()
        self.canvas = gui_plot()

        self.ui.setupUi(self)
        self.setup_layout()
        """
        tab0 = ui.tab0
        tab1 = ui.tab1
        tab0.setLayout(ui.verticalLayout_tab0)
        tab1.setLayout(ui.verticalLayout_tab1)
        """
        self.ui.spinBox_S2M_start_port.setMinimum(1)
        self.ui.comboBox_port_order.setItemData(0, "even_odd")
        self.ui.comboBox_port_order.setItemData(1, "seq")
        self.setup_matplot_figure()
        self.setup_control()

    def setup_matplot_figure(self):
        # create a matplotlib figure
        self.toolbar = NavigationToolbar(self.canvas, self)
        # add the matplotlib widget to the main window
        self.ui.verticalLayout_mpl.addWidget(self.toolbar)
        self.ui.verticalLayout_mpl.addWidget(self.canvas)

    def setup_layout(self):
        self.setLayout(self.ui.verticalLayout_main)
        self.ui.tab0.setLayout(self.ui.verticalLayout_tab0)
        self.ui.tab1.setLayout(self.ui.verticalLayout_tab1)

    def setup_control(self):
        self.ui.pushButton_Read_SnP.clicked.connect(self.read_SnP)
        self.ui.pushButton_S2Mixed.clicked.connect(self.S2Mixed)
        self.ui.pushButton_plot.clicked.connect(self.test_plot_clicked)

    def read_SnP(self):
        self.ui.Label_Status.setText("Reading SnP file...")
        SnP_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", "./", "SnP files (*.s*p)"
        )
        if SnP_file_name[0] == "":
            self.ui.Label_Status.setText("Please choose SnP file")
        else:
            self.current_Network = snp.readsnp(SnP_file_name[0])

            self.ui.spinBox_S2M_start_port.setMaximum(self.current_Network.number_of_ports)
            self.ui.Label_Show_Opened_File.setText(
                f'Current File: "{SnP_file_name[0]}" '
            )
            self.ui.Label_Status.setText("SnP file readed successfully")


    def S2Mixed(self):
        self.ui.Label_Status.setText(
            f'order of port is "{self.ui.comboBox_port_order.currentData()}"'
        )
        if self.current_Network.number_of_ports < 4:
            self.ui.Label_Status.setText(
                "Please choose a SnP file which port number is more than 4"
            )
        port_begin = self.ui.spinBox_S2M_start_port.value()
        order_of_port = self.ui.comboBox_port_order.currentData()

    def test_plot_clicked(self):
        if self.current_Network == []:
            self.ui.Label_Status.setText("Please choose SnP file")
            return
        else:
            # self.canvas.axs  = self.canvas.fig.add_subplot(111)
            self.canvas.axs.cla()
            self.canvas.draw()
            self.canvas.x = np.divide(self.current_Network.frequency.f, 1e9)
            self.canvas.y = self.current_Network.s_db[:, 0, 0]
            self.canvas.xlab = "Frequency (GHz)"
            self.canvas.ylab = "S11 (dB)"
            self.canvas.titleName = "Test for class canvas"
            self.canvas.legend = "S11"
            self.canvas.scale = "log"
            self.canvas.plot()
        # refresh canvas
        self.canvas.draw()





if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mw = main()
    mw.show()
    app.exec_()
