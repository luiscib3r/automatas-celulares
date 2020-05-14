import pygame
import numpy as np
import time

# Dimensions of game screen
width, height = 700, 700

# Game screen
screen = pygame.display.set_mode((width, height))

# Background color
bg = 25, 25, 25

screen.fill(bg)

# Number of cell (horizontal - vertical)
nxC, nyC = 50, 50

# Width and Height of a cell
dimCW = width / nxC
dimCH = height / nyC

# initial game state (all in zero)
gameState = np.zeros((nxC, nyC))

# Some structures

# Walking
gameState[24, 24] = 1
gameState[25, 25] = 1
gameState[25, 26] = 1
gameState[24, 26] = 1
gameState[23, 26] = 1

# Tube
# gameState[30, 20] = 1
# gameState[31, 20] = 1
# gameState[32, 20] = 1

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
                newGameState = np.zeros((nxC, nyC))

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

                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[x % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, y % nyC] + \
                          gameState[(x + 1) % nxC, y % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[x % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # rules of classic game of live
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                elif gameState[x, y] == 1 and (n_neigh < 1 or n_neigh > 4):
                    newGameState[x, y] = 0

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
