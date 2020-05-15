import pygame
import numpy as np
import time

# Read number for specific rule
usr_input = input('Enter rule number [0 - 255]: ')

if usr_input == 'r':
    usr_input = np.random.randint(0, 256)

rule = 0

try:
    rule = int(usr_input)
except ValueError:
    print('Rule number out of range [0-255]')
    exit(0)

if rule < 0 or rule > 255:
    print('Rule number out of range [0-255]')
    exit(0)

rule = np.binary_repr(rule, width=8)

# make rule as a list of integers
rule = [int(c) for c in rule]
rule.reverse()

print('Working with rule number: {} - {}'.format(usr_input, rule))

# Dimensions of game screen
width, height = 1000, 700

# Game screen
screen = pygame.display.set_mode((width, height))

# Background color
bg = 25, 25, 25

screen.fill(bg)

# Number of cell (horizontal - vertical)
nxC, nyC = 60, 60

# Width and Height of a cell
dimCW = width / nxC
dimCH = height / nyC

# initial game state (all in zero)
gameState = np.zeros((nxC, nyC), dtype=int)

# Initial state
gameState[int(nxC / 2), 0] = 1

# To stop and start execution
pauseExec = True  # when start the game is paused (press any key to start)

while True:
    # Make new game state
    newGameState = np.copy(gameState)

    # Background fill
    screen.fill(bg)

    # Delay for execution
    time.sleep(0.1)

    # get all events
    ev = pygame.event.get()

    for event in ev:
        # any key to pause or start de game
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

            # [q] to exit
            if event.unicode == 'q':
                exit(0)

            # [l] to clear (all cell to zero)
            if event.unicode == 'l':
                newGameState = np.zeros((nxC, nyC), dtype=int)

        # use mouse to set cell to one (live)
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = 1

    # apply rules to update game state
    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExec:
                # get rule id [0 - 7]
                ruleIdx = 4 * gameState[(x-1) % nxC, y] + 2 * gameState[x, y] + 1 * gameState[(x+1) % nxC, y]

                if y < (nxC - 1):
                    newGameState[x, y+1] = rule[ruleIdx]

            # draw cell in black o white (0 - 1)
            poly = [(x * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x * dimCW, (y + 1) * dimCH)]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # update game state
    gameState = np.copy(newGameState)

    # update screen
    pygame.display.flip()
