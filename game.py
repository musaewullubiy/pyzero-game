# Тут будут классы
import pygame
from pgzero import game


class AnimatedActor:
    def __init__(self, imagepath, position,
                 frame_width=24, frame_height=16,
                 move_images_row=2, move_images_count=5,
                 stand_images_row=1, stand_images_count=14,
                 move_speed=5, frames_count=14):
        self.position = position
        self.imagepath = imagepath

        self.frame = 0
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames_count = frames_count

        self.move_images = []
        self.move_images_row = move_images_row
        self.move_images_count = move_images_count
        self.load_move_images()

        self.stand_images = []
        self.stand_images_row = stand_images_row
        self.stand_images_count = stand_images_count
        self.load_stand_images()

        self.is_moving = False
        self.move_speed = 5
        self.move_direction = 0
        self.time_since_last_frame = 0
        self.animation_speed = 0.6

    def load_move_images(self):
        full_image = pygame.image.load(self.imagepath)
        for x in range(0,
                       full_image.get_width() - self.frame_width * (self.frames_count - self.move_images_count),
                       self.frame_width):
            move_frame_surface = full_image.subsurface(
                pygame.Rect((x, self.frame_height * self.move_images_row), (self.frame_width, self.frame_height)))
            self.move_images.append(move_frame_surface)

    def load_stand_images(self):
        full_image = pygame.image.load(self.imagepath)
        for x in range(0,
                       full_image.get_width() - self.frame_width * (self.frames_count - self.stand_images_count),
                       self.frame_width):
            stand_frame_surface = full_image.subsurface(
                pygame.Rect((x, self.frame_height * self.stand_images_row), (self.frame_width, self.frame_height)))
            self.stand_images.append(stand_frame_surface)

    def on_move(self):
        return self.move_images[self.frame % len(self.move_images)]

    def on_stand(self):
        return self.stand_images[self.frame % len(self.stand_images)]

    def on_jump(self):
        pass

    def update(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.animation_speed:
            self.frame = (self.frame + 1) % len(self.move_images)
            self.time_since_last_frame -= self.animation_speed

        self.position = (self.position[0] + int(self.is_moving) * self.move_direction * self.move_speed, self.position[1])

    def draw(self):
        if self.is_moving:
            image = self.on_move()
        else:
            image = self.on_stand()
        if self.move_direction == -1:
            image = pygame.transform.flip(image, True, False)
        game.screen.blit(image, self.position)

