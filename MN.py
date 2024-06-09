import random

from lingotojson import turntolingo
from menuclass import *

top_menu = [
    {
        "name": "File",
        "items": [
            ["Save", lambda self: self.sendtoowner("CS")],
            ["Save as", lambda self: print("Hello")],
        ],
    },
    {
        "name": "Rendering",
        "items": [
            ["Render", lambda self: self.sendtoowner("CS")],
            ["Kill process", lambda self: print("Hello")],
        ],
    },
]


class MN(MenuWithField):
    def __init__(self, process):
        super().__init__(process, "MN")
        tips = set(open(path / "tips.txt", "r").readlines())
        self.tips = list(tips)
        self.mousp = True
        self.mousp1 = True
        self.mousp2 = True
        self.tips.remove("\n")
        self.owner.demo = False
        self.nexttip()
        self.resize()
        # self.button =
        # self.top_menu = widgets.TopMenu(self, self.surface, top_menu, 300, "#181818")

    def blit(self):
        pg.draw.rect(self.surface, pg.Color("#181818"), pg.Rect(0, self.surface.get_height() * 0.86, self.surface.get_width(), self.surface.get_height() * 0.14 + 10))
        pg.draw.rect(self.surface, pg.Color("#2B2B2B"), pg.Rect(0, self.surface.get_height() * 0.86, self.surface.get_width(), 2))

        super().blit()
        if self.onfield:
            bp = self.getmouse
            self.movemiddle(bp)

        self.top_menu.blit()

    def tiles(self):
        self.drawtiles = not self.drawtiles
        self.rfa()

    def cameras(self):
        self.drawcameras = not self.drawcameras
        self.rfa()

    def props(self):
        self.drawprops = not self.drawprops
        self.rfa()
    
    def effects(self):
        self.draweffects = not self.draweffects
        self.rfa()

    def water(self):
        self.drawwater = not self.drawwater
        self.rfa()

    def GE(self):
        self.sendtoowner("GE")

    def TE(self):
        self.sendtoowner("TE")

    def LE(self):
        self.sendtoowner("LE")

    def FE(self):
        self.sendtoowner("FE")

    def CE(self):
        self.sendtoowner("CE")

    def LP(self):
        self.sendtoowner("LP")

    def PE(self):
        self.sendtoowner("PE")

    def HK(self):
        self.sendtoowner("HK")

    def rerender(self):
        self.sendtoowner("rerender_all")

    def save(self):
        self.savef()

    def saveastxt(self):
        self.savef_txt()

    def saveas(self):
        self.saveasf()

    def render(self):
        self.sendtoowner("CS")
        # self.savef()
        # renderlevel(self.data)

    def quit(self):
        self.sendtoowner("quit")

    def nexttip(self):
        self.labels[0].set_text(
            self.returnkeytext(
                random.choice(self.tips).replace("\n", "").replace("\\n", "\n")
            )
        )

    def report(self):
        report()

    def github(self):
        github()
