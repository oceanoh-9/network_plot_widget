import matplotlib as mpl
from matplotlib.figure import Figure
import matplotlib.pyplot as pyplot
import matplotlib.ticker as tkr
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class gui_plot(FigureCanvas):
    def __init__(self):
        self.font_family = "calibri"
        self.dpi = 150
        self.figsize = [15, 8]
        self.num_row = 1
        self.num_col = 1
        self.figindex = 1
        self.fig = Figure()
        super().__init__(self.fig)

        self.x = []
        self.y = []

        self.xlab = "X"
        self.ylab = "Y"
        self.titleName = "plot"
        self.legend = " "
        self.linewidth = 2
        self.marker = " "
        self.color = "blue"
        self.fontsize = 12

        self.setunit = True
        self.ticker = 1.0
        self.scale = "base"
        self.grid = True

        mpl.rcParams["font.family"] = "calibri"
        self.axs = self.fig.add_subplot(self.num_row, self.num_col, self.figindex)

    def plot(self):
        self.axs.plot(
            self.x,
            self.y,
            linewidth=self.linewidth,
            marker=self.marker,
            color=self.color,
            label=self.legend,
        )

        self.axs.set_title(self.titleName, fontsize=self.fontsize)
        self.axs.set_xlabel(self.xlab, fontsize=self.fontsize)
        self.axs.set_ylabel(self.ylab, fontsize=self.fontsize)
        self.axs.legend(loc="best", fontsize=self.fontsize)
        self.axs.grid(self.grid)
        self.set_scale()
        self.axs.autoscale(enable=True, axis="both", tight=True)
        self.fig.tight_layout()

    def set_limit(self, xlim, ylim):
        self.axs.set_xlim(xlim)
        self.axs.set_ylim(ylim)

    def set_scale(self):
        if self.scale == "base":
            pass
        elif self.scale == "log":
            self.axs.set_xscale("log", base=10)
            locmajor = tkr.LogLocator(base=10, subs=np.arange(0, 1, 0.1), numdecs=0, numticks=10)
            self.axs.xaxis.set_major_locator(locmajor)
            # self.axs.xaxis.set_minor_formatter(tkr.NullFormatter())
            # self.axs.xaxis.set_major_formatter(tkr.FuncFormatter(self.format_func))
        else:
            print("Wrong ScaleName")
    
    def format_func(self,value, tick_number):
        return int(value)

if __name__ == "__main__" :
    print("good")