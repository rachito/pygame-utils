import os

import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, path, tiles_per_move, frames, speed, inf_scroll, surface, pos):
        super(Player, self).__init__()
        self.path = path
        self.image_list = [f for f in os.listdir(path) if not f.startswith('.')]
        self.image_list.sort()
        self.image_paths = self.image_list
        self.images = []
        self.frames = frames
        self.speed = speed
        self.inf_scroll = inf_scroll
        self.surface = surface
        self.pos = pos
        self.move = 'IDDLE_DOWN'
        self.tiles_per_move = tiles_per_move
        self.img_db = {'up': [], 'down': [], 'left': [], 'right': []}

        # Load the images
        for i, image_path in enumerate(self.image_paths):
            self.images.append(
                {'img': pygame.image.load(f'{self.path}/{image_path}').convert_alpha(), 'path': image_path})

        # Split all the images in moves
        img_moves = self.split_list(self.images, self.tiles_per_move)

        # Load the image database
        imgs = []
        for key in self.img_db:
            if key == 'right':
                imgs = img_moves[0]
            if key == 'down':
                imgs = img_moves[1]
            if key == 'left':
                imgs = img_moves[2]
            if key == 'up':
                imgs = img_moves[3]

            for i in range(len(imgs)):
                for j in range(self.frames):
                    self.img_db[key].append(imgs[i])

        # Set the default iddle
        self.image = self.images[0]['img']
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.count = 0

    def draw(self):
        current_img = self.image

        if self.move == 'RIGHT':
            selected_images = self.img_db['right']
            current_img = selected_images[self.count]['img']

        if self.move == 'LEFT':
            selected_images = self.img_db['left']
            current_img = selected_images[self.count]['img']

        if self.move == 'IDDLE_LEFT':
            selected_images = self.img_db['left']
            current_img = selected_images[0]['img']

        if self.move == 'UP':
            selected_images = self.img_db['up']
            current_img = selected_images[self.count]['img']

        if self.move == 'IDDLE_UP':
            selected_images = self.img_db['up']
            current_img = selected_images[0]['img']

        if self.move == 'DOWN':
            selected_images = self.img_db['down']
            current_img = selected_images[self.count]['img']

        if self.move == 'IDDLE_DOWN':
            selected_images = self.img_db['down']
            current_img = selected_images[0]['img']

        self.mask = pygame.mask.from_surface(current_img)
        self.surface.blit(current_img, self.rect)

        self.count += 1
        if self.count == self.tiles_per_move * self.frames:
            self.count = 0

    def update(self, move):
        self.move = move
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a]:
            self.move = 'LEFT'
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_d]:
            self.move = 'RIGHT'
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[pygame.K_w]:
            self.move = 'UP'
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[pygame.K_s]:
            self.move = 'DOWN'
            self.rect.move_ip(0, self.speed)

        if self.inf_scroll:

            # Left/Right/Up/Down inf_scroll
            if self.rect.right < 0:
                self.rect.move_ip(self.surface.get_width() + self.image.get_rect().size[0], 0)
            if self.rect.left > self.surface.get_width():
                self.rect.move_ip(-self.surface.get_width() - self.image.get_rect().size[0], 0)
            if self.rect.bottom < 0:
                self.rect.move_ip(0, self.surface.get_height() + self.image.get_rect().size[1])
            if self.rect.top > self.surface.get_height():
                self.rect.move_ip(0, -self.surface.get_height() - self.image.get_rect().size[1])
        else:

            # Always inside the screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.surface.get_width():
                self.rect.right = self.surface.get_width()
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > self.surface.get_height():
                self.rect.bottom = self.surface.get_height()

    @staticmethod
    def split_list(lst, n):
        return [lst[i:i + n] for i in range(0, len(lst), n)]


class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, speed=15, inf_scroll=False):
        super(Enemy, self).__init__()

        # Screen values
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # Sprite sheet values
        self.image = pygame.image.load('media/ship_sheet.png').convert_alpha()
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

        # x, y initial value center of the screen horizontally
        self.init_x = (self.screen_width / 2)
        self.init_y = self.screen_height - (self.height / 1.5)

        # Initial position
        self.rect = self.image.get_rect(center=(self.init_x, self.init_y))
        self.mask = pygame.mask.from_surface(self.image)

        # Behavior
        self.speed = speed
        self.inf_scroll = inf_scroll

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)

        if self.inf_scroll:
            if self.rect.right < 0:
                self.rect.move_ip(self.screen_width + self.width, 0)
            if self.rect.left > self.screen_width:
                self.rect.move_ip(-self.screen_width - self.width, 0)

        else:
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width

    def draw(self):
        self.screen.blit(self.image, self.rect)
