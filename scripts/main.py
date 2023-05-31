import os
import re
import shutil
import gradio as gr
from modules import script_callbacks
from modules import shared, scripts
import modules.scripts as scripts

accents = ['pink', 'blue']
script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def on_ui_settings():
    section = ('ctp', 'BILIBILI THEME')
    shared.opts.add_option("accent_color", 
                            shared.OptionInfo(
                                default='maroon',
                                label='Accent',
                                component=gr.Radio,
                                component_args={"choices": accents},
                                onchange=on_accent_color_change,
                                section=section
                            ))

def on_accent_color_change():
    # replace the accent color
    with open(os.path.join(script_path,'style.css'), "r+") as file:
        pattern = re.compile(r"--ctp-accent:\s*(.*)")
        text = re.sub(pattern, f'--ctp-accent: var(--ctp-{shared.opts.accent_color});', file.read(), count=1)
        file.seek(0)
        file.write(text)
        file.truncate()

def on_ui_settings_change():
    shutil.copy(os.path.join(script_path,f'/bilibili.css'), os.path.join(script_path, 'style.css'))
    # reappply accent color
    on_accent_color_change()

script_callbacks.on_ui_settings(on_ui_settings)