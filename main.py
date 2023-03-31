import pygame
from pygame.locals import *

from MazeGame.MazePlayer import MazePlayer
from MazeGame.MazeLavaPit import MazeLavaPit
from RunnerChaser.Runner import Runner
from RunnerChaser.Chaser import Chaser

import numpy as np
import sys
import math
import json

np.set_printoptions(threshold=sys.maxsize)
num_episodes = 1000
discount = 0.8
learning_rate = 0.9
epsilon = 0.99
m_epsilon = 1
rc_epsilon = 1
e_decay = 0.75**(1/num_episodes)


Q_m = {}
Q_rc = {}


with open("Maze_Q_Table.json") as file:
    Q_m = json.load(file)
file.close()
with open("Tag_Q_Table.json") as file:
    Q_rc = json.load(file)

def main(i):

    global epsilon
    global m_epsilon
    global rc_epsilon

    m_player = MazePlayer(7.5, 7.5)
    rc_player = Runner(1007.5, 457.5)
    rc_enemy_1 = Chaser(812.5, 547.5)
    #rc_enemy_2 = Chaser(1007.5, 532.5)
    #rc_enemy_3 = Chaser(1157.5, 397.5)
    pit_1 = MazeLavaPit(405, 30, 15*5, 15*18)
    pit_2 = MazeLavaPit(45, 405, 15*15, 15*5)
    pit_3 = MazeLavaPit(390, 420, 15*5, 15*5)
    m_goal = pygame.Rect(540, 540, 60, 60)
    rc_goal = pygame.Rect(970, 0, 60, 60)
    m_help = pygame.Rect(135, 0, 60, 45)
    rc_help = pygame.Rect(1135, 0, 60, 45)


    m_reward = 0
    rc_reward = 0

    pygame.init()
    pygame.display.set_caption("An exciting game of pong")
    screen = pygame.display.set_mode((1300, 600))
    FPS = pygame.time.Clock()
    FPS.tick(30)
    DisplaySurface = pygame.display.set_mode((1300, 600))
    DisplaySurface.fill((0, 0, 0))

    def pack_state_maze():
        player_x = str(int((m_player.rect.centerx - 7.5)/15)).zfill(2)
        player_y = str(int((m_player.rect.centery - 7.5)/15)).zfill(2)
        lava_pit = str(1 if pit_1.active else 0)
        return player_x + player_y + lava_pit

    
    def pack_state_rc():
        player_x = str(int((rc_player.rect.centerx - 7.5)/15)).zfill(2)
        player_y = str(int((rc_player.rect.centery - 7.5)/15)).zfill(2)
        enemy_x = str(int((rc_enemy_1.rect.centerx - 7.5 - 700)/15)).zfill(2)
        enemy_y = str(int((rc_enemy_1.rect.centery - 7.5)/15)).zfill(2)
        lava_pit = str(1 if pit_1.active else 0)
        return player_x + player_y + enemy_x + enemy_y + lava_pit
    
    running = True
    rc_start = pygame.time.get_ticks()
    m_start = pygame.time.get_ticks()
    m_run = True
    rc_run = True
    while running:
        # pressed_key = pygame.key.get_pressed()
        # if pressed_key[K_SPACE]:
        #     break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        m_state = pack_state_maze()
        rc_state = pack_state_rc()


        if not m_state in Q_m.keys():
            Q_m[m_state] = [0., 0., 0., 0., 0.]

        if np.random.rand() > (1 - epsilon):
            m_action = np.random.randint(0, 5)
        else:
            #print("Taken q value action")
            m_action = np.argmax(Q_m[m_state])

        
        if not rc_state in Q_rc.keys():
            Q_rc[rc_state] = [0., 0., 0., 0., 0.]

        if np.random.rand() > (1 - epsilon):
            rc_action = np.random.randint(0, 5)
        else:
            #print("Taken q value action")
            rc_action = np.argmax(Q_rc[rc_state])
        

        DisplaySurface.fill((0, 0, 0))

        pygame.draw.line(DisplaySurface, (100, 100, 100), (600, 0), (600, 600))
        pygame.draw.line(DisplaySurface, (100, 100, 100), (700, 0), (700, 600))
        for i in range(0, 600, 15):
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i, 0), (i, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (0, i), (600, i))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i+700, 0), (i+700, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (700, i), (1300, i))
        
        if m_run:
            m_player.update(m_action)
        pit_1.draw(DisplaySurface)
        pit_2.draw(DisplaySurface)
        pit_3.draw(DisplaySurface)
        pygame.draw.rect(DisplaySurface, (0, 0, 230), m_goal)
        pygame.draw.rect(DisplaySurface, (33, 115, 55), m_help)
        m_player.draw(DisplaySurface)

        if rc_run:
            rc_player.update(rc_action)
            rc_enemy_1.update(rc_player)
        #rc_status2 = rc_enemy_2.update(rc_player, rc_enemy_1, rc_enemy_3)
        #rc_status3 = rc_enemy_3.update(rc_player, rc_enemy_1, rc_enemy_2)
        rc_enemy_1.draw(DisplaySurface)
        #rc_enemy_2.draw(DisplaySurface)
        #rc_enemy_3.draw(DisplaySurface)
        pygame.draw.rect(DisplaySurface, (0, 0, 230), rc_goal)
        pygame.draw.rect(DisplaySurface, (33, 115, 55), rc_help)
        rc_player.draw(DisplaySurface)
        
        
        m_reward = -0.1
        rc_reward = -0.1

        if (m_player.rect.colliderect(pit_1.rect) or m_player.rect.colliderect(pit_2.rect) or m_player.rect.colliderect(pit_3.rect)) and pit_1.active :
            m_run = False
            m_reward += -10
            rc_reward += -0.5
        if rc_player.rect.colliderect(rc_enemy_1):
            rc_run = False
            m_reward += -0.5
            rc_reward += -10
        if m_player.rect.colliderect(m_help) and rc_run:
            if pygame.time.get_ticks() - m_start > 5000:
                print("Maze Help Portal activated!")
                rc_enemy_1.active = False
                m_reward += m_epsilon * 2
                m_epsilon *= 0.9999
                m_start = pygame.time.get_ticks()
        if rc_player.rect.colliderect(rc_help) and m_run:
            if pygame.time.get_ticks() - rc_start > 5000:
                print("Runner-Chaser Help Portal activated!")
                pit_1.active = pit_2.active = pit_3.active = False
                rc_reward += rc_epsilon * 2
                rc_epsilon *= 0.9999
                rc_start = pygame.time.get_ticks()
        
        if m_player.rect.colliderect(m_goal):
            m_run = False
            m_reward += 10
            rc_reward += 1
        if rc_player.rect.colliderect(rc_goal):
            r_run = False
            rc_reward += 10
            m_reward += 1

        
        if not pit_1.active and pygame.time.get_ticks() - rc_start > 5000:
            pit_1.active = pit_2.active = pit_3.active = True
            rc_start = pygame.time.get_ticks()
        
        if not rc_enemy_1.active and pygame.time.get_ticks() - m_start > 5000:
            rc_enemy_1.active = True
            m_start = pygame.time.get_ticks()        
        pygame.display.update()

        m_state2 = pack_state_maze()
        rc_state2 = pack_state_rc()
        

        if not m_state2 in Q_m.keys():
            Q_m[m_state2] = [0., 0., 0., 0., 0.]
        if not rc_state2 in Q_rc.keys():
            Q_rc[rc_state2] = [0., 0., 0., 0., 0.]
        
        if m_run:
            Q_m[m_state][m_action] = (1-learning_rate) * Q_m[m_state][m_action] + learning_rate * (m_reward + discount * np.max(Q_m[m_state2]))
        if rc_run:
            Q_rc[rc_state][rc_action] = (1-learning_rate) * Q_rc[rc_state][rc_action] + learning_rate * (rc_reward + discount * np.max(Q_rc[rc_state2]))
        
        running = m_run or rc_run
        #pygame.time.wait(50)


if __name__ == "__main__":
    #main()
    for i in range(1, num_episodes + 1):
        print(i)
        main(i)
        epsilon *= e_decay
        print(epsilon)
        with open("Maze_Q_Table.json", "w") as file:
          json.dump(Q_m, file)
        file.close()
        with open("Tag_Q_Table.json", "w") as file:
          json.dump(Q_rc, file)
        file.close()
    # # for keys,values in Q.items():
    # #     print(keys)
    # #     print(values)