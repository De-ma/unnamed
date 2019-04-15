"""
P I X E L A T I O N

David Oniani
Licensed under MIT
"""


# Have to manually disable pylint for this project.
# Otherwise, get pylint(E1101) warning.
# Below is the explanation of why it happens
# NOTE: pyxel initiates an object and binds its methods to the pyxel module.
#       You canont use these methods until the init function has been called.
#       This makes a nice API but is not so good for the static analysis.

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

        # Sound settings

        # First sound effect
        # pyxel.sound(0).set(
        #     "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr \
        #         c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
        #     "p",
        #     "6",
        #     "vffn fnff vffs vfnn",
        #     25,
        # )

        # # Second sound effect
        # pyxel.sound(1).set(
        #     "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2 \
        #         f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
        #     "s",
        #     "6",
        #     "nnff vfff vvvv vfff svff vfff vvvv svnn",
        #     25,
        # )

        # # Third sound effect
        # pyxel.sound(2).set(
        #     "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1 \
        #         a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
        #     "t"
        #     "7",
        #     "n",
        #     25,
        # )

        # self.play_music()                  # Play music with all sound effects


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

        # Laser beam variables
        self.laser_is_shooting = False     # Are the clouds shooting?
        self.laser_beam_timer = 0          # Laser beam time gap
        self.hit_score = HIT_SCORE         # Score increment for laser hit

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
        pyxel.cls(13)

        self.welcome()      # Welcome the player

  

        self.ground()       # Draw the ground
        # self.hero()         # Draw the hero
        self.jump()         # Jump
        # self.laser_beam()   # Laser beam activation
        self.pause()        # Check if the game is paused
        self.game_over()    # Check if the game is over
        self.constraints()  # Impose constraints on the hero
        self.show_score()   # Draw the score
        self.show_timer()   # Show the elapsed time

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

        pyxel.blt(
            self.dema_x,
            self.dema_y,
            0,
            0,
            64,
            16,
            79,
            12,
        )

    def welcome(self) -> None:
        """Welcome text."""
        # NOTE: The score must be >= -100 not to show 'GAME OVER' screen
        if not self.is_running and self.score >= -100 and not self.is_paused:
            pyxel.text(
                28,
                50,
                "Welcome!",
                pyxel.frame_count % 16
            )

    def show_score(self) -> None:
        """Put the score in the upper-right corner."""
        score = f"SCORE {self.score}"
        pyxel.text(4, 5, score, 1)
        pyxel.text(4, 4, score, 7)

    def show_timer(self) -> None:
        """Show the timer under the score."""
        timer = f"TIME {self.timer}"
        pyxel.text(4, 13, timer, 1)
        pyxel.text(4, 12, timer, 7)


    def ground(self) -> None:
        """Draw the ground."""
        pyxel.rect(0, 110, 180, 120, 2)

        self.floor = [(i * 60, i * 20 + 50, True) for i in range(3)]
        # 0, 50
        # 60, 70

        for x, y, is_active in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)


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

    def game_over(self) -> None:
        """If the score is below -100, shows the "GAME OVER" screen.

        NOTE: If the score goes below -100, the player gets the points
            equal to 100 times the time in the game (the timer value).
        """
        if self.score < -100:
            self.is_running = False
            pyxel.text(70, 40, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(
                45,
                50,
                f"YOUR FINAL SCORE IS {round(100 * self.timer)}",
                pyxel.frame_count % 16
            )


if __name__ == "__main__":
    Pixelation()
