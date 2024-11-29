import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_BACKSPACE
from gtts import gTTS
from deep_translator import GoogleTranslator
import os

pygame.init()
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 550  
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Text to Speech with Translation")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

font = pygame.font.Font(None, 30)

text_input = ""
language_input = "pt" 
message = ""
audio_path = "output.mp3"
translator = GoogleTranslator()

face_center = (SCREEN_WIDTH // 2, 100) 
face_radius = 60
eye_offset_x, eye_offset_y = 20, 20
eye_radius = 10
pupil_radius = 5

def draw_face():
    # Cabeça (sombra para efeito 3D)
    pygame.draw.circle(screen, (180, 180, 180), face_center, face_radius, 0)  
    pygame.draw.circle(screen, BLACK, face_center, face_radius, 2) 

    # Olhos
    for offset_x in [-eye_offset_x, eye_offset_x]:
        eye_center = (face_center[0] + offset_x, face_center[1] - eye_offset_y)
        pygame.draw.circle(screen, (200, 200, 200), eye_center, eye_radius, 0)  
        pygame.draw.circle(screen, BLACK, eye_center, eye_radius, 2)  

        # Pupilas
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = max(-4, min(4, mouse_x - eye_center[0]))
        dy = max(-4, min(4, mouse_y - eye_center[1]))
        pygame.draw.circle(screen, BLACK, (eye_center[0] + dx, eye_center[1] + dy), pupil_radius)

    # Boca 
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.draw.ellipse(screen, RED, (face_center[0] - 20, face_center[1] + 20, 40, 20))
    else:
        pygame.draw.line(screen, BLACK, (face_center[0] - 20, face_center[1] + 30),
                         (face_center[0] + 20, face_center[1] + 30), 2)

def delete_audio_file():
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    except Exception as e:
        print(f"Erro ao deletar o arquivo: {e}")

def stop_audio():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    except Exception as e:
        print(f"Erro ao parar o áudio: {e}")

def translate_text(text, target_lang):
    try:
        translator.target = target_lang
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Erro ao traduzir o texto: {e}")
        return text 

def generate_and_play_audio(text, lang):
    global message
    try:
        stop_audio()
        delete_audio_file()

        translated_text = translate_text(text, lang)
        tts = gTTS(text=translated_text, lang=lang)
        tts.save(audio_path)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        message = f"Texto traduzido: {translated_text}"
    except Exception as e:
        message = f"Erro: {e}"

# Função para centralizar retângulos
def draw_centered_rect(color, width, height, y_position):
    x_pos = (SCREEN_WIDTH - width) // 2
    pygame.draw.rect(screen, color, (x_pos, y_position, width, height))

running = True
while running:
    screen.fill(WHITE)

    # Eventos do Pygame
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                if text_input.strip():
                    generate_and_play_audio(text_input, language_input)
                else:
                    message = "Por favor, insira um texto!"
            elif event.key == K_BACKSPACE:
                text_input = text_input[:-1]
            else:
                text_input += event.unicode

    # interface
    draw_face()  
    draw_centered_rect(GRAY, 460, 40, face_center[1] + face_radius + 20)  
    draw_centered_rect(BLUE, 460, 40, face_center[1] + face_radius + 70) 
    draw_centered_rect(BLUE, 460, 40, face_center[1] + face_radius + 120) 
    draw_centered_rect(BLUE, 460, 40, face_center[1] + face_radius + 170)  

    # textos
    text_surface = font.render(text_input, True, BLACK)
    lang_surface = font.render(f"Idioma atual: {language_input.upper()}", True, BLACK)
    button_en_surface = font.render("Mudar para Inglês", True, WHITE)
    button_fr_surface = font.render("Mudar para Francês", True, WHITE)
    button_pt_surface = font.render("Mudar para Português", True, WHITE)
    #button_search = font.render("Pesquisar", True, WHITE)
    ##button_ia = font.render("Consultar IA", True, WHITE)
    message_surface = font.render(message, True, BLACK)

    # Adiciona os textos à tela
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - button_en_surface.get_width() - 40, face_center[1] + face_radius + 30))  # Caixa de texto
    screen.blit(button_en_surface, (SCREEN_WIDTH // 2 - button_en_surface.get_width() // 2, face_center[1] + face_radius + 75))
    screen.blit(button_fr_surface, (SCREEN_WIDTH // 2 - button_fr_surface.get_width() // 2, face_center[1] + face_radius + 125))
    screen.blit(button_pt_surface, (SCREEN_WIDTH // 2 - button_pt_surface.get_width() // 2, face_center[1] + face_radius + 175))
    #screen.blit(button_search, (SCREEN_WIDTH // 2 - button_pt_surface.get_width() // 2, face_center[1] + face_radius + 225))
    #screen.blit(button_ia, (SCREEN_WIDTH // 2 - button_pt_surface.get_width() // 2, face_center[1] + face_radius + 275))
    screen.blit(lang_surface, (SCREEN_WIDTH // 2 - button_pt_surface.get_width() - 10, face_center[1] + face_radius + 230))
    screen.blit(message_surface, (SCREEN_WIDTH // 2 - button_pt_surface.get_width() - 10, face_center[1] + face_radius + 270))

    # cliques no mouse
    if pygame.mouse.get_pressed()[0]:  
        mouse_pos = pygame.mouse.get_pos()
        if SCREEN_WIDTH // 2 - 230 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 230 and face_center[1] + face_radius + 70 <= mouse_pos[1] <= face_center[1] + face_radius + 110:
            stop_audio() 
            language_input = "en"
            message = "Idioma alterado para Inglês"
        elif SCREEN_WIDTH // 2 - 230 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 230 and face_center[1] + face_radius + 120 <= mouse_pos[1] <= face_center[1] + face_radius + 160:
            stop_audio()  
            language_input = "fr"
            message = "Idioma alterado para Francês"
        elif SCREEN_WIDTH // 2 - 230 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 230 and face_center[1] + face_radius + 170 <= mouse_pos[1] <= face_center[1] + face_radius + 210:
            stop_audio() 
            language_input = "pt"
            message = "Idioma alterado para Português"

    pygame.display.flip()

stop_audio() 
delete_audio_file()  
pygame.quit()
sys.exit()
