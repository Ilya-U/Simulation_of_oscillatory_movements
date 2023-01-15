import matplotlib.pyplot as plt


class GraphDrawer:
    def __init__(self, y_cos_limit: float, y_sin_limit: float, cos_label: str, sin_label: str) -> None:
        plt.ion()
        self.fig = plt.figure()
        plt.gcf().canvas.set_window_title("Графики")

        self.y_sin_limit = y_sin_limit
        self.y_cos_limit = y_cos_limit

        self.time_limit = 15

        self.cos_line = Line(self.fig.add_subplot(211), self.time_limit, self.y_cos_limit, "red", cos_label)
        self.sin_line = Line(self.fig.add_subplot(212), self.time_limit, self.y_sin_limit, "blue", sin_label)


    def update(self, time, new_cos_data, new_sin_data) -> None:
        if time <= self.time_limit:
            self.cos_line.add_data(time, new_cos_data)
            self.sin_line.add_data(time, new_sin_data)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close()


class Line:
    def __init__(self, ax, time_limit: float, y_limit: float, color: str, ylabel: str, xlabel: str="Время") -> None:
        self.ax = ax
        self.time_limit = time_limit
        self.y_limit = y_limit

        self.ax.set_xlim(0, self.time_limit)
        self.ax.set_ylim(-self.y_limit, self.y_limit)

        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel(xlabel)

        self.data_x = []
        self.data_y = []

        self.line, = self.ax.plot(self.data_x, self.data_y, color=color)

    def add_data(self, new_x, new_y) -> None:
        self.data_x.append(new_x)
        self.data_y.append(new_y)
        self.line.set_xdata(self.data_x)
        self.line.set_ydata(self.data_y)
