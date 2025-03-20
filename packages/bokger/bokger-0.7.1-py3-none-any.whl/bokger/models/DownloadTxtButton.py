from bokeh.models import CustomJS
from bokeh.models.widgets import Button
import os

_js_path = os.path.join(os.path.dirname(__file__),"DownloadTxt.js")
_js_code = open(_js_path).read()


def downloadTxtButton(txt : str, filename: str)-> Button:
    button_label = f"Download {filename}"
    button = Button(label=button_label, button_type="success")    
    _js = CustomJS(args=dict(txt=txt, filename=filename),code=_js_code)
    button.js_on_click(_js)
    return button

if __name__ =='__main__':
    from bokeh.io import show
    from bokeh.plotting import output_file
    output_file(filename = "save_txt.html", mode='inline')
    
    button = downloadTxtButton("hello world","example.txt")

    show(button)
