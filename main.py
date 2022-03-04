import pygame
import pygame_menu
import control
import shelve
import sys

from rocket import Rocket
from ground import Ground

def menu():
    menu = pygame_menu.Menu('Rocket Game', 1200, 800)
    menu.add.text_input('Player name:', default='', onchange = run)
    menu.add.button('Play', start_the_game)
    menu.add.button('Best score', scores)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)

def fuelBar(fuel, screen):
    fuelbar = pygame.image.load('Images/fuelbar.png')
    fuelbar = pygame.transform.scale(fuelbar, (fuel/10,40))
    fuelbar_rect = fuelbar.get_rect()
    screen.blit(fuelbar, (20, 20))

def pause(rocket, screen):
    while rocket.pause:
        control.events(rocket)
        pygame.mixer.music.stop()
        rocket.alreadystart = False
        continue_button = pygame.draw.rect(screen,(44,50,56),(450,250,250,50))
        quit_button = pygame.draw.rect(screen,(44,50,56),(450,350,250,50))
        continue_text = pygame.font.Font(None, 36)
        text_cont = continue_text.render('Back to game', True,(255,255,255))
        screen.blit(text_cont, (500, 265))

        quit_text = pygame.font.Font(None, 36)
        text_cont = quit_text.render('Exit to main menu', True,(255,255,255))
        screen.blit(text_cont, (470, 365))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] > 450 and pygame.mouse.get_pos()[0] < 700 and pygame.mouse.get_pos()[1] > 250 and pygame.mouse.get_pos()[1] < 300:
                    rocket.pause = False
                    return
                if pygame.mouse.get_pos()[0] > 450 and pygame.mouse.get_pos()[0] < 700 and pygame.mouse.get_pos()[1] > 350 and pygame.mouse.get_pos()[1] < 400:
                        menu = pygame_menu.Menu('Rocket Game', 1200, 800)
                        menu.add.text_input('Player name:', default='', onchange = run)
                        menu.add.button('Play', run)
                        menu.add.button('Best score', scores)
                        menu.add.button('Quit', pygame_menu.events.EXIT)
                        menu.mainloop(surface)
    pygame.display.update()

def scores():
    menu_scores = pygame_menu.Menu('Best of the best', 1200, 800)
    db = shelve.open('db')
    score = db['hi_scores']
    name = db['name']
    print("Best score: ", score)
    print("Name:", name)
    db.close()
    if name != "Null" and score != 0:
        menu_scores.add.label("Best player: " + name)
        menu_scores.add.label("Score: " + str(score))
        menu_scores.add.label("---------------------")
    menu_scores.add.button('Clear score', clear_scores)
    menu_scores.add.button('Back', menu)
    menu_scores.mainloop(surface)

def clear_scores():
    db = shelve.open('db')
    db['hi_scores'] = 0
    db['name'] = "Null"
    db['score'] = 0
    db['player_name'] = "Null"
    db.close()

def name_set(name):
    db = shelve.open('db')
    db['player_name'] = name
    db.close()

def error_name():
    menu_error = pygame_menu.Menu('Error!', 1200, 800)
    menu_error.add.label("Enter your name in the input box!")
    menu_error.add.button("Back", menu)
    menu_error.mainloop(surface)

def run():
    pygame.init()
    db = shelve.open('db')
    name = db['player_name']
    db.close()
    if name == "":
        error_name()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1200, 800))
    bg = pygame.image.load('Images/BackGround.png')
    bg = pygame.transform.scale(bg, (1200,3200))
    pygame.display.set_caption("Тестовое окно")
    rocket = Rocket(screen)
    ground = Ground(screen)

    while ground.dead == False:
        pause(rocket, screen)
        clock.tick(60)
        control.events(rocket)
        rocket.update_rocket()
        ground.update_ground(rocket, bg)
        rocket.output()
        ground.output()
        fuelBar(rocket.fuelMass, screen)
        pygame.display.flip()
    db = shelve.open('db')
    d = db['hi_scores']
    playername = db['player_name']
    if d < ground.score:
       db['hi_scores'] = ground.score
       db['name'] = playername
    db['player_name'] = "Null"
    db.close()

pygame.init()
surface = pygame.display.set_mode((1200, 800))

menu = pygame_menu.Menu('Rocket Game', 1200, 800)
menu.add.text_input("Name:", default= "", onchange= name_set)
menu.add.button('Play', run)
menu.add.button('Best score', scores)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)