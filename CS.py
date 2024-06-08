import random

from lingotojson import turntolingo
from menuclass import *


class CS(MenuWithField):
    def __init__(self, process):
        super().__init__(process, "CS")
        self.mousp = True
        self.mousp1 = True
        self.mousp2 = True
        camera_manager = self.data["CM"]
        cameras = camera_manager["cameras"]
        self.selected_cameras: list = camera_manager.get("camerasToRender")
        if self.selected_cameras == None:
            camera_manager["camerasToRender"] = [0]
            self.selected_cameras = camera_manager["camerasToRender"]

        for i, camera in enumerate(cameras):
            self.add_button(i)


        self.resize()

    def add_button(self, i):
        self.buttons.append(
            widgets.Button(self.surface, pg.rect.Rect(3, 10 + i * 15, 10, 10), [90, 255, 90] if i in self.selected_cameras else [90, 90, 90], f"Camera {i}", onpress=lambda: self.toggle_camera(i))
        )

    def blit(self):
        super().blit()
        if self.onfield:
            bp = self.getmouse
            self.movemiddle(bp)

    def toggle_camera(self, index):
        print(index)
        button: widgets.Button = self.buttons[index + 2]
        if (index in self.selected_cameras):
            self.selected_cameras.remove(index)
            button.set_color([90, 90, 90])
        else:
            self.selected_cameras.append(index)
            button.set_color([90, 255, 90])
        self.resize()

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
        self.savef()
        renderlevel(self.data)

    def quit(self):
        self.sendtoowner("quit")

    def report(self):
        report()

    def github(self):
        github()