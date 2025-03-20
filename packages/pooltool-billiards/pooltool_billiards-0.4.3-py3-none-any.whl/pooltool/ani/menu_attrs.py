#!/usr/bin/env python
"""
A minimal Panda3D example demonstrating a YAML/config-driven menu system.
This example uses a data model defined with attrs, a renderer that creates DirectGUI
elements from that model, and a minimal ShowBase application.
"""

from typing import List, Optional, Union

import attrs
from direct.gui.DirectGui import (
    DirectButton,
    DirectCheckButton,
    DirectEntry,
    DirectFrame,
    DirectLabel,
    DirectOptionMenu,
    DirectScrolledFrame,
)
from panda3d.core import (
    CardMaker,
    NodePath,
    TextNode,
    Texture,
    TransparencyAttrib,
    Vec4,
)

import pooltool.ani as ani
import pooltool.ani.utils as autils
from pooltool.ani.fonts import load_font
from pooltool.utils import panda_path


@attrs.define
class Text:
    content: str
    title: bool = False


@attrs.define
class Button:
    button: str
    description: str
    command: Optional[str] = None


@attrs.define
class BackButton:
    show: bool
    command: Optional[str] = None


@attrs.define
class Dropdown:
    name: str
    description: str
    options: List[str]
    selection: str
    command: Optional[str] = None


@attrs.define
class CheckBox:
    name: str
    description: str
    checked: bool
    command: Optional[str] = None


@attrs.define
class Entry:
    name: str
    description: str
    initial: str = ""
    validator: Optional[str] = None
    command: Optional[str] = None


@attrs.define
class Menu:
    name: str
    items: List[Union[Text, Button, BackButton, Dropdown, CheckBox, Entry]] = (
        attrs.field(factory=list)
    )


# ===== Menu Renderer =====

# Constants (you can adjust these as needed)
TEXT_COLOR = (0.1, 0.1, 0.1, 1)
FRAME_COLOR = (0, 0, 0, 1)
TEXT_SCALE = 0.05
BUTTON_TEXT_SCALE = 0.07
HEADING_SCALE = 0.12
MOVE = 0.02
INFO_SCALE = 0.025

# For demonstration, we define MENU_ASSETS as a folder name.
MENU_ASSETS = ani.model_dir / "menu"
# In a real application, these fonts would be loaded from disk.
TITLE_FONT = "LABTSECW"
BUTTON_FONT = "LABTSECW"


# A helper to load an image as a 3D plane.
def loadImageAsPlane(filepath, yresolution=600):
    # For demonstration, loadTexture is obtained from ShowBase.loader (we assume Global.loader exists)
    tex = base.loader.loadTexture(filepath)
    tex.setBorderColor(Vec4(0, 0, 0, 0))
    tex.setWrapU(Texture.WMBorderColor)
    tex.setWrapV(Texture.WMBorderColor)
    cm = CardMaker(filepath + " card")
    cm.setFrame(
        -tex.getOrigFileXSize(),
        tex.getOrigFileXSize(),
        -tex.getOrigFileYSize(),
        tex.getOrigFileYSize(),
    )
    card = NodePath(cm.generate())
    card.setTexture(tex)
    card.setScale(card.getScale() / yresolution)
    card.flattenLight()
    return card


# The MenuRenderer interprets a Menu data model into Panda3D DirectGUI elements.
class MenuRenderer:
    def __init__(self, menu_data: Menu):
        self.menu_data = menu_data
        self.last_element = None  # For aligning subsequent elements
        self.elements = []  # Keep track of created DirectGUI objects

        # Create a backdrop and a scrollable canvas.
        # For simplicity, we use Global.render2d and Global.aspect2d as provided by ShowBase.
        from direct.showbase.ShowBase import ShowBase

        self.base = ShowBase.global_instance  # assume our ShowBase is stored here
        self.area_backdrop = DirectFrame(
            frameColor=FRAME_COLOR,
            frameSize=(-1, 1, -1, 1),
            parent=self.base.render2d,
        )
        # Optionally, set a background image:
        self.area_backdrop.setImage(panda_path(f"{MENU_ASSETS}/menu_background.jpeg"))

        self.canvas = DirectScrolledFrame(
            frameColor=(1, 1, 1, 0.2),
            canvasSize=(-1, 1, -3, 1),
            frameSize=(-1, 1, -0.9, 0.3),
            scrollBarWidth=0.04,
            parent=self.base.aspect2d,
        )
        self.canvas.setTransparency(TransparencyAttrib.MAlpha)
        self.canvas.verticalScroll["pageSize"] = 0.05

    def render(self):
        """Render each menu item from the data model."""
        for item in self.menu_data.items:
            if isinstance(item, Text):
                self.add_text(item)
            elif isinstance(item, Button):
                self.add_button(item)
            elif isinstance(item, BackButton):
                self.add_backbutton(item)
            elif isinstance(item, Dropdown):
                self.add_dropdown(item)
            elif isinstance(item, CheckBox):
                self.add_checkbox(item)
            elif isinstance(item, Entry):
                self.add_entry(item)
            else:
                raise ValueError(f"Unsupported menu item type: {type(item)}")

    def add_text(self, text_item: Text):
        """Render a text element."""
        scale = HEADING_SCALE if text_item.title else TEXT_SCALE
        label = DirectLabel(
            text=text_item.content,
            scale=scale,
            parent=self.canvas.getCanvas(),
            relief=None,
            text_fg=TEXT_COLOR,
            text_align=TextNode.ALeft,
        )
        if self.last_element:
            autils.alignTo(label, self.last_element, autils.CT, autils.CB)
        else:
            label.setPos((-0.7, 0, 0.8))
        label.setX(-0.7)
        self.last_element = label
        self.elements.append(label)
        return label

    def add_button(self, button_item: Button):
        """Render a button element."""
        btn = DirectButton(
            text=button_item.button,
            text_align=TextNode.ALeft,
            scale=BUTTON_TEXT_SCALE,
            parent=self.canvas.getCanvas(),
            relief=None,
            text_fg=TEXT_COLOR,
            text_font=load_font(BUTTON_FONT),
        )
        # Bind the command if provided (for demo, we just print the command)
        if button_item.command:
            btn["command"] = lambda: print(f"Button command: {button_item.command}")
        if self.last_element:
            autils.alignTo(btn, self.last_element, autils.CT, autils.CB)
        else:
            btn.setPos((-0.63, 0, 0.8))
        btn.setX(-0.63)
        btn.setZ(btn.getZ() - MOVE)
        self.last_element = btn
        self.elements.append(btn)
        return btn

    def add_backbutton(self, back_item: BackButton):
        """Render a back button."""
        btn = DirectButton(
            scale=0.06,
            # For demo purposes, we won’t load an image; in a full app, use loadImageAsPlane.
            text="Back",
            relief=None,
            parent=self.area_backdrop,
        )
        btn_np = NodePath(btn)
        btn_np.reparentTo(self.area_backdrop)
        btn_np.setPos(-0.92, 0, 0.22)
        if back_item.command:
            btn["command"] = lambda: print(f"Back command: {back_item.command}")
        self.elements.append(btn_np)
        return btn_np

    def add_dropdown(self, dropdown_item: Dropdown):
        """Render a dropdown element."""
        dmenu = DirectOptionMenu(
            scale=BUTTON_TEXT_SCALE * 0.8,
            items=dropdown_item.options,
            initialitem=(
                dropdown_item.options.index(dropdown_item.selection)
                if dropdown_item.selection in dropdown_item.options
                else 0
            ),
            textMayChange=1,
            text_align=TextNode.ALeft,
            relief=None,
            parent=self.canvas.getCanvas(),
        )
        if self.last_element:
            autils.alignTo(dmenu, self.last_element, autils.CT, autils.CB)
        else:
            dmenu.setPos((-0.63, 0, 0.8))
        dmenu.setX(-0.63)
        dmenu.setZ(dmenu.getZ() - MOVE)
        # Bind a command for demonstration.
        if dropdown_item.command:
            dmenu["command"] = lambda: print(
                f"Dropdown command: {dropdown_item.command}"
            )
        self.last_element = dmenu
        self.elements.append(dmenu)
        return dmenu

    def add_checkbox(self, checkbox_item: CheckBox):
        """Render a checkbox element."""
        cb = DirectCheckButton(
            scale=BUTTON_TEXT_SCALE * 0.5,
            indicatorValue=1 if checkbox_item.checked else 0,
            relief=None,
            parent=self.canvas.getCanvas(),
        )
        if self.last_element:
            autils.alignTo(cb, self.last_element, autils.CT, autils.CB)
        else:
            cb.setPos((-0.63, 0, 0.8))
        cb.setX(-0.63)
        cb.setZ(cb.getZ() - MOVE)
        if checkbox_item.command:
            cb["command"] = lambda: print(f"Checkbox command: {checkbox_item.command}")
        self.last_element = cb
        self.elements.append(cb)
        return cb

    def add_entry(self, entry_item: Entry):
        """Render an entry element."""
        entry = DirectEntry(
            text=entry_item.initial,
            scale=BUTTON_TEXT_SCALE * 0.7,
            numLines=1,
            width=4,
            relief=None,
            parent=self.canvas.getCanvas(),
        )
        if self.last_element:
            autils.alignTo(entry, self.last_element, autils.CT, autils.CB)
        else:
            entry.setPos((-0.63, 0, 0.8))
        entry.setX(-0.63)
        entry.setZ(entry.getZ() - MOVE)
        if entry_item.command:
            entry["command"] = lambda: print(f"Entry command: {entry_item.command}")
        self.last_element = entry
        self.elements.append(entry)
        return entry

    def hide(self):
        self.area_backdrop.hide()
        self.canvas.hide()

    def show(self):
        self.area_backdrop.show()
        self.canvas.show()


# ===== Minimal Panda3D Application =====
from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # For convenience, store the ShowBase instance globally so our renderer can access render2d/aspect2d.
        ShowBase.global_instance = self

        # Create a sample menu (in practice you would load this from YAML via cattrs)
        sample_menu = Menu(
            name="Main Menu",
            items=[
                Text(content="Welcome to My App", title=True),
                Text(content="Please select an option:"),
                Button(
                    button="Start", description="Begin the game", command="start_game"
                ),
                Dropdown(
                    name="Difficulty",
                    description="Select a difficulty level",
                    options=["Easy", "Medium", "Hard"],
                    selection="Medium",
                    command="set_difficulty",
                ),
                CheckBox(
                    name="Sound",
                    description="Enable sound effects",
                    checked=True,
                    command="toggle_sound",
                ),
                Entry(
                    name="Player Name",
                    description="Enter your name",
                    initial="Player1",
                    validator="validate_name",
                ),
                BackButton(show=True, command="go_back"),
            ],
        )

        # Render the menu using the MenuRenderer.
        self.menu_renderer = MenuRenderer(sample_menu)
        self.menu_renderer.render()
        self.menu_renderer.show()

        # For demonstration, print a message when the window is closed.
        self.accept("escape", self.userExit)


# Run the Panda3D application.
if __name__ == "__main__":
    app = MyApp()
    app.run()
