from time import perf_counter

from pico2d import (clear_canvas, close_canvas, delay, get_canvas_height,
                    get_canvas_width, get_events, open_canvas, update_canvas)
from sdl2 import SDL_KEYDOWN, SDL_QUIT, SDLK_LEFT, SDLK_RIGHT

from bird import Bird


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
BIRD_COUNT = 10


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        width = get_canvas_width()
        height = get_canvas_height()
        birds = [
            Bird(index, width, height, BIRD_COUNT)
            for index in range(BIRD_COUNT)
        ]
        running = True
        previous_time = perf_counter()

        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN:
                    if event.key == SDLK_LEFT:
                        for bird in birds:
                            bird.set_direction(-1)
                    elif event.key == SDLK_RIGHT:
                        for bird in birds:
                            bird.set_direction(1)

            current_time = perf_counter()
            frame_time = current_time - previous_time
            previous_time = current_time

            for bird in birds:
                bird.update(frame_time)

            clear_canvas()
            for bird in birds:
                bird.draw()
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()