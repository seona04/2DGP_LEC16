from pico2d import *
import game_world
import game_framework
from bird import Bird
from boy import Boy
from grass import Grass

boy = None
birds = []
BIRD_COUNT = 10


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            for bird in birds:
                bird.set_direction(-1)
            boy.handle_event(event)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            for bird in birds:
                bird.set_direction(1)
            boy.handle_event(event)
        else:
            boy.handle_event(event)


def init():
    global boy, birds

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

    width = get_canvas_width()
    height = get_canvas_height()
    birds = [
        Bird(index, width, height, BIRD_COUNT)
        for index in range(BIRD_COUNT)
    ]
    for bird in birds:
        game_world.add_oject(bird, 2)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy, birds
    game_world.clear()
    boy = None
    birds = []


def update():
    game_world.update()
    delay(0.1)

def render():
    clear_canvas()
    game_world.render()
    update_canvas()







