import random

class Rock():
    """
    represents a rock object
    """
    GAP = 200
    VEL = 5
    
    def __init__(self, x, pygame, pipe_img):
        """
        initialize rock object
        :param x: int
        :param y: int
        :return" None
        """
        self.x = x
        self.height = 0

        # where the top and bottom of the rock is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img
        self.PYGAME = pygame

        self.passed = False

        self.set_height()

    def set_height(self):
        """
        set the height of the rock, from the top of the screen
        :return: None
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        move rock based on vel
        :return: None
        """
        self.x -= self.VEL

    def draw(self, win):
        """
        draw both the top and bottom of the rock
        :param win: pygame window/surface
        :return: None
        """
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, player):
        """
        returns if a point is colliding with the rock
        :param player: Player object
        :return: Bool
        """
        player_mask = player.get_mask()
        top_mask = self.PYGAME.mask.from_surface(self.PIPE_TOP)
        bottom_mask = self.PYGAME.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - player.x, self.top - round(player.y))
        bottom_offset = (self.x - player.x, self.bottom - round(player.y))

        b_point = player_mask.overlap(bottom_mask, bottom_offset)
        t_point = player_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False

