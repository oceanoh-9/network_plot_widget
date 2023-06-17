import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np
import mplcursors


def set_plot(
    FigSize=[15, 8],
    setdpi=300,
    num_row=1,
    num_col=1,
    fontstyle="calibri",
):
    mpl.rcParams["font.family"] = fontstyle

    fig, axs = plt.subplots(nrows=num_row, ncols=num_col, figsize=FigSize, dpi=setdpi)
    # ------end of subplot
    return fig, axs


# -------------------------- end of set_plot ----------


def first_plot(
    fig,
    axs,
    Xax,
    Yax,
    Xlab,
    Ylab,
    Legend="legend",
    TitleName="plot",
    Xlim=[0, 1],
    Ylim=[0, 1],
    Linewidth=2,
    Fontsize=20,
    marker="s",
    color="blue",
    Ticker="base",
):
    # -----------------plot the line
    axs.plot(Xax, Yax, color=color, linewidth=Linewidth, marker=marker, label=Legend)

    # axis scale
    axs.set_xlim(Xlim)
    axs.set_ylim(Ylim)

    axs.set_title(TitleName, fontsize=Fontsize)
    axs.set_xlabel(Xlab, fontsize=Fontsize)
    axs.set_ylabel(Ylab, fontsize=Fontsize)
    axs.legend(loc="best", fontsize=Fontsize)
    axs.grid(True)

    # -----------------format the tick
    if Ticker == "base":
        pass
    elif Ticker == "unit":
        axs.xaxis.set_major_formatter(tkr.FuncFormatter(format_tick))
    elif Ticker == "log":
        axs.set_xscale("log", base=10)
        locmajor = tkr.LogLocator(base=10, subs=np.arange(0, 1, 0.1), numticks=10)
        axs.xaxis.set_major_locator(locmajor)
    else:
        print("Wrong Ticker")

    # ----show the plot
    # plt.show()


# -------------------------------- end of first_plot ----------


def plot(
    fig,
    axs,
    Xax,
    Yax,
    Legend="legend",
    Linewidth=2,
    Fontsize=20,
    marker="s",
    color="blue",
):
    # -----------------plot the line
    axs.plot(Xax, Yax, color=color, linewidth=Linewidth, marker=marker, label=Legend)
    axs.legend(loc="best", fontsize=Fontsize)


# -----------------e----nd of plot


def format_tick(n, pos):
    if n >= 1e9:
        val, unit = divmod(n, 1e9)
        if unit == 0:
            return f"{val}G"
        else:
            return f"{val:.1f}G"
    elif n >= 1e6:
        val, unit = divmod(n, 1e6)
        if unit == 0:
            return f"{val}M"
        else:
            return f"{val:.1f}M"
    elif n >= 1000:
        val, unit = divmod(n, 1000)
        if unit == 0:
            return f"{val}k"
        else:
            return f"{val:.1f}k"
    elif n >= 1:
        return f"{n:.3f}"
    elif n >= 1e-3:
        return f"{n*1e3:.3f}m"
    elif n >= 1e-6:
        return f"{n*1e6:.3f}u"
    elif n >= 1e-9:
        return f"{n*1e9:.3f}n"
    elif n >= 1e-12:
        return f"{n*1e12:.3f}p"


# -------------------------- end of format_tick ----------

# # ----------------save file or show the plot
# if Do == "show":
#     plt.show()
#     # plt.hold()
# elif Do == "save":
#     plt.savefig(FileName)
# elif Do == "both":
#     plt.savefig(FileName)
#     plt.show()
# else:
#     print("Wrong input of 'Do'")
