import requests

from nicegui import ui

WIDGET_COLOUR = "#2F2F2F"
TEXT_COLOUR = "#929292"

brightness_val = 5
available_presets = [
    "Atomic swirl",
    "Candle",
    "Police Lights Solid",
    "Rainbow swirl",
    "Sea waves",
    "Strobe red",
]

def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def post(command: dict) -> dict:
    response = requests.post(
        "http://localhost:8090/json-rpc",
        json=command
    )

    return response.json()

def make_colour_command(colour: tuple) -> dict:
    command = {
        "command"   : "color",
        "color"     : colour,
        "duration"  : 0,
        "priority"  : 64,
        "origin"    : "JSON API"
    }
    return command

def make_preset_command(effect: str) -> dict:
    command = {
        "command"   : "effect",
        "effect"    : {
            "name"      : effect
        },
        "duration"  : 0,
        "priority"  : 64,
        "origin"    : "JSON API"
    }
    return command

def make_screen_mirror_command(active: bool) -> dict:
    command = {
        "command"           : "componentstate",
        "componentstate"    :
        {
            "component"         : "VIDEOGRABBER",
            "state"             : active
        }
    }
    return command

def make_brightness_command(brightness: float) -> dict:
    command = {
        "command"       : "adjustment",
        "adjustment"    : 
        {
            "classic_config"    : True,
            "luminanceGain"     : brightness
        }
    }
    return command

def colour_change(colour) -> None:
    post(make_colour_command(hex_to_rgb(colour[1:])))

def preset_change(effect) -> None:
    ui.notify(f"You clicked {effect}")
    post(make_preset_command(effect))

def screen_mirror_change(active) -> None:
    post(make_screen_mirror_command(active))

def brightness_change(brightness) -> None:
    globals().update(
        brightness_val = brightness
    )
    print("ADD A POST IN YOU DUMBASS")


def apply_styles():
    ui.query('body').style('background-color: #1a1a1a')
    ui.add_css('''
        .q-slider__selection { background: #929292 !important; }
        .q-slider__thumb { color: #929292 !important; }
    ''')

def brightness_slider():
    ui.space()
    ui.space()
    ui.space()
    ui.label("Brightness Slider").style(f"color: {TEXT_COLOUR}")
    ui.space()
    ui.slider(
        min=0,
        max=10,
        step=0.1,
        value=brightness_val,
    ).props(
        f"label-always"# color={WIDGET_COLOUR}"
    ).on(
        'update:model-value',
        lambda e: brightness_change(e.args),
        throttle=1.0
    )

@ui.page('/')
def home():
    screen_mirror_change(False)
    apply_styles()
    ui.label('Main Menu').style(f"color: {TEXT_COLOUR}")
    ui.button('Manual Control',
        on_click=lambda: ui.navigate.to('/manual'),
        color=WIDGET_COLOUR).style(f"color: {TEXT_COLOUR}")
    ui.button('Presets',
        on_click=lambda: ui.navigate.to('/presets'),
        color=WIDGET_COLOUR).style(f"color: {TEXT_COLOUR}")
    ui.button('Screen Mirror',
        on_click=lambda: ui.navigate.to('/screen_mirror'),
        color=WIDGET_COLOUR).style(f"color: {TEXT_COLOUR}")
    brightness_slider()

@ui.page('/manual')
def manual():
    apply_styles()
    ui.label('Manual Lighting').style(f"color: {TEXT_COLOUR}")
    with ui.button(icon='colorize', color=WIDGET_COLOUR).style(f"color: {TEXT_COLOUR}"):
        ui.color_picker(on_pick=lambda e: colour_change(e.color))
    ui.button('Back', 
        on_click=lambda: ui.navigate.to('/'), 
        color=WIDGET_COLOUR).style(f"color: {TEXT_COLOUR}")
    brightness_slider()

@ui.page('/presets')
def presets():
    apply_styles()
    ui.label('Preset Effects').style(f"color: {TEXT_COLOUR}")
    with ui.dropdown_button(
        "Presets",
        auto_close=True,
        color=WIDGET_COLOUR
    ).style(f"color: {TEXT_COLOUR}"):
        for preset in available_presets:
            ui.item(
                preset,
                on_click = lambda p = preset: preset_change(p))
    ui.button(
        'Back', 
        on_click=lambda: ui.navigate.to('/'), 
        color=WIDGET_COLOUR,
    ).style(f"color: {TEXT_COLOUR}")
    brightness_slider()

@ui.page('/screen_mirror')
def screen_mirror():
    screen_mirror_change(True)
    apply_styles()
    ui.label('Screen Mirroring Active - Exit to Stop').style(f"color: {TEXT_COLOUR}")
    ui.button('Back', 
    on_click=lambda: ui.navigate.to('/'), 
    color=WIDGET_COLOUR).style(f"color: {TEXT_COLOUR}")
    brightness_slider()

ui.run(port=8091)
