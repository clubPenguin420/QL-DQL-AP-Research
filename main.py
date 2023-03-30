import pygame

from MazeGame.MazePlayer import MazePlayer
from MazeGame.MazeLavaPit import MazeLavaPit
from RunnerChaser.Runner import Runner
from RunnerChaser.Chaser import Chaser

import numpy as np
import sys
import math
import json

np.set_printoptions(threshold=sys.maxsize)
num_episodes = 100
discount = 0.8
learning_rate = 0.9
epsilon = 0.99
e_decay = 0.75**(1/num_episodes)
state = 0


Q = {}


def main():

    global epsilon
    global state

    m_player = MazePlayer(7.5, 7.5)
    rc_player = Runner(1007.5, 457.5)
    rc_enemy_1 = Chaser(857.5, 457.5)
    rc_enemy_2 = Chaser(1007.5, 532.5)
    rc_enemy_3 = Chaser(1157.5, 397.5)
    pit_1 = MazeLavaPit(405, 30, 15*5, 15*18)
    pit_2 = MazeLavaPit(45, 405, 15*15, 15*5)
    pit_3 = MazeLavaPit(390, 420, 15*5, 15*5)
    m_goal = pygame.Rect(540, 540, 60, 60)
    rc_goal = pygame.Rect(970, 0, 60, 60)
    m_help = pygame.Rect(285, 555, 60, 45)
    rc_help = pygame.Rect(1135, 0, 60, 45)

    pygame.init()
    pygame.display.set_caption("An exciting game of pong")
    screen = pygame.display.set_mode((1300, 600))
    FPS = pygame.time.Clock()
    FPS.tick(30)
    DisplaySurface = pygame.display.set_mode((1300, 600))
    DisplaySurface.fill((0, 0, 0))

    # def pack_state():
    #     paddle1_y = int((math.floor(paddle1.rect.centery - 60)/12))
    #     paddle2_y = int(math.floor((paddle2.rect.centery - 60)/12))
    #     ball_x = int((ball.rect.centerx - 27)/6)
    #     ball_y = int((ball.rect.centery - 3)/6)
    #     ball_v = 0
    #     if ball.velocity == [6, 6]:
    #         ball_v = 0
    #     elif ball.velocity == [-6, 6]:
    #         ball_v = 1
    #     elif ball.velocity == [6, -6]:
    #         ball_v = 2
    #     elif ball.velocity == [-6, -6]:
    #         ball_v = 3
    #     return "".join(map(str, (paddle1_y, paddle2_y, ball_x, ball_y, ball_v)))
    
    running = True
    rc_start = pygame.time.get_ticks()
    m_start = pygame.time.get_ticks()
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # state = pack_state()
        # if not state in Q.keys():
        #     Q[state] = [0., 0., 0.]

        # if np.random.rand() > (1 - epsilon):
        #     action1 = np.random.randint(0, 3)
        # else:
        #     #print("Taken q value action")
        #     action1 = np.argmax(Q[state])

        # if np.random.rand() > (1 - epsilon):
        #     action2 = np.random.randint(0, 3)
        # else:
        #     action2 = np.argmax(Q[state])
        

        DisplaySurface.fill((0, 0, 0))

        pygame.draw.line(DisplaySurface, (100, 100, 100), (600, 0), (600, 600))
        pygame.draw.line(DisplaySurface, (100, 100, 100), (700, 0), (700, 600))
        for i in range(0, 600, 15):
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i, 0), (i, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (0, i), (600, i))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i+700, 0), (i+700, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (700, i), (1300, i))
        
        m_player.update(0)
        rc_player.update(0)

        rc_status1 = rc_enemy_1.update(rc_player)
        rc_status2 = rc_enemy_2.update(rc_player)
        rc_status3 = rc_enemy_3.update(rc_player)

        pit_1.draw(DisplaySurface)
        pit_2.draw(DisplaySurface)
        pit_3.draw(DisplaySurface)
        rc_enemy_1.draw(DisplaySurface)
        rc_enemy_2.draw(DisplaySurface)
        rc_enemy_3.draw(DisplaySurface)

        pygame.draw.rect(DisplaySurface, (0, 0, 230), m_goal)
        pygame.draw.rect(DisplaySurface, (0, 0, 230), rc_goal)
        pygame.draw.rect(DisplaySurface, (33, 115, 55), m_help)
        pygame.draw.rect(DisplaySurface, (33, 115, 55), rc_help)

        m_player.draw(DisplaySurface)
        rc_player.draw(DisplaySurface)

        if (m_player.rect.colliderect(pit_1.rect) or m_player.rect.colliderect(pit_2.rect) or m_player.rect.colliderect(pit_3.rect)) and pit_1.active :
            running = False
        if rc_status1 == -1 or rc_status2 == -1 or rc_status3 == -1:
            running = False
        elif m_player.rect.colliderect(m_help):
            print("Maze Help Portal activated!")
            if pygame.time.get_ticks() - m_start > 5000:
                rc_enemy_1.active = rc_enemy_2.active = rc_enemy_3.active = False
                m_start = pygame.time.get_ticks()
        elif rc_player.rect.colliderect(rc_help):
            print("Runner-Chaser Help Portal activated!")
            if pygame.time.get_ticks() - rc_start > 5000:
                pit_1.active = pit_2.active = pit_3.active = False
                rc_start = pygame.time.get_ticks()

        
        if not pit_1.active and pygame.time.get_ticks() - rc_start > 5000:
            pit_1.active = pit_2.active = pit_3.active = True
            rc_start = pygame.time.get_ticks()
        
        if not rc_enemy_1.active and pygame.time.get_ticks() - m_start > 5000:
            rc_enemy_1.active = rc_enemy_2.active = rc_enemy_3.active = True
            m_start = pygame.time.get_ticks()        
        pygame.display.update()
        array = pygame.surfarray.array2d(DisplaySurface)
        # state2 = pack_state()
        # reward1 = ball.win
        # reward2 = ball.win * -1

        # if not state2 in Q.keys():
        #     Q[state2] = [0., 0., 0.]
        # Q[state][action1] = (1-learning_rate) * Q[state][action1] + learning_rate * (reward1 + discount * np.max(Q[state2]))
        # Q[state][action2] = (1-learning_rate) * Q[state][action2] + learning_rate * (reward2 + discount * np.max(Q[state2]))   #Bellman Equation
        # state = state2
        
        
        #pygame.time.wait(0.5)


if __name__ == "__main__":
    main()
    # for i in range(1, num_episodes + 1):
    #     print(i)
    #     main(i)
    #     epsilon *= e_decay
    #     print(epsilon)
    #     print(Q[state])
    # # for keys,values in Q.items():
    # #     print(keys)
    # #     print(values)