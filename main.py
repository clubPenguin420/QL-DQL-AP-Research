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

discount = 0.9
e_decay = 0.65**(1/5000)
l_decay = 0.70**(1/5000)
params = {}
episode_num = 0
epsilon = 0
m_epsilon = 0
rc_epsilon = 0
learning_rate = 0
m_wins = 0
rc_wins = 0
m_help_counter = 0
rc_help_counter = 0


with open("parameters.json") as p_file:
    params = json.load(p_file)
    m_epsilon = params["m_epsilon"]
    rc_epsilon = params["rc_epsilon"]
    epsilon = params["epsilon"]
    episode_num = params["episode#"]
    learning_rate = params["learning_rate"]
    m_wins = params["m_wins"]
    rc_wins = params["rc_wins"]
p_file.close()
#num_episodes = 1000



Q_m = {}
Q_rc = {}

data = {}




with open("Maze_Q_Table4.json") as file:
    Q_m = json.load(file)
file.close()
with open("Tag_Q_Table4.json") as file:
    Q_rc = json.load(file)
file.close()

with open("graphing_data4.json") as file:
    data = json.load(file)
file.close()


def main(i):

    global epsilon
    global m_epsilon
    global rc_epsilon
    global m_wins
    global rc_wins
    global m_help_counter
    global rc_help_counter

    m_player = MazePlayer(7.5, 7.5)
    rc_player = Runner(1007.5, 457.5)
    rc_enemy_1 = Chaser(707.5, 547.5)
    rc_enemy_2 = Chaser(1007.5 - 15*3, 232.5)
    #rc_enemy_3 = Chaser(1157.5, 397.5)
    pit_1 = MazeLavaPit(405, 45, 15*5, 15*15)
    pit_2 = MazeLavaPit(45, 435, 15*14, 15*5)
    pit_3 = MazeLavaPit(60, 15*10, 15*3, 15*3)
    #m_goal = pygame.Rect(540, 540, 60, 60)
    m_goal = pygame.Rect(390-15*10, 420-15*8, 60, 60)
    rc_goal = pygame.Rect(1135+15*5, 285+15*4, 60, 60)
    m_help = pygame.Rect(105+15*8, 15*8, 60, 45)
    rc_help = pygame.Rect(1180-15*3, 465, 60, 45)


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
        enemy1_x = str(int((rc_enemy_1.rect.centerx - 7.5 - 700)/15)).zfill(2)
        enemy1_y = str(int((rc_enemy_1.rect.centery - 7.5)/15)).zfill(2)
        enemy2_x = str(int((rc_enemy_2.rect.centerx - 7.5 - 700)/15)).zfill(2)
        enemy2_y = str(int((rc_enemy_2.rect.centery - 7.5)/15)).zfill(2)
        enemy_active = str(1 if rc_enemy_1.active else 0)
        return player_x + player_y + enemy1_x + enemy1_y + enemy2_x + enemy2_y + enemy_active
    
    running = True
    rc_start = pygame.time.get_ticks()
    m_start = pygame.time.get_ticks()
    m_run = True
    rc_run = True
    mh_activated = False
    rch_activated = False
    rc_enemy_counter = -5
    m_help_counter = 0
    rc_help_counter = 0
    run_counter = 0
    pm_state = 0
    pm_action = 0
    prc_state = 0
    prc_action = 0
    tm_state = False
    trc_state = False
    while running and run_counter < 120:
        # pressed_key = pygame.key.get_pressed()
        # if pressed_key[K_SPACE]:
        #     break
        
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
            if rc_enemy_counter % 2 == 0 and rc_enemy_counter > 0:
                rc_enemy_1.update_c(rc_player, rc_enemy_2)
                rc_enemy_2.update_c(rc_player, rc_enemy_1)
            rc_enemy_counter += 1
        #rc_status2 = rc_enemy_2.update(rc_player, rc_enemy_1, rc_enemy_3)
        #rc_status3 = rc_enemy_3.update(rc_player, rc_enemy_1, rc_enemy_2)
        rc_enemy_1.draw(DisplaySurface)
        rc_enemy_2.draw(DisplaySurface)
        #rc_enemy_3.draw(DisplaySurface)
        pygame.draw.rect(DisplaySurface, (0, 0, 230), rc_goal)
        pygame.draw.rect(DisplaySurface, (33, 115, 55), rc_help)
        rc_player.draw(DisplaySurface)
        
        
        
        if m_run:
            if (m_player.rect.colliderect(pit_1.rect) or m_player.rect.colliderect(pit_2.rect) or m_player.rect.colliderect(pit_3.rect)) and pit_1.active :
                m_run = False
                m_reward += -15
                tm_state = True
            if m_player.rect.colliderect(m_help):
                if (pygame.time.get_ticks() - m_start > 7000 or m_help_counter == 0):
                    #print("Maze Help Portal activated!")
                    m_help_counter += 1
                    if rc_run:
                        mh_activated = True
                        rc_enemy_1.active = rc_enemy_2.active = False
                        m_reward += m_epsilon * 2
                        m_epsilon *= 0.99
                    else:
                        m_reward += 0 * m_epsilon
                    m_start = pygame.time.get_ticks()
        if rc_run:
            if rc_player.rect.colliderect(rc_enemy_1) or rc_player.rect.colliderect(rc_enemy_2):
                rc_run = False
                rc_reward += -15
                trc_state = True

            if rc_player.rect.colliderect(rc_help):
                if (pygame.time.get_ticks() - rc_start > 7000 or rc_help_counter == 0):
                    # print("Runner-Chaser Help Portal activated!")
                    rc_help_counter += 1
                    if m_run:
                        rch_activated = True
                        pit_1.active = pit_2.active = pit_3.active = False
                        rc_reward += rc_epsilon * 2
                        rc_epsilon *= 0.99
                    else:
                        rc_reward += 0 * rc_epsilon
                    rc_start = pygame.time.get_ticks()
        
        if m_run:
            if m_player.rect.colliderect(m_goal):
                m_run = False
                tm_state = True
                m_wins += 1
                m_reward += 30
                if rch_activated:
                    rc_reward += 0.5
        
        if rc_run:
            if rc_player.rect.colliderect(rc_goal):
                rc_run = False
                trc_state = True
                rc_wins += 1
                rc_reward += 30
                if mh_activated:
                    m_reward += 0.5

        
        if not pit_1.active and pygame.time.get_ticks() - rc_start > 7000:
            pit_1.active = pit_2.active = pit_3.active = True
            rc_start = pygame.time.get_ticks()
        
        if not rc_enemy_1.active and pygame.time.get_ticks() - m_start > 7000:
            rc_enemy_1.active = rc_enemy_2.active = True
            m_start = pygame.time.get_ticks()        
        pygame.display.update()

        m_state2 = pack_state_maze()
        rc_state2 = pack_state_rc()
        

        if not m_state2 in Q_m.keys():
            Q_m[m_state2] = [0., 0., 0., 0., 0.]
        if not rc_state2 in Q_rc.keys():
            Q_rc[rc_state2] = [0., 0., 0., 0., 0.]
        
        if m_run:
            if run_counter != 0:
                if tm_state:
                    Q_m[pm_state][pm_action] = (1-learning_rate) * Q_m[pm_state][pm_action] + m_reward
                    tm_state = False
                else:
                    Q_m[m_state][m_action] = (1-learning_rate) * Q_m[m_state][m_action] + learning_rate * (m_reward + discount * np.max(Q_m[m_state2]))
            #print("Maze Reward: " + str(m_reward))
        if rc_run:
            if run_counter != 0:
                if trc_state:
                    Q_rc[prc_state][prc_action] = (1-learning_rate) * Q_rc[prc_state][prc_action] + rc_reward
                    trc_state = False
                else:
                    Q_rc[rc_state][rc_action] = (1-learning_rate) * Q_rc[rc_state][rc_action] + learning_rate * (rc_reward + discount * np.max(Q_rc[rc_state2]))
            #print("Tag Reward: " + str(rc_reward))
        
        pm_state = m_state
        pm_action = m_action
        prc_state = rc_state
        prc_action = rc_action
        
        
        running = m_run or rc_run
        run_counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        #pygame.time.wait(300)


if __name__ == "__main__":
    #main()
    while episode_num <= 25000:
        print("Episode #: " + str(episode_num))
        main(episode_num)
        epsilon *= e_decay
        learning_rate *= l_decay
        print("Epsilon: " + str(epsilon))
        print("Maze Help Epsilon: " + str(m_epsilon))
        print("Tag Help Epsilon: " + str(rc_epsilon))
        print("Learning Rate: " + str(learning_rate))
        print("Maze Wins: " + str(m_wins))
        print("Tag Wins: " + str(rc_wins))
        print("\n\n\n")

        data[episode_num] = [m_wins, rc_wins, m_help_counter, rc_help_counter]

        if episode_num % 50 == 0:
            with open("Maze_Q_Table4.json", "w") as m_file:
              json.dump(Q_m, m_file)
            m_file.close()
            with open("Tag_Q_Table4.json", "w") as t_file:
              json.dump(Q_rc, t_file)
            t_file.close()
            with open("parameters.json", "w") as p_file:
                params["episode#"] = episode_num
                params["epsilon"] = epsilon
                params["m_epsilon"] = m_epsilon
                params["rc_epsilon"] = rc_epsilon
                params["learning_rate"] = learning_rate
                params["m_wins"] = m_wins
                params["rc_wins"] = rc_wins
                json.dump(params, p_file)
            p_file.close()
            with open("graphing_data4.json", "w") as g_file:
                json.dump(data, g_file)
            g_file.close()
        episode_num += 1
    # # for keys,values in Q.items():
    # #     print(keys)
    # #     print(values)