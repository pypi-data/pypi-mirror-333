import marimo

__generated_with = "0.11.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import traitlets
    import anywidget

    class MopadWidget(anywidget.AnyWidget):
        _esm = """
        function render({model, el}){
            const btnId = model.get("button_id");
            let value = model.get("value");
            let p = document.createElement("p");
            p.innerHTML = 'mopad'
            el.appendChild(p)

            const frames = window.mozRequestAnimationFrame || window.requestAnimationFrame; 
            console.log(frames);
            function run_loop(){
                console.log("loop is running now")
                const gamepad = navigator.getGamepads()[0];
                let wait = false;
                gamepad.buttons.map(function(d, i){
                    if(d.pressed){
                        if(i == btnId){
                            value = value + 1; 
                            model.set("value", value);
                            model.save_changes();
                            p.innerHTML = `update: ${value}`
                            wait = true;
                        }
                    }
                })
                if(wait){
                    setTimeout(() => frames(run_loop), 200)
                    wait = false;
                }else{
                    setTimeout(() => frames(run_loop), 50)
                }
            }
        
            run_loop()
        };

        export default { render };
        """
        value = traitlets.Int(0).tag(sync=True)
        button_id = traitlets.Int(0).tag(sync=True)
    return MopadWidget, anywidget, mo, traitlets


@app.cell
def _(MopadWidget, mo):
    widget = mo.ui.anywidget(MopadWidget())
    widget
    return (widget,)


@app.cell
def _(widget):
    widget.value
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
