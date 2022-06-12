"""Create entry."""
import gradio as gr

def greet(name):
    """Greet."""
    if not name:
        name = "world"
    return "Hello " + name + "!! (coming sooooon...)"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch()
