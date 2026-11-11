from math import sin, tau
from pathlib import Path

from pico2d import load_image

import game_framework


SHEET_WIDTH = 918
SHEET_HEIGHT = 506
SHEET_COLUMNS = 5
SHEET_ROWS = 3
FRAME_COUNT = 14
FRAMES_PER_SECOND = 12.0
BIRD_WIDTH = 150
BIRD_HEIGHT = 138


def _make_frame_rectangles():
    rectangles = []
    for row in range(SHEET_ROWS):
        top = row * SHEET_HEIGHT // SHEET_ROWS
        bottom = (row + 1) * SHEET_HEIGHT // SHEET_ROWS
        columns = SHEET_COLUMNS if row < 2 else 4
        for column in range(columns):
            left = column * SHEET_WIDTH // SHEET_COLUMNS
            right = (column + 1) * SHEET_WIDTH // SHEET_COLUMNS
            rectangles.append((left, SHEET_HEIGHT - bottom,
                               right - left, bottom - top))
    return tuple(rectangles)


FRAME_RECTANGLES = _make_frame_rectangles()


class Bird:
    image = None

    def __init__(self, index, canvas_width, canvas_height, bird_count=10):
        if Bird.image is None:
            image_path = Path(__file__).with_name('bird_animation.png')
            Bird.image = load_image(str(image_path))

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.x = (index + 0.5) * canvas_width / bird_count
        self.base_y = canvas_height * (0.15 + (index % 5) * 0.175)
        self.y = self.base_y
        self.speed = 90.0 + (index % 5) * 12.0
        self.direction = 1
        self.phase = index * tau / bird_count
        self.elapsed = 0.0
        self.frame = index * FRAME_COUNT / bird_count

    def set_direction(self, direction):
        if direction not in (-1, 1):
            raise ValueError('direction must be -1 or 1')
        self.direction = direction

    def update(self, frame_time=None):
        if frame_time is None:
            frame_time = game_framework.frame_time
        self.elapsed += frame_time
        self.frame = (
            self.frame + FRAMES_PER_SECOND * frame_time
        ) % FRAME_COUNT
        left_edge = BIRD_WIDTH / 2
        right_edge = self.canvas_width - BIRD_WIDTH / 2
        travel_distance = right_edge - left_edge
        position = self.x - left_edge
        if self.direction < 0:
            position = 2 * travel_distance - position
        position = (
            position + self.speed * frame_time
        ) % (2 * travel_distance)
        if position <= travel_distance:
            self.x = left_edge + position
            self.direction = 1
        else:
            self.x = right_edge - (position - travel_distance)
            self.direction = -1
        self.y = self.base_y + 8.0 * sin(self.elapsed * 2.0 + self.phase)

    def draw(self):
        left, bottom, width, height = FRAME_RECTANGLES[int(self.frame)]
        flip = 'h' if self.direction < 0 else ''
        Bird.image.clip_composite_draw(
            left, bottom, width, height, 0, flip, self.x, self.y,
            BIRD_WIDTH, BIRD_HEIGHT
        )