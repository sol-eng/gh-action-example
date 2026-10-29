from palmerpenguins import load_penguins
from shiny.express import input, render, ui

penguins = load_penguins().dropna()
numeric_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

ui.page_opts(title="Palmer Penguins (deployed via GitHub Actions)", fillable=True)

with ui.sidebar():
    ui.input_selectize(
        "species", "Species", choices=sorted(penguins["species"].unique().tolist()),
        selected=sorted(penguins["species"].unique().tolist()), multiple=True,
    )
    ui.input_selectize("x_var", "X variable", choices=numeric_cols, selected="bill_length_mm")
    ui.input_selectize("y_var", "Y variable", choices=numeric_cols, selected="bill_depth_mm")


@render.plot
def scatter():
    import matplotlib.pyplot as plt

    filtered = penguins[penguins["species"].isin(input.species())]

    fig, ax = plt.subplots()
    for species, group in filtered.groupby("species"):
        ax.scatter(group[input.x_var()], group[input.y_var()], label=species, alpha=0.7)
    ax.set_xlabel(input.x_var())
    ax.set_ylabel(input.y_var())
    ax.legend(title="Species")
    return fig
