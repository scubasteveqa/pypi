from shiny import App, ui, render, reactive
import numpy as np
import matplotlib.pyplot as plt

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Simple Data Generator"),
        ui.input_slider("num_points", "Number of points", min=10, max=200, value=50),
        ui.input_slider("noise", "Noise level", min=0.1, max=2.0, value=0.5, step=0.1),
        ui.input_action_button("generate", "Generate New Data")
    ),
    ui.card(
        ui.card_header("Random Data Plot"),
        ui.output_plot("scatter_plot")
    )
)

def server(input, output, session):
    data = reactive.value({
        "x": np.random.normal(0, 1, 50),
        "y": np.random.normal(0, 1, 50)
    })
    
    @reactive.effect
    @reactive.event(input.generate)
    def _():
        n = input.num_points()
        noise = input.noise()
        data.set({
            "x": np.random.normal(0, 1, n),
            "y": np.random.normal(0, noise, n)
        })
    
    @render.plot
    def scatter_plot():
        fig, ax = plt.subplots()
        ax.scatter(data.get()["x"], data.get()["y"], alpha=0.7)
        ax.set_xlabel("X values")
        ax.set_ylabel("Y values")
        ax.set_title(f"Random Data (n={len(data.get()['x'])}, noise={input.noise()})")
        ax.grid(True, linestyle='--', alpha=0.7)
        return fig

app = App(app_ui, server)
