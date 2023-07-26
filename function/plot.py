import matplotlib as mpl
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
import matplotlib.ticker as tkr
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class gui_plot(FigureCanvas):
    def __init__(self):
        #self.font_family = "calibri"
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
        self.linewidth = 1
        self.marker = " "
        self.color = "blue"
        self.colors = []
        self.set_colors()
        self.fontsize = 16

        self.setunit = True
        self.ticker = 1.0
        self.scale = "base"
        self.grid = True

        #mpl.rcParams["font.family"] = "calibri"
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
            locmajor = tkr.LogLocator(
                base=10, subs=np.arange(0, 1, 0.1), numdecs=0, numticks=10
            )
            self.axs.xaxis.set_major_locator(locmajor)
            # self.axs.xaxis.set_minor_formatter(tkr.NullFormatter())
            # self.axs.xaxis.set_major_formatter(tkr.FuncFormatter(self.format_func))
        else:
            print("Wrong ScaleName")

    def format_func(self, value, tick_number):
        return int(value)

    def set_colors(self):
        self.colors = [
            "#ff0000", # red
            "#0000ff", # blue
            "#ff00ff", # pink
            "#00ffff", # cyian

            "#009933", # green
            "#ff8000", # orange
            "#9933ff", # purple
            "#663300", # brown

            "#ff9999", # light red
            "#9999ff", # light blue
            "#ff99ff", # light pink
            "#99ffff", # light cyian

            "#800000", #darker red
            "#000080", #darker blue
            "#800080", #darker pink
            "#008080", #darker cyian

            "#99ff99", # light green
            "#ffcc99", # light orange
            "#ff99cc", # light purple
            "#cc9966", # light brown

            "#006600", #darker green
            "#cc6600", #darker orange
            "#6600cc", #darker purple
            "#4d2600", #darker brown
        ]
        


if __name__ == "__main__":
    print("good")
