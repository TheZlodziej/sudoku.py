import pygame
import random
import copy
from consts import *
from tile import *

def create_tile_map():
    tile_map = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            row.append(Tile(j*(TILE_SIZE[0]+SPACER_WIDTH), i*(TILE_SIZE[1]+SPACER_WIDTH)))
        tile_map.append(row)
    return tile_map

def draw_spacers(window):
    for i in range(1,9):
        pygame.draw.rect(window, SPACER_COLOR, ((TILE_SIZE[0])*i + SPACER_WIDTH*(i-1), 0,SPACER_WIDTH, WINDOW_SIZE[1])) #vertical
        pygame.draw.rect(window, SPACER_COLOR, (0, ((TILE_SIZE[1])*i + SPACER_WIDTH*(i-1)), WINDOW_SIZE[0], SPACER_WIDTH)) #horizontal

def draw_tiles(tile_map, window):
    for row in tile_map:
        for el in row:
            el.draw(window)

def get_pressed_tile(): #returns tuple (x,y)
    mouse_pos = pygame.mouse.get_pos()
    pressed_tile_pos = ((mouse_pos[0] - (mouse_pos[0]//TILE_SIZE[0]) * SPACER_WIDTH)//TILE_SIZE[0], (mouse_pos[1] - (mouse_pos[1]//TILE_SIZE[1]) * SPACER_WIDTH)//TILE_SIZE[1])
    return pressed_tile_pos

def check_if_won(tile_map):
        #lines
        for i in range(9):
            line_v = []
            line_h = []
            for j in range(9):
                line_v.append(tile_map[j][i].value)
                line_h.append(tile_map[i][j].value)
            line_v.sort()
            line_h.sort()
            if line_v != [1,2,3,4,5,6,7,8,9] or line_h != [1,2,3,4,5,6,7,8,9]:
                return False
        #squares
        for l in range(0,3):
            for k in range(0,3):
                square=[]
                for i in range(0+3*l, 3+3*l):
                    for j in range(0+3*k, 3+3*k):
                        square.append(tile_map[i][j].value)
                square.sort()
                if square != [1,2,3,4,5,6,7,8,9]:
                    return False
        return True

def move_selected(destination_tile):
    global tile_map, last_pressed, last_pressed_val

    if last_pressed != destination_tile:
        tile_map[last_pressed[1]][last_pressed[0]].color = TILE_COLOR
        tile_map[last_pressed[1]][last_pressed[0]].selected = False ####
        last_pressed = destination_tile
        last_pressed_val = 0    

def possible_change(val):
    global filled_squares
    for sq in filled_squares:
        if sq == val:
            return False
    return True

def event_handler():
    global running, last_pressed, tile_map, last_pressed_val
    #keyboard input
    pressed_val = last_pressed_val

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                pressed_val = 1
            elif event.key == pygame.K_2:
                pressed_val = 2
            elif event.key == pygame.K_3:
                pressed_val = 3
            elif event.key == pygame.K_4:
                pressed_val = 4
            elif event.key == pygame.K_5:
                pressed_val = 5
            elif event.key == pygame.K_6:
                pressed_val = 6
            elif event.key == pygame.K_7:
                pressed_val = 7
            elif event.key == pygame.K_8:
                pressed_val = 8
            elif event.key == pygame.K_9:
                pressed_val = 9
            elif event.key == pygame.K_r:
                new_game()
            elif event.key == pygame.K_DOWN:
                new_pos = (last_pressed[0], (last_pressed[1]+1)%9)
                move_selected(new_pos)
                pressed_val = tile_map[new_pos[1]][new_pos[0]].value
            elif event.key == pygame.K_UP:
                new_pos = (last_pressed[0], (last_pressed[1]-1)%9)
                move_selected(new_pos)
                pressed_val = tile_map[new_pos[1]][new_pos[0]].value
            elif event.key == pygame.K_RIGHT:
                new_pos = ((last_pressed[0]+1)%9, last_pressed[1])
                move_selected(new_pos)
                pressed_val = tile_map[new_pos[1]][new_pos[0]].value
            elif event.key == pygame.K_LEFT:
                new_pos = ((last_pressed[0]-1)%9, last_pressed[1])
                move_selected(new_pos)
                pressed_val = tile_map[new_pos[1]][new_pos[0]].value
    
    if pressed_val != last_pressed_val and possible_change(last_pressed):
        tile_map[last_pressed[1]][last_pressed[0]].value = pressed_val
        last_pressed_val = pressed_val
    
    #mouse press
    if pygame.mouse.get_pressed()[0]: #if left mouse button pressed
        move_selected(get_pressed_tile())

def update(window):
    tile_map[last_pressed[1]][last_pressed[0]].color = SELECTED_TILE_COLOR
    tile_map[last_pressed[1]][last_pressed[0]].selected = True
    event_handler()
    draw_tiles(tile_map, window)
    draw_spacers(window)
    pygame.display.update()

def gen_puz(x,y,state): #state = arr of [x,y,avail]
    if is_impossible_to_solve(state):
        return None
        
    if x==8 and y==8:
        return state

    available = []
    for s_ in range(9):
        if state[x][y][s_]:
            available.append(s_)

    random.shuffle(available)
    for s_ in available:
        n_state = copy.deepcopy(state)
        add_nb_to_state(s_,x,y,n_state)
        n_x = x+1
        n_y = y
        if n_x == 9:
            n_x = 0
            n_y = n_y + 1

        if n_y == 9:
            return None

        ret = gen_puz(n_x, n_y, n_state)
        if ret is not None:
            return ret
                
def generate_puzzle(blank_squares=50):
    global tile_map, filled_squares
    filled_squares = []
    puzzle = gen_puz(0,0,[[[True for k in range(9)] for j in range(9)] for i in range(9)])

    while blank_squares > 0:
        x = random.randint(0,8)
        y = random.randint(0,8)
        for k in range(9):
            if puzzle[x][y][k]:
                blank_squares -= 1
                puzzle[x][y][k] = False

    for x in range(9):
        for y in range(9):
            for k in range(9):
                if puzzle[x][y][k]:
                    filled_squares.append((x,y))
                    tile_map[y][x].value = k+1
                    tile_map[y][x].filled = True
                    break

    #not (x & y) == (not x) or (not y) 
    #not (x | y) == (not x) and (not y)

def add_nb_to_state(nb,x,y,state):
    for i in range(9):
        assert nb != i or state[x][y][i]
        state[x][y][i] = (nb == i)

    for i in range(9):
        if i != x:
            state[i][y][nb] = False
        if i != y:
            state[x][i][nb] = False

    sq_x = x//3
    sq_y = y//3
    for sq_x_ in range(3):
        for sq_y_ in range(3):
            x_ = sq_x*3 + sq_x_
            y_ = sq_y*3 + sq_y_
            if x_ != x and y_ != y:
                state[x_][y_][nb] = False
    
def is_impossible_to_solve(state):
    for x in range(9):
        for y in range(9):
            same_zera = True
            for i in range(9):
                if state[x][y][i]:
                    same_zera=False
                    break
            if same_zera:
                return True
    return False
                
def new_game():
    global tile_map, last_pressed, last_pressed_val
    tile_map = create_tile_map()
    last_pressed = (0, 0)
    last_pressed_val = 0
    generate_puzzle()

#--main--
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)
running = True
clock = pygame.time.Clock()
last_pressed = (0, 0)
last_pressed_val = 0
tile_map = create_tile_map()
filled_squares = []

new_game()

while running:
    clock.tick(FPS)
    update(window)
    if(check_if_won(tile_map)):
        print("win!")
        running = False
pygame.quit()
quit()