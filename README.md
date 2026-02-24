# HoardGui
All code is currently within [main.py](main.py)

A simple Web UI for controlling lights set up with HyperHDR.
The GUI is made using NiceGUI, and commands are sent to HyperHDR using their JSON API and requests.post

Current page tree is:  

- Main Menu
    - Manual: Select specific block colours. # TODO Enable Users to select 2/3 colours and gradient between
    - Preset: Select premade effects from a drop down. # TODO Enable users to make their own + expand the list to more prebuilt ones 
    - Screen Mirror: Sets the lights to mirror the display.

All pages also have a brightness slider.
