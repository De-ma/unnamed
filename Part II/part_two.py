# pylint: disable-all

import time
import random
import pyxel

WINDOW_WIDTH = 180
WINDOW_HEIGHT = 120
JUMP_HEIGHT = 20
HIT_SCORE = 1


class App:
    def __init__(self) -> None:
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Unnamed: Part II")
        pyxel.load("my_resource.pyxres")

        self.hero_x = 0
        self.hero_y = 5
        self.is_left = False
        self.is_walking = False 

        
        pyxel.run(self.update, self.draw)  # Run the environment


    def update(self) -> None:
        # Press the 'leftarrow' key or the 'A' key to move left
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.hero_x -= 1
            self.is_left = True 
            self.is_walking = not self.is_walking

            # Press the 'rightarrow' key or 'D' key to move left
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.is_left = False
            self.is_walking = not self.is_walking
            self.hero_x += 1

        # Press the 'uparrow' key or 'W' key to move left
        # elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            # self.is_jumping = True
    def draw(self) -> None:
        pyxel.cls(12)
        self.ground()

        self.hero()
        self.constraints()  # Impose constraints on the hero


    def ground(self) -> None:
        """Draw the ground."""
        pyxel.rect(0, 110, 1080, 40, 3)

    def hero(self) -> None:
        if self.is_walking and self.is_left:
            pyxel.blt(  self.hero_x,
                    self.hero_y + 100,
                    0,
                    8,
                    8,
                    -8,
                    8,
                    12,
                )
        elif not self.is_walking and self.is_left:
                    pyxel.blt(  self.hero_x,
                    self.hero_y + 100,
                    0,
                    8,
                    0,
                    -8,
                    8,
                    12,
                )
        elif self.is_walking and not self.is_left:
            pyxel.blt(  self.hero_x,
                    self.hero_y + 100,
                    0,
                    8,
                    8,
                    8,
                    8,
                    12,
                )
        elif not self.is_walking and not self.is_left:
            pyxel.blt(  self.hero_x,
                    self.hero_y + 100,
                    0,
                    8,
                    0,
                    8,
                    8,
                    12,
                )



    def constraints(self) -> None:
        """Making sure that everything is within the borders."""
        if self.hero_x + 10 > 180:
            self.hero_x = 0

        elif self.hero_x < 0:
            self.hero_x = 170

        elif self.hero_y + 82 > 120:
            self.hero_y = 0

if __name__ == "__main__":
    App()
