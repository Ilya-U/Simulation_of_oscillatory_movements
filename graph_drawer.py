import matplotlib.pyplot as plt


class GraphDrawer:
    def __init__(self, y_cos_limit, y_sin_limit) -> None:
        # TODO Необходимо выделить класс Line, чтобы избежать дублирования кода!!!
        plt.ion()
        self.fig = plt.figure()

        self.y_sin_limit = y_sin_limit
        self.y_cos_limit = y_cos_limit

        self.time_limit = 30

        self.cos_line = Line(self.fig.add_subplot(211), self.time_limit, self.y_cos_limit, "red")
        self.sin_line = Line(self.fig.add_subplot(212), self.time_limit, self.y_sin_limit, "blue")

    def update(self, time, new_cos_data, new_sin_data):
        self.cos_line.add_data(time, new_cos_data)
        self.sin_line.add_data(time, new_sin_data)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class Line:
    def __init__(self, ax, time_limit, y_limit, color) -> None:
        self.ax = ax
        self.time_limit = time_limit
        self.y_limit = y_limit

        self.ax.set_xlim(0, self.time_limit)
        self.ax.set_ylim(-self.y_limit, self.y_limit)
        self.data_x = []
        self.data_y = []
        self.line, = self.ax.plot(self.data_x, self.data_y, color=color)

    def add_data(self, new_x, new_y):
        self.data_x.append(new_x)
        self.data_y.append(new_y)
        self.line.set_xdata(self.data_x)
        self.line.set_ydata(self.data_y)
