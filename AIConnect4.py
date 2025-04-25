import numpy as np
import random
import pygame
import sys
import math
import time
import sys
sys.setrecursionlimit(10000)

# Initialize the mixer for sound
pygame.mixer.init()

# Enhanced colors - more vibrant palette
BLUE = (37, 97, 163)  # Deeper blue for the board
DARK_BLUE = (23, 64, 111)  # For board outline
BLACK = (0, 0, 0)
RED = (217, 48, 48)  # Brighter red
YELLOW = (242, 208, 39)  # More golden yellow
GREEN = (52, 168, 83)  # Richer green
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)  # Background color
PURPLE = (128, 0, 128)
LIGHT_PURPLE = (153, 50, 204)
BOARD_BG = (53, 116, 201)  # Slightly different shade for board background
TRANSPARENT = (173, 216, 230)
# Game constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 8)  # Slightly smaller pieces for more space

PLAYER1 = 0
PLAYER2 = 1
AI = 2

EMPTY = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
AI_PIECE = 3

WINDOW_LENGTH = 4

DIFF_LEVEL = 4

# Adding animation effects
def animate_piece_drop(board, row, col, piece, screen, SQUARESIZE, height, RADIUS):
    color = BLACK
    if piece == PLAYER1_PIECE:
        color = RED
    elif piece == PLAYER2_PIECE:
        color = YELLOW
    elif piece == AI_PIECE:
        color = GREEN
    
    # Calculate start and end positions
    start_y = SQUARESIZE / 2
    end_y = height - (row * SQUARESIZE + SQUARESIZE / 2)
    
    # Number of animation frames
    frames = 10
    speed = (end_y - start_y) / frames
    # Load the sound
    sound1 = pygame.mixer.Sound("hit1.mp3")
    sound2 = pygame.mixer.Sound("hit2.mp3")

    # Choose one at random
    sound_chosen = random.choice([sound1, sound2])
    sound = pygame.mixer.Sound(sound_chosen)  # Replace with your sound file
    
    # Play the sound
    sound.play()
    for i in range(frames + 1):
        # Redraw the board without the new piece
        draw_board_only(board, screen, SQUARESIZE, height, RADIUS)
        
        # Calculate current y position
        current_y = min(start_y + speed * i, end_y)
        
        # Draw the piece at current position
        pygame.draw.circle(screen, color, (int(col * SQUARESIZE + SQUARESIZE / 2), int(current_y)), RADIUS)
        pygame.display.update()
        pygame.time.wait(20)  # Control animation speed
    
    sound.stop()
    # Choose one at random
#   if random.choice([True,False]):
#        sound3.play()
    # Actually update the board data after animation
    board[row][col] = piece

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.font = font
        self.action = action
        self.is_hovered = False
        self.pulse = 0
        self.pulse_dir = 1
        
    def draw(self, screen):
        # Pulsing effect when hovered
        
        

        if self.is_hovered:
            self.pulse += 0.1 * self.pulse_dir
            if self.pulse > 1:
                self.pulse = 1
                self.pulse_dir = -1
            elif self.pulse < 0:
                self.pulse = 0
                self.pulse_dir = 1
                
            # Interpolate between normal and hover color
            r = self.color[0] + (self.hover_color[0] - self.color[0]) * self.pulse
            g = self.color[1] + (self.hover_color[1] - self.color[1]) * self.pulse
            b = self.color[2] + (self.hover_color[2] - self.color[2]) * self.pulse
            color = (r, g, b)
            
            # Slight growth when hovered
            rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4)
            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)  # White outline
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
            
        # Render text with slight shadow
        shadow_surf = self.font.render(self.text, True, (0, 0, 0, 128))
        shadow_rect = shadow_surf.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        screen.blit(shadow_surf, shadow_rect)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def check_clicked(self, mouse_pos, mouse_clicked):
        # Check if the button is clicked
        if self.rect.collidepoint(mouse_pos) and mouse_clicked:
            if self.action:
                sound = pygame.mixer.Sound("button.mp3")
                sound.play()
                return self.action()
            return True
        return False

def create_gradient_background(width, height, start_color, end_color):
    background = pygame.Surface((width, height))
    for y in range(height):
        # Calculate color for this row
        r = start_color[0] + (end_color[0] - start_color[0]) * y / height
        g = start_color[1] + (end_color[1] - start_color[1]) * y / height
        b = start_color[2] + (end_color[2] - start_color[2]) * y / height
        row_color = (int(r), int(g), int(b))
        
        # Draw row with this color
        pygame.draw.line(background, row_color, (0, y), (width, y))
    return background

def set_diff(diff):
    global DIFF_LEVEL
    DIFF_LEVEL = diff
    return show_menu()

def select_diff():
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Connect 4 - Abdul Tawab | Sahir Hassan | Muzaffar Ali | Fakhurddin - Select Difficulty")
    icon = pygame.image.load('icon.ico')  # Make sure 'icon.ico' is in the same folder as your script
    pygame.display.set_icon(icon)
    font = pygame.font.SysFont("arial", 40, bold=True)
    title_font = pygame.font.SysFont("verdana", 70, bold=True)
    
    # Create gradient background
    background = create_gradient_background(700, 500, (135, 206, 250), (65, 105, 225))
    
    # Render the title with shadow effect
    title_shadow = title_font.render("Connect 4", True, (0, 0, 0))
    title_text = title_font.render("Connect 4", True, YELLOW)
    
    # Create buttons with enhanced colors
    two_player_button = Button(200, 200, 300, 60, "Easy", DARK_BLUE, BLUE, WHITE, font, lambda: set_diff(1))
    three_player_button = Button(200, 300, 300, 60, "Medium", DARK_BLUE, BLUE, WHITE, font, lambda: set_diff(2))
    quit_button = Button(200, 400, 300, 60, "Hard", DARK_BLUE, BLUE, WHITE, font, lambda: set_diff(4))

    buttons = [two_player_button, three_player_button, quit_button]
    
    # Create particle effects for background
    particles = []
    for i in range(30):
        x = random.randint(0, 700)
        y = random.randint(0, 500)
        size = random.randint(2, 5)
        speed = random.uniform(0.5, 1.5)
        particles.append([x, y, size, speed])

    clock = pygame.time.Clock()
    
    while True:
        screen.blit(background, (0, 0))
        
        # Update and draw particles
        for p in particles:
            p[1] += p[3]  # Move particle down
            if p[1] > 500:
                p[1] = 0
                p[0] = random.randint(0, 700)
            
            pygame.draw.circle(screen, (255, 255, 255, 128), (int(p[0]), int(p[1])), p[2])
        
        # Draw title with shadow effect
        screen.blit(title_shadow, (152, 72))
        screen.blit(title_text, (150, 70))
        
        # Draw and update buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
            result = button.check_clicked(mouse_pos, mouse_clicked)
            if result:
                return result

        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS



def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Connect 4 | Number of Players")
    font = pygame.font.SysFont("arial", 40, bold=True)
    title_font = pygame.font.SysFont("verdana", 70, bold=True)
    
    # Create gradient background
    background = create_gradient_background(700, 500, (135, 206, 250), (65, 105, 225))
    
    # Render the title with shadow effect
    title_shadow = title_font.render("Connect 4", True, (0, 0, 0))
    title_text = title_font.render("Connect 4", True, YELLOW)
    
    # Create buttons with enhanced colors
    two_player_button = Button(200, 200, 300, 60, "Two Player", DARK_BLUE, BLUE, WHITE, font, lambda: (1, 1))
    three_player_button = Button(200, 300, 300, 60, "Three Player", DARK_BLUE, BLUE, WHITE, font, lambda: show_three_player_menu())
    quit_button = Button(200, 400, 300, 60, "Back", DARK_BLUE, BLUE, WHITE, font, lambda: 'back')

    buttons = [two_player_button, three_player_button, quit_button]
    
    # Create particle effects for background
    particles = []
    for i in range(30):
        x = random.randint(0, 700)
        y = random.randint(0, 500)
        size = random.randint(2, 5)
        speed = random.uniform(0.5, 1.5)
        particles.append([x, y, size, speed])

    clock = pygame.time.Clock()
    
    while True:
        screen.blit(background, (0, 0))
        
        # Update and draw particles
        for p in particles:
            p[1] += p[3]  # Move particle down
            if p[1] > 500:
                p[1] = 0
                p[0] = random.randint(0, 700)
            
            pygame.draw.circle(screen, (255, 255, 255, 128), (int(p[0]), int(p[1])), p[2])
        
        # Draw title with shadow effect
        screen.blit(title_shadow, (152, 72))
        screen.blit(title_text, (150, 70))
        
        # Draw and update buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
            result = button.check_clicked(mouse_pos, mouse_clicked)
            if result:
                if result == "back":
                    return select_diff()  # Return to main menu
                return result  # Return the selected option

        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS

def is_board_full(board):
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            return False
    return True

def create_board():
    return np.zeros((ROW_COUNT,COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True, [(r, c+i) for i in range(4)]

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True, [(r+i, c) for i in range(4)]

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True, [(r+i, c+i) for i in range(4)]

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True, [(r-i, c+i) for i in range(4)]
    return False, []

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER1_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 20
    
    return score

def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    score += center_array.count(piece) * 6

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    return score

def minimax(board, depth, alpha, beta, maximizingPlayer, piece, opponent_piece):
    valid_locations = get_valid_locations(board)
    is_terminal = any(winning_move(board, p)[0] for p in [PLAYER1_PIECE, PLAYER2_PIECE, AI_PIECE]) or len(valid_locations) == 0

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, piece)[0]:
                return (None, 100000000000000)
            elif winning_move(board, opponent_piece)[0]:
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, piece))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, piece)
            new_score = minimax(b_copy, depth-1, alpha, beta, False, piece, opponent_piece)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, opponent_piece)
            new_score = minimax(b_copy, depth-1, alpha, beta, True, piece, opponent_piece)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def draw_board_only(board, screen, SQUARESIZE, height, RADIUS):
    # Draw blue board with curved edges
    board_rect = pygame.Rect(0, SQUARESIZE, COLUMN_COUNT * SQUARESIZE, ROW_COUNT * SQUARESIZE)
    pygame.draw.rect(screen, BOARD_BG, board_rect, border_radius=15)
    pygame.draw.rect(screen, DARK_BLUE, board_rect, 4, border_radius=15)  # Add a border
    
    # Draw grid and holes
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Draw inner shadow for each hole
            pygame.draw.circle(screen, DARK_BLUE, 
                              (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), 
                              RADIUS + 2)
            # Draw actual hole
            pygame.draw.circle(screen, BLACK, 
                              (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), 
                              RADIUS)
    
    # Draw pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] != 0:
                color = BLACK
                if board[r][c] == PLAYER1_PIECE:
                    color = RED
                elif board[r][c] == PLAYER2_PIECE:
                    color = YELLOW
                elif board[r][c] == AI_PIECE:
                    color = GREEN
                
                piece_y = height - int(r*SQUARESIZE+SQUARESIZE/2)
                
                # Draw highlight on piece (3D effect)
                highlight_pos = (int(c*SQUARESIZE+SQUARESIZE/2 - RADIUS/3), 
                                piece_y - RADIUS/3)
                highlight_radius = RADIUS//4
                
                # Draw main piece
                pygame.draw.circle(screen, color, 
                                  (int(c*SQUARESIZE+SQUARESIZE/2), piece_y), 
                                  RADIUS)
                
                # Add highlight to create 3D effect
                if color != BLACK:
                    lighter_color = tuple(min(c + 70, 255) for c in color)
                    pygame.draw.circle(screen, lighter_color, highlight_pos, highlight_radius)
prev_col= col = None
def draw_board(board, screen, SQUARESIZE, height, RADIUS, winning_pieces=None, turn = None):
    global prev_col, col
    # Clear the screen with background color
    sound = pygame.mixer.Sound("colhover.mp3")
    screen.fill(LIGHT_BLUE)
    if turn == PLAYER1:
        color = RED
    elif turn == PLAYER2:
        color = YELLOW
    elif turn == AI:
        color = TRANSPARENT
    # Draw column indicator (where piece will drop)
    if pygame.mouse.get_focused():
        print(col, prev_col)
        mouse_x = pygame.mouse.get_pos()[0]
        col = min(COLUMN_COUNT-1, max(0, mouse_x // SQUARESIZE))
        if col != prev_col:
            sound.play()
            print('play2')
            prev_col = col
        pygame.draw.polygon(screen, color, [
            (col * SQUARESIZE + SQUARESIZE/2 - 15, 20),
            (col * SQUARESIZE + SQUARESIZE/2 + 15, 20),
            (col * SQUARESIZE + SQUARESIZE/2, 50)
        ])
    
    # Draw the board
    draw_board_only(board, screen, SQUARESIZE, height, RADIUS)
    
    # Highlight winning pieces if any
    if winning_pieces:
        for r, c in winning_pieces:
            # Draw animation for winning pieces
            color = BLACK
            if board[r][c] == PLAYER1_PIECE:
                color = RED
            elif board[r][c] == PLAYER2_PIECE:
                color = YELLOW
            elif board[r][c] == AI_PIECE:
                color = GREEN
                
            # Draw animated highlight around winning pieces
            highlight_radius = RADIUS + 5 + 3 * math.sin(pygame.time.get_ticks() / 200)
            pygame.draw.circle(screen, WHITE, 
                              (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), 
                              int(highlight_radius), 3)
    
    pygame.display.update()

def show_three_player_menu():
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Connect 4 - Three Player Configuration")
    font = pygame.font.SysFont("arial", 40, bold=True)
    title_font = pygame.font.SysFont("verdana", 50, bold=True)

    # Create gradient background
    background = create_gradient_background(700, 500, (135, 206, 250), (65, 105, 225))

    # Render the title with shadow
    title_shadow = title_font.render("Three Player Mode", True, BLACK)
    title_text = title_font.render("Three Player Mode", True, YELLOW)

    # Create buttons
    option1_button = Button(200, 200, 300, 60, "1 Human, 2 AI", DARK_BLUE, BLUE, WHITE, font, lambda: (1, 2))
    option2_button = Button(200, 300, 300, 60, "2 Humans, 1 AI", DARK_BLUE, BLUE, WHITE, font, lambda: (2, 1))
    back_button = Button(200, 400, 300, 60, "Back", DARK_BLUE, BLUE, WHITE, font, lambda: "back")

    buttons = [option1_button, option2_button, back_button]
    
    # Create particle effects for background
    particles = []
    for i in range(30):
        x = random.randint(0, 700)
        y = random.randint(0, 500)
        size = random.randint(2, 5)
        speed = random.uniform(0.5, 1.5)
        particles.append([x, y, size, speed])

    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, 0))
        
        # Update and draw particles
        for p in particles:
            p[1] += p[3]  # Move particle down
            if p[1] > 500:
                p[1] = 0
                p[0] = random.randint(0, 700)
            
            pygame.draw.circle(screen, (255, 255, 255, 128), (int(p[0]), int(p[1])), p[2])

        # Draw title with shadow
        screen.blit(title_shadow, (102, 72))
        screen.blit(title_text, (100, 70))

        # Draw and update buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
            result = button.check_clicked(mouse_pos, mouse_clicked)
            if result:
                if result == "back":
                    return show_menu()  # Return to main menu
                return result  # Return the selected option

        pygame.display.update()
        clock.tick(60)

def display_winner(screen, message, color):
    # Create semi-transparent overlay
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(180)  # Transparency
    overlay.fill((0, 0, 0))  # Black overlay
    screen.blit(overlay, (0, 0))
    
    # Create text
    font = pygame.font.SysFont("verdana", 70, bold=True)
    text_shadow = font.render(message, True, BLACK)
    text = font.render(message, True, color)
    
    # Position text in center
    shadow_rect = text_shadow.get_rect(center=(screen.get_width()//2 + 3, screen.get_height()//2 + 3))
    text_rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    
    # Draw text with shadow
    screen.blit(text_shadow, shadow_rect)
    screen.blit(text, text_rect)
    
    # Add "Play Again" message
    small_font = pygame.font.SysFont("arial", 30)
    again_text = small_font.render("Game will restart in 3 seconds...", True, WHITE)
    again_rect = again_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 80))
    screen.blit(again_text, again_rect)
    
    pygame.display.update()

def main_game_loop(num_players, human, ai):
    board = create_board()
    print_board(board)
    game_over = False
    winning_pieces = []
    
    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    
    screen = pygame.display.set_mode(size)
    if num_players == 2:
        pygame.display.set_caption("Connect 4 - 2 Player")
    else:
        pygame.display.set_caption(f"Connect 4 - {human} Human {ai} AI")

    
    turn = random.randint(PLAYER1, AI if num_players == 3 else PLAYER2)
    clock = pygame.time.Clock()
    draw_board(board, screen, SQUARESIZE, height, RADIUS, None, turn)
    pygame.display.update()
    
    # Game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Update board display when mouse moves (for column highlighting)
            if event.type == pygame.MOUSEMOTION:
                draw_board(board, screen, SQUARESIZE, height, RADIUS, winning_pieces , turn)
                
            # Player's turn handling (for human players)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Player 1's turn (always human)
                if turn == PLAYER1:
                    col = event.pos[0] // SQUARESIZE
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        
                        # Animate the piece dropping
                        animate_piece_drop(board, row, col, PLAYER1_PIECE, screen, SQUARESIZE, height, RADIUS)
                        
                        # Check for win
                        win, win_positions = winning_move(board, PLAYER1_PIECE)
                        if win:
                            sound1 = pygame.mixer.Sound("win.mp3")
                            sound1.play()
                            winning_pieces = win_positions
                            draw_board(board, screen, SQUARESIZE, height, RADIUS, winning_pieces, turn)
                            display_winner(screen, "Player 1 wins!", RED)
                            game_over = True
                        else:
                            turn = (turn + 1) % num_players
                            draw_board(board, screen, SQUARESIZE, height, RADIUS, None, turn)
                
                # Player 2's turn (if human)
                elif turn == PLAYER2 and human >= 2:
                    col = event.pos[0] // SQUARESIZE
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        
                        # Animate the piece dropping
                        animate_piece_drop(board, row, col, PLAYER2_PIECE, screen, SQUARESIZE, height, RADIUS)
                        
                        # Check for win
                        win, win_positions = winning_move(board, PLAYER2_PIECE)
                        if win:
                            winning_pieces = win_positions
                            sound1 = pygame.mixer.Sound("win.mp3")
                            sound1.play()
                            draw_board(board, screen, SQUARESIZE, height, RADIUS, winning_pieces, turn)
                            display_winner(screen, "Player 2 wins!", YELLOW)
                            game_over = True
                        else:
                            turn = (turn + 1) % num_players
                            draw_board(board, screen, SQUARESIZE, height, RADIUS, None, turn)
        
        # AI turns
        # Player 2's turn (if AI)
        if turn == PLAYER2 and human < 2 and not game_over:
            pygame.time.wait(500)  # Brief pause to show AI thinking
            col, minimax_score = minimax(board, DIFF_LEVEL , -math.inf, math.inf, True, PLAYER2_PIECE, PLAYER1_PIECE)

            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                
                # Animate the piece dropping
                animate_piece_drop(board, row, col, PLAYER2_PIECE, screen, SQUARESIZE, height, RADIUS)
                
                # Check for win
                win, win_positions = winning_move(board, PLAYER2_PIECE)
                if win:
                    winning_pieces = win_positions
                    draw_board(board, screen, SQUARESIZE, height, RADIUS, winning_pieces, turn)
                    display_winner(screen, "Player 2 wins!", YELLOW)
                    game_over = True
                else:
                    turn = (turn + 1) % num_players
                    draw_board(board, screen, SQUARESIZE, height, RADIUS, None, turn)
        
        # Player 3's turn (always AI in 3-player mode)
        if turn == AI and not game_over:
            pygame.time.wait(500)  # Brief pause to show AI thinking
            col, minimax_score = minimax(board, DIFF_LEVEL , -math.inf, math.inf, True, PLAYER2_PIECE, PLAYER1_PIECE)

            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                
                # Animate the piece dropping
                animate_piece_drop(board, row, col, AI_PIECE, screen, SQUARESIZE, height, RADIUS)
                
                # Check for win
                win, win_positions = winning_move(board, AI_PIECE)
                if win:
                    winning_pieces = win_positions
                    sound1 = pygame.mixer.Sound("win.mp3")
                    sound1.play()
                            
                    draw_board(board, screen, SQUARESIZE, height, RADIUS, winning_pieces, turn)
                    display_winner(screen, "Player 3 wins!", GREEN)
                    game_over = True
                else:
                    turn = (turn + 1) % num_players
                    draw_board(board, screen, SQUARESIZE, height, RADIUS, None, turn)
        
        # Check for a tie
        if is_board_full(board) and not game_over:
            sound1 = pygame.mixer.Sound("tie.mp3")
            sound1.play()
                            
            display_winner(screen, "Tie Game!", BLUE)
            game_over = True
        
        if game_over:
            pygame.time.wait(3000)
            return  # Exit the game loop
            
        # Update display and maintain framerate
        pygame.display.update()
        clock.tick(60)

# Main game entry point
pygame.init()
while True:
    # Main Menu

    result = select_diff()
    
    if isinstance(result, tuple):
        if len(result) == 2:
            human, ai = result
            num_players = human + ai
            
            # Run the game with the selected configuration
            main_game_loop(num_players, human, ai)
    elif result is None:
        # If no result or back button pressed, restart the loop
        continue