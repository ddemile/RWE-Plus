from menuclass import *


class TT(MenuWithField):
    def __init__(self, surface: pg.surface.Surface, renderer: Renderer):
        super().__init__(surface, "TT", renderer)
        self.step = 0
        self.maxstep = 0
        self.renderer.geo_full_render(self.layer)
        self.size = 13
        self.pastedata = json.load(open(path2tutorial + "text samples.json", "r"))
        self.selectedtool = ""
        self.toolrotation = 0
        self.resize()
        self.rfa()
        self.blit()
        self.onstart()

    def onstart(self):
        self.labels[1].visible = False
        self.buttons[2].visible = False
        self.buttons[3].visible = False
        self.buttons[4].visible = False
        self.field.visible = False

    def blit(self, draw=True):
        super().blit(draw)
        mpos = pg.mouse.get_pos()
        con = False
        match self.step:
            case 1:
                con = self.xoffset != 0 or self.yoffset != 0
            case 2:
                con = self.size != 13
            case 3:
                con = self.layer != 0

        self.enablenext(con)
        if self.field.rect.collidepoint(mpos) and self.field.visible:
            bp = pg.mouse.get_pressed(3)
            pos = [math.floor((mpos[0] - self.field.rect.x) / self.size),
                   math.floor((mpos[1] - self.field.rect.y) / self.size)]
            pos2 = [pos[0] * self.size + self.field.rect.x, pos[1] * self.size + self.field.rect.y]
            pg.draw.rect(self.surface, cursor, [pos2, [self.size, self.size]], 1)
            posoffset = [pos[0] - self.xoffset, pos[1] - self.yoffset]
            if bp[0] == 1 and self.mousp and (self.mousp2 and self.mousp1):
                self.mousp = False
                self.emptyarea()
            elif bp[0] == 1 and not self.mousp and (self.mousp2 and self.mousp1) and self.step > 5:
                placeblock = 1
                if self.selectedtool == "AR":
                    placeblock = 0
                elif self.selectedtool == "SL":
                    placeblock = 2 + self.toolrotation
                if (0 <= posoffset[0] < len(self.data["GE"])) and (0 <= posoffset[1] < len(self.data["GE"][0])):
                    self.area[posoffset[0]][posoffset[1]] = 0
                    self.data["GE"][posoffset[0]][posoffset[1]][self.layer][0] = placeblock
            elif bp[0] == 0 and not self.mousp and (self.mousp2 and self.mousp1):
                if self.step == 6 or (self.selectedtool == "AR" and self.step == 8) \
                                  or (self.selectedtool == "SL" and self.step == 10):
                    self.enablenext(True)
                self.mousp = True
                self.render_geo_area()
                self.rfa()

            if bp[2] == 1 and self.mousp2 and (self.mousp and self.mousp1):
                self.mousp2 = False
                self.rectdata = [posoffset, [0, 0], pos2]
                self.emptyarea()
            elif bp[2] == 1 and not self.mousp2 and (self.mousp and self.mousp1) and self.step > 6:
                self.rectdata[1] = [posoffset[0] - self.rectdata[0][0], posoffset[1] - self.rectdata[0][1]]
                rect = pg.Rect([self.rectdata[2], [pos2[0] - self.rectdata[2][0], pos2[1] - self.rectdata[2][1]]])
                tx = f"{int(rect.w / self.size)}, {int(rect.h / self.size)}"
                widgets.fastmts(self.surface, tx, *mpos, white)
                pg.draw.rect(self.surface, select, rect, 5)
            elif bp[2] == 0 and not self.mousp2 and (self.mousp and self.mousp1):
                if self.step == 7 or (self.selectedtool == "AR" and self.step == 8) \
                                  or (self.selectedtool == "SL" and self.step == 10):
                    self.enablenext(True)
                placeblock = 1
                if self.selectedtool == "AR":
                    placeblock = 0
                elif self.selectedtool == "SL":
                    placeblock = 2 + self.toolrotation
                for x in range(self.rectdata[1][0]):
                    for y in range(self.rectdata[1][1]):
                        if (0 <= posoffset[0] < len(self.data["GE"])) and (0 <= posoffset[1] < len(self.data["GE"][0])):
                            self.data["GE"][x + self.rectdata[0][0]][y + self.rectdata[0][1]][self.layer][0] = placeblock
                            self.area[x + self.rectdata[0][0]][y + self.rectdata[0][1]] = 0
                self.data["GE"] = self.data["GE"]
                self.detecthistory(["GE"])
                self.renderer.geo_render_area(self.area, self.layer)
                self.rfa()
                self.mousp2 = True

            if self.step > 0:
                self.movemiddle(bp, pos)

    def enablenext(self, condition):
        if condition:
            self.buttons[0].enabled = True
            self.buttons[0].visible = True

    def next(self):
        self.step += 1
        textline = self.settings["textlines"][self.step]
        firstchar = textline[0]
        self.buttons[0].visible = True
        self.buttons[0].enabled = True
        if firstchar == "?":
            self.labels[0].set_text(textline[1:])
        elif firstchar == "@":
            self.labels[0].set_text(textline[1:])
            self.buttons[0].visible = False
        else:
            self.labels[0].set_text(textline)
            if self.step > self.maxstep:
                self.buttons[0].enabled = False
        if self.maxstep < self.step - 1:
            self.maxstep = self.step
        self.buttons[1].set_text(str(self.step))
        self.showstep()

    def showstep(self):
        self.clearfield()
        match self.step:
            case 0:
                self.field.visible = False
            case 1:
                self.field.visible = True
                self.pastegeo("MMB - move around")
            case 2:
                self.pastegeo("MMB - move around")
                self.pastegeo("scroll - scale", 1)
            case 3:
                if self.layer != 0:
                    self.layer = 0
                    self.render_geo_full()
                self.pastegeo("MMB - move around")
                self.pastegeo("scroll - scale", 1)
                self.pastegeo("L - change layer", 2)
                self.buttons[2].visible = False
                self.buttons[3].visible = False
                self.buttons[4].visible = False
                self.labels[1].visible = False
            case 4:
                if self.layer != 1:
                    self.layer = 1
                    self.render_geo_full()
            case 5:
                self.buttons[2].visible = True
                self.buttons[3].visible = True
                self.buttons[4].visible = True

                self.buttons[2].enabled = True
                self.buttons[3].enabled = False
                self.buttons[4].enabled = False
                self.labels[1].visible = True
            case 6:
                self.pastegeo("LMB - Place")
            case 7:
                self.pastegeo("LMB - Place")
                self.pastegeo("RMB - fill", 1)
                self.buttons[3].enabled = False
            case 8:
                self.pastegeo("LMB - Place")
                self.pastegeo("RMB - fill", 1)
                self.buttons[3].enabled = True
                self.buttons[4].enabled = False
            case 9:
                self.pastegeo("LMB - Place")
                self.pastegeo("RMB - fill", 1)
                self.pastegeo("SPACE - rotate slopes", 2)
                self.buttons[4].enabled = True
                self.buttons[2].visible = True
                self.buttons[3].visible = True
                self.buttons[4].visible = True
                self.labels[1].visible = True
                self.field.visible = True
            case 12:
                self.field.visible = False
                self.buttons[2].visible = False
                self.buttons[3].visible = False
                self.buttons[4].visible = False
                self.labels[1].visible = False
            case 13:
                self.rebuttons()
    def rebuttons(self):
        arr = {}

    def clearfield(self):
        clearblock = 1 if self.layer == 0 else 0
        for x in range(self.btiles[0], len(self.data["GE"]) - self.btiles[2]):
            for y in range(self.btiles[1], len(self.data["GE"][0]) - self.btiles[3]):
                self.data["GE"][x][y][self.layer][0] = clearblock
        self.render_geo_full()
        self.rfa()

    def skip(self):
        self.enablenext(True)
        self.next()

    def prev(self):
        if self.step - 1 >= 0:
            self.step -= 1
            textline = self.settings["textlines"][self.step]
            firstchar = textline[0]
            self.buttons[0].visible = True
            if firstchar == "?":
                self.labels[0].set_text(textline[1:])
            elif firstchar == "@":
                self.labels[0].set_text(textline[1:])
                self.buttons[0].visible = False
            else:
                self.labels[0].set_text(textline)
            self.buttons[0].enabled = True
            self.buttons[1].set_text(str(self.step))
            self.showstep()

    def swichlayers(self):
        if self.step in [3, 11]:
            super().swichlayers()
            self.next()

    def swichlayers_back(self):
        if self.step in []:
            super().swichlayers_back()
            self.next()

    def WL(self):
        if self.step == 5:
            self.enablenext(True)
        self.selectedtool = "WL"
        self.labels[1].set_text("Selected tool: Wall")

    def AR(self):
        self.selectedtool = "AR"
        self.labels[1].set_text("Selected tool: Air")

    def SL(self):
        self.selectedtool = "SL"
        self.labels[1].set_text("Selected tool: Slope, rotation: 0")
        self.toolrotation = 0

    def rotate(self):
        if self.selectedtool == "SL":
            self.toolrotation = (self.toolrotation + 1) % 4
            self.labels[1].set_text("Selected tool: Slope, rotation: " + str(self.toolrotation))

    def send(self, message):
        if message[0] == "-":
            self.mpos = 1
            if hasattr(self, message[1:]):
                getattr(self, message[1:])()
        match message:
            case "SU":
                if self.step > 1:
                    self.size += 1
                    self.renderfield()
            case "SD":
                if self.step > 1:
                    if self.size - 1 > 0:
                        self.size -= 1
                        self.renderfield()
            case "left":
                self.xoffset += 1
            case "right":
                self.xoffset -= 1
            case "up":
                self.yoffset += 1
            case "down":
                self.yoffset -= 1

    def pastegeo(self, data, line=0):
        self.emptyarea()
        for xi, x in enumerate(copy.deepcopy(self.pastedata[data])):
            for yi, y in enumerate(x):
                xpos = self.btiles[0] + xi + 1
                ypos = self.btiles[1] + yi + 1
                ypos += line * 6
                self.data["GE"][xpos][ypos][self.layer] = y
                self.area[xpos][ypos] = 0
        self.detecthistory(["GE"])
        self.render_geo_area()
        self.rfa()