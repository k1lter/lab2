import pygame
import sys

def events(rocket):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    rocket.tleft = True
                elif event.key == pygame.K_e:
                    rocket.tright = True
                elif event.key == pygame.K_LSHIFT:
                    rocket.trust = True
                elif event.key == pygame.K_w:
                    print("-----------------------------")
                    print("Hight = ", rocket.hight/10)
                    print("TWR = ", rocket.TWR)
                    print("Fuel mass = ", rocket.fuelMass)
                    print("Dry mass = ", rocket.dryMass)
                    print("Angle = ", rocket.angle)
                    print("Speed = ", rocket.speed)
                    print("Verctical speed = ", rocket.v_speed)
                    print("Horizontal speed = ", rocket.h_speed)
                    print("rocket.rotated_rect.centerx", rocket.rotated_rect.centerx)
                    print("-----------------------------")
                elif event.key == pygame.K_ESCAPE:
                    rocket.pause = not rocket.pause
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    rocket.tleft = False
                elif event.key == pygame.K_e:
                    rocket.tright = False