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
        self.setup_matplot_figure()
        self.ButtonClick()

    def ButtonClick(self):
        self.ui.Button_Read_SnP.clicked.connect(self.import_SnP)
        self.ui.Button_S2Mixed.clicked.connect(self.S2Mixed)
        self.ui.Button_plot.clicked.connect(self.plot_clicked)
        self.ui.Button_clear_select.clicked.connect(self.clear_select)
        self.ui.Button_select_all.clicked.connect(self.select_all)

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
        self.ui.comboBox_port_order.setItemData(1, "seq")
        self.ui.comboBox_port_order.setItemData(0, "even_odd")
        
        self.ui.comboBox_PlotOption.setItemData(0, "dB")
        self.ui.comboBox_PlotOption.setItemData(1, "Phase")
        self.ui.comboBox_PlotOption.setItemData(2, "Real part")
        self.ui.comboBox_PlotOption.setItemData(3, "Imagainary part")
        self.ui.comboBox_PlotOption.setItemData(4, "Magnitude")

    def clear_select(self):
        self.ui.listView_data.clearSelection()

    def select_all(self):
        self.ui.listView_data.selectAll()

    def import_SnP(self):
        num_datatype = 4
        num_port = 0
        self.maindata_cache = np.array([])
        self.ui.Label_Status.setText("Reading SnP file...")

        SnP_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", "./", "SnP files (*.s*p)"
        )

        if SnP_file_name[0] == "":
            self.ui.Label_Status.setText("Please choose SnP file")
            return
        else:
            self.current_Network = snp.readsnp(SnP_file_name[0])
            num_port = self.current_Network.number_of_ports
            self.ui.spinBox_S2M_start_port.setMaximum(
                self.current_Network.number_of_ports - 3
            )
            self.ui.Label_Show_Opened_File.setText(
                f'Current File: "{SnP_file_name[0]}" '
            )
            self.maindata_cache = np.empty([self.current_Network.frequency.npoints, num_port, num_port, num_datatype], dtype=complex)
            self.ui.Label_Status.setText("SnP file readed successfully")
        self.ui.Label_Status.setText("import data to list...")

        if self.ui.checkBox_Convert2ZY.isChecked():
            self.model.ListviewData.clear()
            print("Convert to ZY is selected")
            for j in range(3):
                num_network = num_port**2
                for i in range(num_network):
                    row = i // num_port
                    col = i % num_port
                    # datatype: 0=S-par. 1=Z-par. 2=Y-par. 3=mmS-par. 
                    self.model.ListviewData.append((j, row, col))
                    print(j, row, col)
                    print(f'datatype={j}, row={row}, col={col}')
                if j == 0:
                    self.maindata_cache[:, :, :, j] = self.current_Network.s
                elif j == 1:
                    self.maindata_cache[:, :, :, j] = self.current_Network.z
                elif j == 2:
                    self.maindata_cache[:, :, :, j] = self.current_Network.y
                self.ui.Label_Status.setText("import data to list successfully")
        else:
            if num_port != 0:
                num_network = num_port**2
                self.model.ListviewData.clear()
                for i in range(num_network):
                    row = i // num_port
                    col = i % num_port
                    self.model.ListviewData.append((0, row, col))
                self.maindata_cache[:, :, :, 0] = self.current_Network.s
                self.ui.Label_Status.setText("import data to list successfully")
        self.model.layoutChanged.emit()
        num_port = 0
        num_network = 0

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

    def plot_clicked(self):
        if self.current_Network == []:
            self.ui.Label_Status.setText("Please choose SnP file")
            return
        else:
            indexes = self.ui.listView_data.selectedIndexes()
            if indexes:
                if len(indexes) > 1:
                    self.canvas.ylab = ("")
                datatype, row, column = [], [], []
                for k in range(len(indexes)):
                    cache = self.model.ListviewData[indexes[k].row()]
                    datatype.append(cache[0])
                    row.append(cache[1])
                    column.append(cache[2])

                row = np.array(row)
                row += 1
                column = np.array(column)
                column += 1

                self.canvas.axs.cla()
                self.canvas.draw()
                self.canvas.x = np.divide(self.current_Network.frequency.f, 1e9)
                self.canvas.xlab = "Frequency (GHz)"
                self.canvas.titleName = "Test for plot multi option"
                # self.canvas.scale = "log"
                self.plot_option(datatype, row, column)
            else:
                self.ui.Label_Status.setText("Please select the data")
                return
        # refresh canvas
        self.canvas.draw()
        indexes = []
        return 
     
    def plot_option(self, datatype, row, column):
        index_PlotOption = self.ui.comboBox_PlotOption.currentIndex()
        print(f"index_PlotOption = {index_PlotOption}")
        """
        index_PlotOption: 0=dB 1=Phase 2=Real part 3=Imagainary part 4=Magnitude
        """
        if index_PlotOption == 0:
            # dB
            self.canvas.ylab = "dB"
            for j in range(len(datatype)):
                if datatype[j] == 0:
                    self.canvas.y = self.current_Network.s_db[
                        :, row[j] - 1, column[j] - 1
                    ] 
                    self.canvas.legend = f"S{row[j]}{column[j]}"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 1:
                    self.canvas.y = 20*np.log10(self.current_Network.z[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Z({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 2:
                    self.canvas.y = 20*np.log10(self.current_Network.y[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Y({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                else:
                    self.ui.Label_Status.setText("Invalid DataType..")
                    return
        elif index_PlotOption == 1:
            # Phase
            self.canvas.ylab = "Phase (deg)"
            for j in range(len(datatype)):
                if datatype[j] == 0:
                    self.canvas.y = np.angle(self.current_Network.s[
                        :, row[j] - 1, column[j] - 1
                    ], deg=True)
                    self.canvas.legend = f"S{row[j]}{column[j]}"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 1:
                    self.canvas.y = np.angle(self.current_Network.z[
                        :, row[j] - 1, column[j] - 1
                    ], deg=True)
                    self.canvas.legend = f"Z({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 2:
                    self.canvas.y = np.angle(self.current_Network.y[
                        :, row[j] - 1, column[j] - 1
                    ], deg=True)
                    self.canvas.legend = f"Y({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                else:
                    self.ui.Label_Status.setText("Invalid DataType..")
                    return
        elif index_PlotOption == 2:
            # Real part
            self.canvas.ylab = "Real part"
            for j in range(len(datatype)):
                if datatype[j] == 0:
                    self.canvas.y = np.real(self.current_Network.s[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"S{row[j]}{column[j]}"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 1:
                    self.canvas.y = np.real(self.current_Network.z[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Z({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 2:
                    self.canvas.y = np.real(self.current_Network.y[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Y({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                else:
                    self.ui.Label_Status.setText("Invalid DataType..")
                    return           
        elif index_PlotOption == 3:
            # Imagainary part
            self.canvas.ylab = "Imagainary part"
            for j in range(len(datatype)):
                if datatype[j] == 0:
                    self.canvas.y = np.imag(self.current_Network.s[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"S{row[j]}{column[j]}"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 1:
                    self.canvas.y = np.imag(self.current_Network.z[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Z({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 2:
                    self.canvas.y = np.imag(self.current_Network.y[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Y({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                else:
                    self.ui.Label_Status.setText("Invalid DataType..")
                    return
        elif index_PlotOption == 4:
            # Magnitude
            self.canvas.ylab = "Magnitude"
            for j in range(len(datatype)):
                if datatype[j] == 0:
                    self.canvas.y = np.abs(self.current_Network.s[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"S{row[j]}{column[j]}"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 1:
                    self.canvas.y = np.abs(self.current_Network.z[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Z({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                elif datatype[j] == 2:
                    self.canvas.y = np.abs(self.current_Network.y[
                        :, row[j] - 1, column[j] - 1
                    ])
                    self.canvas.legend = f"Y({row[j]},{column[j]})"
                    self.canvas.color = self.canvas.colors[j]
                    self.canvas.plot()
                else:
                    self.ui.Label_Status.setText("Invalid DataType..")
                    return
        else:
            self.ui.Label_Status.setText("Invalid PlotOption..")
            return


class model_list(QtCore.QAbstractListModel):
    def __init__(self, *args, ListviewData=None, **kwargs):
        super(model_list, self).__init__(*args, **kwargs)
        self.ListviewData = ListviewData or []
        """
        ListviewData[index.row] = [datatype, i, j]
        datatype: 0=S-par. 1=Z-par. 2=Y-par 3=mmS-par.
        i: row of the parameters
        j: column of the parameters
        """

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self.ListviewData)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.ItemDataRole.DisplayRole:
            datatype, i, j = self.ListviewData[index.row()]
            row = i + 1
            col = j + 1
            if datatype == 0:
                text = f"S({row},{col})"
                return text
            elif datatype == 1:
                text = f"Z({row},{col})"
                return text
            elif datatype == 2:
                text = f"Y({row},{col})"
                return text
                 


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mw = main()
    mw.show()
    app.exec_()
