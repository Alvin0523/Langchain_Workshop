# pygame_ui.py
import pygame
import math
import time

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 420, 520
BG_COLOR = (245, 245, 250)
TEXT_COLOR = (50, 50, 60)

# ---------------- DRAW HELPERS ----------------

def draw_cat(screen, x, y, mood):
    t = time.time()
    bob = int(4 * math.sin(t * 2))
    y += bob

    body = (220, 220, 225)
    outline = (90, 90, 100)
    blush = (255, 170, 170)

    # Body
    pygame.draw.ellipse(screen, body, (x-45, y+40, 90, 55))
    pygame.draw.ellipse(screen, outline, (x-45, y+40, 90, 55), 2)

    # Head
    pygame.draw.circle(screen, body, (x, y), 50)
    pygame.draw.circle(screen, outline, (x, y), 50, 2)

    # Ears
    pygame.draw.polygon(screen, body, [(x-35,y-30),(x-10,y-60),(x-5,y-25)])
    pygame.draw.polygon(screen, body, [(x+35,y-30),(x+10,y-60),(x+5,y-25)])

    # Eyes
    blink = int(t * 3) % 6 == 0
    if mood == "sleepy" or blink:
        pygame.draw.line(screen, outline, (x-18,y-5),(x-5,y-5),3)
        pygame.draw.line(screen, outline, (x+5,y-5),(x+18,y-5),3)
    else:
        pygame.draw.circle(screen, outline, (x-12,y-5), 4)
        pygame.draw.circle(screen, outline, (x+12,y-5), 4)

    # Blush
    pygame.draw.circle(screen, blush, (x-25,y+8), 5)
    pygame.draw.circle(screen, blush, (x+25,y+8), 5)

    # Mouth
    if mood == "happy":
        pygame.draw.arc(screen, outline, (x-10,y+5,20,15), 3.14, 0, 2)
    elif mood == "excited":
        pygame.draw.circle(screen, (255,120,120), (x,y+15), 6)
    else:
        pygame.draw.line(screen, outline, (x-6,y+15),(x+6,y+15),2)

    # Tail
    wag = int(8 * math.sin(t * 4))
    pygame.draw.line(screen, outline, (x+40,y+60),(x+70,y+50+wag),4)


def draw_speech_bubble(screen, text, font, x, y):
    padding = 10
    max_width = 260

    words = text.split(" ")
    lines, line = [], ""
    for w in words:
        test = line + w + " "
        if font.size(test)[0] <= max_width:
            line = test
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)

    bubble_w = max(font.size(l)[0] for l in lines) + padding*2
    bubble_h = len(lines)*font.get_height() + padding*2

    rect = pygame.Rect(x - bubble_w//2, y - bubble_h - 20, bubble_w, bubble_h)

    pygame.draw.rect(screen, (255,255,255), rect, border_radius=14)
    pygame.draw.rect(screen, (180,180,180), rect, 2, border_radius=14)

    pygame.draw.polygon(
        screen, (255,255,255),
        [(x-10,y-20),(x+10,y-20),(x,y-5)]
    )

    ty = rect.y + padding
    for l in lines:
        surf = font.render(l, True, TEXT_COLOR)
        screen.blit(surf, (rect.centerx - surf.get_width()//2, ty))
        ty += font.get_height()


# ---------------- MAIN LOOP ----------------

def run_gui(pet_state, get_response, is_thinking_flag):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mochi")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 24)
    input_text = ""

    while True:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text and not is_thinking_flag():
                        get_response(input_text)
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Cat
        draw_cat(screen, WIDTH//2, 200, pet_state["mood"])

        # Bubble
        text = "Thinking..." if is_thinking_flag() else pet_state["last_response"]
        draw_speech_bubble(screen, text, font, WIDTH//2, 150)

        # Input bar
        bar = pygame.Rect(40, HEIGHT-55, WIDTH-80, 36)
        pygame.draw.rect(screen, (255,255,255), bar, border_radius=18)
        pygame.draw.rect(screen, (180,180,180), bar, 2, border_radius=18)

        surf = font.render(input_text, True, TEXT_COLOR)
        screen.blit(surf, (bar.x + 14, bar.y + 9))

        pygame.display.flip()
        clock.tick(30)
