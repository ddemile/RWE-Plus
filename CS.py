import random

from lingotojson import turntolingo
from menuclass import *


class CS(MenuWithField):
    def __init__(self, process):
        self.menu = "CE"
        self.mode = "move"
        super().__init__(process, "CS")
        self.mousp = True
        self.mousp1 = True
        self.mousp2 = True
        camera_manager = self.data["CM"]
        cameras = camera_manager["cameras"]
        self.page = 0
        self.selected_cameras: list = camera_manager.get("camerasToRender")
        if self.selected_cameras == None:
            camera_manager["camerasToRender"] = [0]
            self.selected_cameras = camera_manager["camerasToRender"]

        self.render_page()

    def render_page(self):
        self.buttons = self.buttons[:4]
        cameras: list = self.data["CM"]["cameras"]
        start_index = self.page * 6
        end_index = start_index + 6

        for i, camera in enumerate(cameras[start_index:end_index]):
            self.add_button(i, start_index)
        self.resize()

    def add_button(self, i, start_i):
        button = widgets.Button(self.surface, pg.rect.Rect(3, 10 + i * 11, 10, 10), [90, 255, 90] if start_i + i in self.selected_cameras else [90, 90, 90], f"Camera {start_i + i}", onpress=lambda: self.toggle_camera(start_i + i, button))
        self.buttons.append(button)

    def blit(self):
        super().blit()
        if self.onfield:
            bp = self.getmouse
            self.movemiddle(bp)
        self.rendercameras()

    def toggle_camera(self, index: int, button: widgets.Button):
        if (index in self.selected_cameras):
            self.selected_cameras.remove(index)
            button.set_color([90, 90, 90])
        else:
            self.selected_cameras.append(index)
            button.set_color([90, 255, 90])
        self.resize()
    
    def rendercameras(self):
        closest = 0
        if hasattr(self, "closestcameraindex"):
            closest = self.closestcameraindex()
        for indx, cam in enumerate(self.data["CM"]["cameras"]):

            rect = self.getcamerarect(cam)
            rect2 = pg.Rect(rect.x + self.size, rect.y + self.size, rect.w - self.size * 2, rect.h - self.size * 2)
            rect3 = pg.Rect(rect2.x + self.size * 8, rect2.y, rect2.w - self.size * 16, rect2.h)
            # print(camera_border, rect, self.size)
            pg.draw.rect(self.surface, camera_border, rect.clip(self.field.rect), max(self.size // 3, 1))
            pg.draw.rect(self.surface, camera_border, rect2.clip(self.field.rect), max(self.size // 4, 1))

            pg.draw.rect(self.surface, red, rect3.clip(self.field.rect), max(self.size // 3, 1))

            line = self.field.rect.clipline(pg.Vector2(rect.center) - pg.Vector2(self.size * 5, 0),
                                            pg.Vector2(rect.center) + pg.Vector2(self.size * 5, 0))
            if line:
                pg.draw.line(self.surface, camera_border, line[0], line[1],
                             self.size // 3 + 1)

            line = self.field.rect.clipline(pg.Vector2(rect.center) - pg.Vector2(0, self.size * 5),
                                            pg.Vector2(rect.center) + pg.Vector2(0, self.size * 5))
            if line:
                pg.draw.line(self.surface, camera_border, line[0], line[1],
                             self.size // 3 + 1)
            if self.field.rect.collidepoint(rect.center):
                pg.draw.circle(self.surface, camera_border, rect.center, self.size * 3, self.size // 3 + 1)

            if "quads" not in self.data["CM"]:
                self.data["CM"]["quads"] = []
                for _ in self.data["CM"]["cameras"]:
                    self.data["CM"]["quads"].append([[0, 0], [0, 0], [0, 0], [0, 0]])
            col = camera_notheld
            if hasattr(self, "held") and hasattr(self, "heldindex"):
                if indx == self.heldindex and self.held:
                    col = camera_held

            quads = self.data["CM"]["quads"][indx]

            newquads = quads.copy()

            for i, q in enumerate(quads):
                n = [0, 0]
                nq = q[0] % 360
                n[0] = math.sin(math.radians(nq)) * q[1] * self.size * 5
                n[1] = -math.cos(math.radians(nq)) * q[1] * self.size * 5
                newquads[i] = n

            tl = pg.Vector2(rect.topleft) + pg.Vector2(newquads[0])
            tr = pg.Vector2(rect.topright) + pg.Vector2(newquads[1])
            br = pg.Vector2(rect.bottomright) + pg.Vector2(newquads[2])
            bl = pg.Vector2(rect.bottomleft) + pg.Vector2(newquads[3])

            if self.size >= 3 and self.field.rect.collidepoint(rect.center):
                widgets.fastmts(self.surface, f"Id: {indx}", rect.centerx, rect.centery, white)
            # pg.draw.polygon(self.surface, col, [tl, bl, br, tr], self.size // 3)
            for i in [[tl, bl], [bl, br], [br, tr], [tr, tl]]:
                line = self.field.rect.clipline(i[0], i[1])
                if line:
                    pg.draw.line(self.surface, col, line[0], line[1], self.size // 3)

    def previous_page(self):
        if self.page > 0:
            self.page -= 1
            self.render_page()
            
    def next_page(self):
        if self.page < math.floor(len(self.data["CM"]["cameras"]) / 6) and len(self.data["CM"]["cameras"]) % 6 > 0:
            self.page += 1
            self.render_page()

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