from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class SalaryChart(FigureCanvasQTAgg):

    def __init__(self):
        self.figure = Figure(figsize=(8, 4))
        super().__init__(self.figure)

    def update_chart(self, employees):

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        noms = [e.nom for e in employees]
        salaires = [e.salary for e in employees]

        bars = ax.bar(
            noms,
            salaires,
            color="#3498db"
        )

        ax.set_title(
            "Salaires des employés"
        )

        ax.set_ylabel("€")

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.3
        )

        for bar in bars:

            y = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                y,
                f"{y:.0f}",
                ha="center"
            )

        self.draw()
