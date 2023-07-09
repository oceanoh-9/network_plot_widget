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
class main(QWidget):
    current_Network = []

    def __init__(self):
        # ensure the execution of the inherited class's __init__()
        super().__init__()
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)
        self.canvas = gui_plot()
        self.model = model_list()
        self.ui.listView_data.setModel(self.model)
        self.setup_layout()

        self.ui.spinBox_S2M_start_port.setMinimum(1)
        self.ui.comboBox_port_order.setItemData(0, "even_odd")
        self.ui.comboBox_port_order.setItemData(1, "seq")
        self.setup_matplot_figure()
        self.setup_control()

    def setup_control(self):
        self.ui.Button_Read_SnP.clicked.connect(self.import_SnP)
        self.ui.Button_S2Mixed.clicked.connect(self.S2Mixed)
        self.ui.Button_plot.clicked.connect(self.test_plot_clicked)

    def setup_matplot_figure(self):
        # create a matplotlib figure
        self.toolbar = NavigationToolbar(self.canvas, self)
        # add the matplotlib widget to the main window
        self.ui.vLayout_mpl.addWidget(self.toolbar)
        self.ui.vLayout_mpl.addWidget(self.canvas)

    def setup_layout(self):
        self.setLayout(self.ui.vLayout_main)
        self.ui.tab_list.setLayout(self.ui.vLayout_tab_list)
        self.ui.tab_mixed_Spar.setLayout(self.ui.vLayout_tab_mixed_Spar)

    def import_SnP(self):
        num_port = 0
        self.ui.Label_Status.setText("Reading SnP file...")

        SnP_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", "./", "SnP files (*.s*p)"
        )

        if SnP_file_name[0] == "":
            self.ui.Label_Status.setText("Please choose SnP file")
        else:
            self.current_Network = snp.readsnp(SnP_file_name[0])
            num_port = self.current_Network.number_of_ports
            self.ui.spinBox_S2M_start_port.setMaximum(
                self.current_Network.number_of_ports
            )
            self.ui.Label_Show_Opened_File.setText(
                f'Current File: "{SnP_file_name[0]}" '
            )
            self.ui.Label_Status.setText("SnP file readed successfully")
        self.ui.Label_Status.setText("import data to list...")
        if num_port != 0:
            num_network = num_port**2
            self.model.mydata.clear()
            for i in range(num_network):
                row = i // num_port
                col = i % num_port
                self.model.mydata.append((0, row, col))
            self.model.layoutChanged.emit()
            self.ui.Label_Status.setText("import data to list successfully")
            num_port = 0

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


class model_list(QtCore.QAbstractListModel):
    def __init__(self, *args, mydata=None, **kwargs):
        super(model_list, self).__init__(*args, **kwargs)
        self.mydata = mydata or []
        """
        mydata[index.row] = [datatype, i, j]
        datatype: 0=S-par. 1=mmS-par. 
        i: row of the parameters
        j: column of the parameters
        """

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self.mydata)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.ItemDataRole.DisplayRole:
            datatype, i, j = self.mydata[index.row()]
            row = i + 1
            col = j + 1
            if datatype == 0:
                text = f"S{row}{col}"
                return text


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mw = main()
    mw.show()
    app.exec_()
