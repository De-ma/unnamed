
# pylint: disable-all


import time
import random
import pyxel


WINDOW_WIDTH = 180
WINDOW_HEIGHT = 120

JUMP_HEIGHT = 20

HIT_SCORE = 1


class Pixelation:
    """The core class of the game."""
    def __init__(self) -> None:
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Pixelation")

        pyxel.load("jump_game.pyxel")

        self.start_time = 0                # Start time
        self.timer = 0                     # Track the time
        self.is_running = False            # Is the game running?
        self.is_paused = False             # Is the game paused?

        self.loop_1 = False                # Do not use reset cloud
        self.loop_2 = False                # Do not use reset cloud

        self.go_into_loop_1 = True         # Check if x coordinate > limit
        self.go_into_loop_2 = True         # Check if x coordinate > limit

        self.hero_x = 0
        self.hero_y = 100

        self.dema_x = 0
        self.dema_y = 100

        self.score = 0                     # Total score

        # Jump variables
        self.velocity = 0                  # Increment velocity
        self.jump_height = JUMP_HEIGHT     # Jump height
        self.is_jumping = False            # Variable declaration, for jumping
        self.jump_num = 0                  # How many times did it jump?

        pyxel.run(self.update, self.draw)  # Run the environment

    def update(self) -> None:
        """Update the environment."""
        # If the player pressed the 'Enter' key, to run the game
        if self.is_running:
            # Update the timer
            self.timer = round(time.time() - self.start_time, 1)

            # Press the 'leftarrow' key or the 'A' key to move left
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
                self.hero_x -= 1

            # Press the 'rightarrow' key or 'D' key to move left
            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                pyxel.blt(
                    self.hero_x,
                    self.hero_y + 100,
                    0,
                    16,
                    0,
                    16,
                    16,
                    12,
                )
                self.hero_x += 1

            # Press the 'uparrow' key or 'W' key to move left
            elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                self.is_jumping = True

            # Press the 'Space' key to shoot the laser beam
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.laser_is_shooting = True

            # Press the 'P' key to pause the game
            elif pyxel.btnp(pyxel.KEY_P):
                self.is_paused = True

            # Press the 'Q' key to quit the game
            elif pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
        else:
            # Press the 'Enter' key to start the game
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.is_running = True
                self.start_time = time.time()

            # Press the 'P' key to unpause the game
            elif pyxel.btnp(pyxel.KEY_P):
                self.is_paused = False
                self.is_running = True

            # Press the 'Q' key to quit the game
            elif pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

    def draw(self) -> None:
        """Draw the environment."""
        pyxel.cls(12)

        self.welcome() 

        if (self.is_running is True):

            self.ground() #Draw ground
            self.hero() #Draw hero
            self.jump()         # Jump
        # # self.laser_beam()   # Laser beam activation
        # self.pause()        # Check if the game is paused
        # self.game_over()    # Check if the game is over
            self.constraints()  # Impose constraints on the hero
        # self.show_score()   # Draw the score
        # self.show_timer()   # Show the elapsed time

            # pyxel.blt(
            #     self.hero_x,
            #     self.hero_y + 100,
            #     0,
            #     0,
            #     0,
            #     16,
            #     16,
            #     12,
            # )
        


        # pyxel.blt(
        #     self.dema_x,
        #     self.dema_y,
        #     0,
        #     0,
        #     64,
        #     16,
        #     79,
        #     12,
        # )

    def welcome(self) -> None:
        """Welcome text."""
        # NOTE: The score must be >= -100 not to show 'GAME OVER' screen
        if not self.is_running:
            pyxel.cls(0)
            pyxel.text(
                WINDOW_HEIGHT/3,
                WINDOW_WIDTH/4,
                "Welcome to unnamed part i!\n\nPress enter to start.",
                7
            )

    def ground(self) -> None:
        """Draw the ground."""
        pyxel.rect(0, 110, 180, 120, 2)

        # self.floor = [(i * 60, i * 20 + 50, True) for i in range(3)]
        # # 0, 50
        # # 60, 70

        # for x, y, is_active in self.floor:
        #     pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

    def hero(self) -> None:
        pyxel.blt(  self.hero_x,
                    self.hero_y + 100,
                    0,
                    16,
                    0,
                    16,
                    16,
                    12,
                )

    def jump(self) -> None:
        """A simple jump implementation."""
        print("%s %s", self.hero_x, self.hero_y)
        if self.is_jumping:
            self.jump_num += 1
            # Up
            if self.jump_num <= self.jump_height:
                self.velocity = 1.5
                self.hero_y -= self.velocity
            # Down
            elif self.jump_num > self.jump_height:
                if self.hero_x > 115 and self.hero_x < 155 and self.hero_y < -25 and self.hero_y > -30:
                    # 120, 90  160 
                    self.velocity = 0
                    self.jump_num = 0
                    self.is_jumping = False
                    # self.hero_y = 90
                elif self.hero_x > 55 and self.hero_x < 95 and self.hero_y < -50 and self.hero_y > -55:
                    # 60, 70
                    self.velocity = 0
                    self.jump_num = 0
                    self.is_jumping = False
                    # self.hero_y = 90
                elif self.hero_y != 0:
                    self.velocity = 1.5
                    self.hero_y += self.velocity
                else:
                    self.is_jumping = False
                    self.velocity = 0
                    self.jump_num = 0

    def detect_collision(
        self,
        x_l_1: float,  # Leftmost x coordinate for the first object
        x_r_1: float,  # Rightmost x coordinate for the first object
        x_l_2: float,  # Leftmost x coordinate for the second object
        x_r_2: float   # Rightmost x coordinate for the second object
    ) -> bool:
        """Collision detection algorithm.

        There are three possible cases.

        I. Left side collision

             +----------------+
        +----|-+              |
        |    | |              |
        |    +-|--------------+
        |      |
        |      |
        +------+

            if x_l_1 < x_l_2 and x_r_1 >= x_l_2

        II. Right side collision

        +----------------+
        |             +--|---+
        |             |  |   |
        +----------------+   |
                      |      |
                      |      |
                      +------+


            if x_l_1 >= x_l_2 and x_r_1 > x_r_2

        III. Full collision

        +----------------+
        |   +------+     |
        |   |      |     |
        +----------------+
            |      |
            |      |
            +------+


            if x_l_1 >= x_l_2 and x_r_1 <= x_r_2


        For the left and right side collision, we do not care about
        whether the object's right x coordinate is greater than that
        of the other object.

        NOTE: In case of laser beam, no need to worry about the height
            since it goes all the way up.

        NOTE: Modifications to the inequalities are needed not to mingle
            the cases. For instance, in the first case, if we do not impose
            the restriction x_r_1 <= x_r_2, we get the third case.

        NOTE: We could abstract out the third case, but it is
            better to have it this way since the former option
            will needlessly overcomplicate things.
        """
        # Case I
        if x_l_1 < x_l_2 and (x_r_1 >= x_l_2 and x_r_1 <= x_r_2):
            return True

        # Case II
        if (x_l_1 >= x_l_2 and x_l_1 <= x_r_2) and x_r_1 > x_r_2:
            return True

        # Case III
        if x_l_1 >= x_l_2 and x_r_1 <= x_r_2:
            return True

        return False

    def constraints(self) -> None:
        """Making sure that everything is within the borders."""
        if self.hero_x + 10 > 180:
            self.hero_x = 0

        elif self.hero_x < 0:
            self.hero_x = 170

        elif self.hero_y + 82 > 120:
            self.hero_y = 0

    def play_music(self) -> None:
        """Background music for the game."""
        pyxel.play(0, [0, 1], loop=True)
        pyxel.play(1, [2, 3], loop=True)
        pyxel.play(2, 4, loop=True)

    def pause(self) -> None:
        """Pause the game."""
        if self.is_paused:
            self.is_running = False
            pyxel.text(50, 50, "THE GAME IS PAUSED", pyxel.frame_count % 16)


if __name__ == "__main__":
    Pixelation()
