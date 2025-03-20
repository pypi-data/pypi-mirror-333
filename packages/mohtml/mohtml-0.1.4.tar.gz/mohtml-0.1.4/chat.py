import marimo

__generated_with = "0.11.6"
app = marimo.App(width="columns")


@app.cell(column=0)
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    return


@app.cell(column=1)
def _():
    return


if __name__ == "__main__":
    app.run()
