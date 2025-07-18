import pygame
import os
from constants import BLACK

class Asselya:
    """Класс для NPC Асели, которая проверяет социальные сети"""
    
    def __init__(self, x, y, sprite_path):
        """
        Инициализация Асели
        
        Args:
            x, y: Начальная позиция
            sprite_path: Путь к папке со спрайтами
        """
        self.world_x = x
        self.world_y = y
        self.base_x = x  # Базовая позиция для возврата
        self.base_y = y
        self.width = 70
        self.height = 100
        
        # Состояния
        self.is_active = False  # Активна ли Аселя
        self.is_chasing = False  # Преследует ли игрока
        self.speed = 5  # Базовая скорость движения
        self.facing_left = False  # Направление спрайта
        
        # Загрузка спрайтов
        self.sprites = {
            "standing": [],
            "running": []
        }
        
        try:
            # Получаем абсолютный путь к текущей директории
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Current directory: {current_dir}")
            
            # Загрузка спрайтов стояния
            standing_path = os.path.join(current_dir, sprite_path, "standing")
            print(f"Standing path: {standing_path}")
            if os.path.exists(standing_path):
                files = sorted(os.listdir(standing_path))
                print(f"Found standing files: {files}")
                for file in files:
                    if file.endswith(".png"):
                        full_path = os.path.join(standing_path, file)
                        print(f"Loading standing sprite: {full_path}")
                        sprite = pygame.image.load(full_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (self.width, self.height))
                        self.sprites["standing"].append(sprite)
            else:
                print(f"Standing path does not exist: {standing_path}")
            
            # Загрузка спрайтов бега
            running_path = os.path.join(current_dir, sprite_path, "running")
            print(f"Running path: {running_path}")
            if os.path.exists(running_path):
                files = sorted(os.listdir(running_path))
                print(f"Found running files: {files}")
                for file in files:
                    if file.endswith(".png"):
                        full_path = os.path.join(running_path, file)
                        print(f"Loading running sprite: {full_path}")
                        sprite = pygame.image.load(full_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (self.width, self.height))
                        self.sprites["running"].append(sprite)
            else:
                print(f"Running path does not exist: {running_path}")
            
            print(f"Loaded {len(self.sprites['standing'])} standing sprites and {len(self.sprites['running'])} running sprites")
            
            if not self.sprites["standing"] or not self.sprites["running"]:
                raise Exception("No sprites loaded!")
            
        except Exception as e:
            print(f"Ошибка загрузки спрайтов Асели: {e}")
            # Создаем заглушку если спрайты не загрузились
            surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(surface, (150, 0, 150), (0, 0, self.width, self.height))
            self.sprites["standing"] = [surface]
            self.sprites["running"] = [surface]
        
        # Анимация
        self.current_frame = 0
        self.animation_timer = 0
        self.ANIMATION_DELAY = 100  # Миллисекунды между кадрами
        self.STANDING_DELAY = 150   # Более медленная анимация для стояния
        
        # Прямоугольник для коллизий
        self.rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)
    
    def start_chase(self):
        """Начать преследование игрока"""
        print("Аселя начала преследование!")
        self.is_chasing = True
        self.current_frame = 0  # Сбрасываем анимацию
    
    def stop_chase(self):
        """Остановить преследование игрока"""
        print("Аселя вернулась на базу")
        self.is_chasing = False
        self.world_x = self.base_x
        self.world_y = self.base_y
        self.current_frame = 0  # Сбрасываем анимацию
    
    def update_animation(self, delta_time):
        """Обновление анимации"""
        self.animation_timer += delta_time
        
        # Выбираем задержку в зависимости от состояния
        delay = self.ANIMATION_DELAY if self.is_chasing else self.STANDING_DELAY
        
        if self.animation_timer >= delay:
            self.animation_timer = 0
            sprites = self.sprites["running" if self.is_chasing else "standing"]
            if sprites:  # Проверяем, что есть спрайты
                self.current_frame = (self.current_frame + 1) % len(sprites)
    
    def draw(self, screen, camera):
        """
        Отрисовка Асели
        
        Args:
            screen: Поверхность для отрисовки
            camera: Объект камеры
        """
        if not self.is_active:
            return
            
        # Получаем текущий спрайт
        sprites = self.sprites["running" if self.is_chasing else "standing"]
        if not sprites:
            return
            
        current_sprite = sprites[self.current_frame]
        
        # Получаем экранные координаты
        screen_x, screen_y = camera.apply(self.world_x, self.world_y)
        
        # Отражаем спрайт по горизонтали если нужно
        if self.facing_left:
            current_sprite = pygame.transform.flip(current_sprite, True, False)
        
        # Отрисовываем спрайт
        screen.blit(current_sprite, (screen_x, screen_y))