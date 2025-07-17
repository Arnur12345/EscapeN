import pygame
import sys
import time

# Инициализация Pygame
pygame.init()

# Устанавливаем размер экрана
screen = pygame.display.set_mode((800, 600))

# Устанавливаем шрифт для текста
font = pygame.font.Font(None, 36)

# Функция для отображения текста с эффектом печатания
def type_writer(text, x, y, speed=0.1):
    display_text = ""
    for i in range(len(text)):
        display_text += text[i]
        screen.fill((0, 0, 0))  # Закрашиваем экран
        screen.blit(background, (0, 0))  # Отображаем фон
        draw_text(display_text, x, y)
        pygame.display.flip()  # Обновляем экран
        time.sleep(speed)

# Функция для отображения текста
def draw_text(text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

# Загружаем фон
background = pygame.image.load("button.png")

# Основной цикл
running = True
while running:
    screen.fill((0, 0, 0))  # Закрашиваем экран
    screen.blit(background, (0, 0))  # Отображаем фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Печатаем текст с эффектом
    type_writer("Hello, this is a typing effect!", 100, 100)

    pygame.display.flip()  # Обновляем экран

pygame.quit()
sys.exit()
