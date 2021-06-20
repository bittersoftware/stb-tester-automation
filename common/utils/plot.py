import matplotlib.pyplot as plt
import time
import datetime

X_LABEL = "Time (s)"


class PlotBarChart:
    """Generates a bar chart using

    Attributes:
    - data: array of floats
    - fname: string: file name [Default: epoch time]
    - treshold: int or float: paints bar as red if bigger than threshold
    - title: string: titlte of the chart

    Method:
    Saves chart png image when constructed
    """

    def __init__(self, data, treshold=None, fname=None, title=None):
        """__init__

        Args:
            data (list): list of floats
            treshold (int/float, optional): paints bar in red if greater than threshold.
            Defaults to None.
            fname (string, optional): file name [Default: epoch time]. Defaults to None.
            title (string, optional): title of the chart. Defaults to "KPI".
        """
        self.data = data
        self.fname = fname
        self.treshold = treshold
        self.title = title
        self.generate_chart()

    def generate_chart(self):
        assert len(self.data) > 0, "Invalid number of digits. Must be 3 digits"
        assert all(
            isinstance(number, float) or isinstance(number, int) for number in self.data
        ), "All digits must be float or ints"

        if not self.fname:
            self.fname = "{}.png".format(time.time())

        plt.style.use("ggplot")

        x_pos = [i for i, _ in enumerate(self.data)]
        x_axis = [str(i + 1) for i, _ in enumerate(self.data)]

        if self.treshold:
            clrs = ["grey" if (x < self.treshold) else "red" for x in self.data]
        else:
            clrs = ["grey"]

        if self.title:
            plt.title(self.title)
        else:
            plt.title("KPI")

        plt.xlabel("Execution")
        plt.ylabel(X_LABEL)

        plt.bar(x_axis, self.data, color=clrs, width=0.4)
        plt.xticks(x_pos, x_axis)

        plt.savefig(self.fname)
        plt.close()


class CreateVodChart:
    def __new__(cls, config, data):
        if all(k in config for k in ("ylimitMax", "ylimitMax")) and (len(data) > 0):
            return super(CreateVodChart, cls).__new__(cls)
        else:
            raise ValueError

    def __init__(self, config, data):
        """
        Class that uses the data passed by parameter to generate a graph with the
        specified format of the config file, which is also passed by parameter.
        The data used is generic and therefore, it is not of a
        specific streaming VOD type

        Args:
            config (dict): Dictionary with parameters that configure the format
                    of the generated graph
            data (list): List with the necessary data to generate the graph.
                        Each element of the list in a pair of elements,
                        in which the first corresponds to the time and the
                        second to the quality.
        """

        self.data = data
        self.config = config
        self.plot_vod_chart()

    def plot_vod_chart(self):
        """
        Class method that reads the data file, separating the data from the
        X-axis from the Y-axis, in order to generate
        the graph, which is generated as a png file in the same folder as this

        """
        # Plot style
        plt.style.use("seaborn-notebook")

        x_axis_time = []  # Extract time
        y_axis_quality = []  # Extract quality
        resolutions = set()

        for d in self.data:
            x_axis_time.append(d[0])
            y_axis_quality.append(d[1])
            resolutions.add(d[1])

        counter = dict((key, 0) for key in resolutions)

        for resolution in resolutions:
            counter[resolution] = y_axis_quality.count(resolution)

        textstr = ""
        for key, value in counter.items():
            textstr = textstr + "\n{} = {}".format(key, value)

        bbox_props = dict(
            boxstyle="square,pad=0.3", fc="white", edgecolor="black", lw=2
        )
        plt.annotate(textstr, xy=(0.03, 0.5), xycoords="axes fraction", bbox=bbox_props)

        # Plot
        # Plot Video
        plt.yticks(list(resolutions))
        plt.plot(
            x_axis_time,
            y_axis_quality,
            color=self.config.get("color_chart", "blue"),
            label=self.config.get("label_plot", "Video Profile"),
        )

        plt.title(
            self.config.get("titleChart", "Video on Demand - Adaptive Bit Rate (ABR)")
        )
        plt.xlabel(self.config.get("xlabel", X_LABEL))
        plt.ylabel(self.config.get("ylabel", "Bitstream/Resolution"))
        plt.ylim(self.config.get("ylimitMin", 0), self.config["ylimitMax"])
        plt.xlim(0, max(x_axis_time))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = "vod_network_chart_" + current_time + ".png"
        plt.savefig(fname, orientation="landscape")
        plt.close()


class CreateLiveChart:
    def __new__(cls, config, data):
        if all(k in config for k in ("ylimitMax", "ylimitMin")):
            if len(data["fcc"]) > 0 or len(data["multicast"]) > 0:
                return super(CreateLiveChart, cls).__new__(cls)
        else:
            raise ValueError

    def __init__(self, config, data):
        """
        Class that generates a graph through somes lists contained in the
        dictionary passed by parameter.
        The objective of this class is to represent the time it takes between
        channel changes in a graph

        Args:
            data ([dict]): Dictionary that contains the necessary data to
                    make the graph. It consists of 3 data lists
                    (fcc, ret, live) mainly, which refer to the data to be
                    interpreted in the graph.
                    The rest of the data in the dictionary are parameters for the
                    graph format
        """
        self.fcc = data["fcc"]
        self.ret = data["ret"]
        self.multicast = data["multicast"]
        self.config = config
        self.plot_live_chart()

    def plot_live_chart(self):
        """
        This class method is dedicated to interpreting the three data lists in
        a chart and then giving a format to the chart
        before exporting it to a png file.

        """

        # plot style
        plt.style.use("seaborn-notebook")
        # FCC Data
        if self.fcc:
            x_axis_time = []  # Extract time
            y_axis_port = []  # Extract port
            fcc_port = self.fcc[0][1]
            for d in self.fcc:
                x_axis_time.append(d[0])
                y_axis_port.append(d[1])

            # Plot
            plt.plot(x_axis_time, y_axis_port, color="blue", label="fcc")
            plt.ylim(self.config["ylimitMin"], self.config["ylimitMax"])

        # RET Data
        if self.ret:
            x_axis_time = []  # Extract time
            y_axis_port = []  # Extract port

            for d in self.ret:
                x_axis_time.append(d[0])
                y_axis_port.append(d[1])

            # Plot
            plt.plot(
                x_axis_time, y_axis_port, "ro", color="red", label="ret", markersize=3
            )
            plt.ylim(self.config["ylimitMin"], self.config["ylimitMax"])

        # Live Data
        if self.multicast:
            x_axis_time = []  # Extract time
            y_axis_port = []  # Extract port
            multicast_port = self.multicast[0][1]
            for d in self.multicast:
                x_axis_time.append(d[0])
                y_axis_port.append(d[1])

        try:
            fcc_time = "{:.2f}".format(self.fcc[-1][0] - self.fcc[0][0])
        except Exception:
            fcc_time = None
        try:
            fcc_packets = len(self.fcc)
        except Exception:
            fcc_packets = None
        try:
            ret_packets = len(self.ret)
        except Exception:
            ret_packets = None

        # FCC Time and RET Packets data
        textstr = "\n".join(
            (
                "FCC Time  = {} sec".format(fcc_time),
                "FCC Packets  = {}".format(fcc_packets),
                "RET Packets  = {}".format(ret_packets),
            )
        )

        bbox_props = dict(
            boxstyle="square,pad=0.3", fc="white", edgecolor="black", lw=2
        )
        plt.annotate(textstr, xy=(0.03, 0.5), xycoords="axes fraction", bbox=bbox_props)

        # Plot
        plt.plot(
            x_axis_time, y_axis_port, "ro", color="gray", label="liv", markersize=3
        )
        plt.ylim(self.config["ylimitMin"], self.config["ylimitMax"])
        plt.yticks(ticks=[fcc_port, multicast_port], labels=["FCC", "Multicast"])
        plt.title(self.config.get("titleChart", "Live Multicast - Unicast UDP"))
        plt.xlabel(self.config.get("xlabel", X_LABEL))
        plt.ylabel(self.config.get("ylabel", "UDP Ports"))

        max_range = []
        if fcc_packets:
            max_range.append(self.fcc[-1][0])
        if ret_packets:
            max_range.append(self.ret[-1][0])
        if self.multicast:
            max_range.append(self.multicast[-1][0])
        plt.xlim(0, max(max_range))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = "live_network_chart_" + current_time + ".png"
        plt.savefig(fname, orientation="landscape")
        plt.close()


if __name__ == "__main__":
    data = [10, 20]
    plot = PlotBarChart(data, treshold=11, title="KPI Test", fname="image")

    config_live = {
        "ylimitMin": 0,
        "ylimitMax": 5500,
        "titleChart": "Multicast Live Capture",
        "xlabel": "Time (sec)",
        "ylabel": "UDP Ports",
    }
