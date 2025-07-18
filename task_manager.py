#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task Manager - Система управления заданиями для стартапера

Этот модуль управляет всеми заданиями в игре:
- Загрузка заданий из JSON
- Активация/деактивация заданий
- Отрисовка заданий на карте
- Обработка взаимодействий
- UI панель заданий
"""

import pygame
import json
import os
from constants import WHITE, GREEN, GOLD, GRAY, LIGHT_GRAY

class TaskStatus:
    """Константы статусов заданий"""
    INACTIVE = "inactive"     # Неактивная - еще не появлялась на карте
    ACTIVE = "active"         # Активная - на карте, не выполнена
    COMPLETED = "completed"   # Завершенная - выполнена

class Task:
    """Класс одного задания"""
    
    def __init__(self, task_data):
        """
        Инициализация задания из данных JSON
        
        Args:
            task_data (dict): Данные задания из JSON
        """
        self.id = task_data["id"]
        self.title = task_data["title"]
        self.description = task_data["description"]
        self.sprite_before_path = task_data["sprite_before"]
        self.sprite_after_path = task_data["sprite_after"]
        self.world_x = task_data["world_x"]
        self.world_y = task_data["world_y"]
        self.width = task_data["width"]
        self.height = task_data["height"]
        self.reward_users = task_data["reward_users"]
        self.reward_money = task_data["reward_money"]
        self.status = task_data["status"]
        
        # Загрузка спрайтов
        self.sprite_before = None
        self.sprite_after = None
        self.current_sprite = None
        self.load_sprites()
        
        # Прямоугольник для коллизий
        self.rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)
    
    def load_sprites(self):
        """Загрузка спрайтов для задания"""
        try:
            # Загружаем спрайт "до выполнения"
            if os.path.exists(self.sprite_before_path):
                self.sprite_before = pygame.image.load(self.sprite_before_path)
                self.sprite_before = pygame.transform.scale(self.sprite_before, (self.width, self.height))
            else:
                # Создаем заглушку если файл не найден
                self.sprite_before = pygame.Surface((self.width, self.height))
                self.sprite_before.fill((100, 100, 150))  # Серо-синий
                
            # Загружаем спрайт "после выполнения"
            if os.path.exists(self.sprite_after_path):
                self.sprite_after = pygame.image.load(self.sprite_after_path)
                self.sprite_after = pygame.transform.scale(self.sprite_after, (self.width, self.height))
            else:
                # Создаем заглушку если файл не найден
                self.sprite_after = pygame.Surface((self.width, self.height))
                self.sprite_after.fill((100, 150, 100))  # Серо-зеленый
                
            # Устанавливаем текущий спрайт в зависимости от статуса
            self.update_current_sprite()
            
        except pygame.error as e:
            print(f"Ошибка загрузки спрайтов для задания {self.id}: {e}")
            # Создаем заглушки
            self.sprite_before = pygame.Surface((self.width, self.height))
            self.sprite_before.fill((100, 100, 150))
            self.sprite_after = pygame.Surface((self.width, self.height))
            self.sprite_after.fill((100, 150, 100))
            self.update_current_sprite()
    
    def update_current_sprite(self):
        """Обновление текущего спрайта в зависимости от статуса"""
        if self.status == TaskStatus.COMPLETED:
            self.current_sprite = self.sprite_after
        else:
            self.current_sprite = self.sprite_before
    
    def set_status(self, new_status):
        """
        Изменение статуса задания
        
        Args:
            new_status (str): Новый статус (из TaskStatus)
        """
        if new_status in [TaskStatus.INACTIVE, TaskStatus.ACTIVE, TaskStatus.COMPLETED]:
            self.status = new_status
            self.update_current_sprite()
            print(f"Задание '{self.title}' изменило статус на: {new_status}")
        else:
            print(f"Неизвестный статус: {new_status}")
    
    def draw(self, screen, camera):
        """
        Отрисовка задания на карте (только если активно или завершено)
        
        Args:
            screen: Поверхность pygame для отрисовки
            camera: Объект камеры для расчета позиций
        """
        if self.status in [TaskStatus.ACTIVE, TaskStatus.COMPLETED]:
            # Получаем экранные координаты через камеру
            screen_x, screen_y = camera.apply(self.world_x, self.world_y)
            
            # Отрисовываем спрайт
            if self.current_sprite:
                screen.blit(self.current_sprite, (screen_x, screen_y))
            
            # Добавляем рамку для активных заданий
            if self.status == TaskStatus.ACTIVE:
                pygame.draw.rect(screen, GOLD, (screen_x - 2, screen_y - 2, 
                               self.width + 4, self.height + 4), 2)
            elif self.status == TaskStatus.COMPLETED:
                pygame.draw.rect(screen, GREEN, (screen_x - 2, screen_y - 2, 
                               self.width + 4, self.height + 4), 2)
    
    def check_collision(self, player_x, player_y, player_width, player_height):
        """
        Проверка коллизии с игроком
        
        Args:
            player_x, player_y: Позиция игрока в мире
            player_width, player_height: Размеры игрока
            
        Returns:
            bool: True если есть коллизия
        """
        if self.status != TaskStatus.ACTIVE:
            return False
            
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        return self.rect.colliderect(player_rect)

class TaskManager:
    """Менеджер системы заданий"""
    
    def __init__(self, tasks_file="tasks.json"):
        """
        Инициализация менеджера заданий
        
        Args:
            tasks_file (str): Путь к JSON файлу с заданиями
        """
        self.tasks_file = tasks_file
        self.tasks = {}  # Словарь заданий {id: Task}
        self.active_tasks = []  # Список ID активных заданий
        self.completed_tasks = []  # Список ID завершенных заданий
        
        self.load_tasks()
    
    def load_tasks(self):
        """Загрузка заданий из JSON файла"""
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            for task_data in data["tasks"]:
                task = Task(task_data)
                self.tasks[task.id] = task
                
                # Добавляем в соответствующие списки по статусу
                if task.status == TaskStatus.ACTIVE:
                    self.active_tasks.append(task.id)
                elif task.status == TaskStatus.COMPLETED:
                    self.completed_tasks.append(task.id)
            
            print(f"Загружено {len(self.tasks)} заданий из {self.tasks_file}")
            
        except FileNotFoundError:
            print(f"Файл заданий {self.tasks_file} не найден!")
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            print(f"Ошибка загрузки заданий: {e}")
    
    def save_tasks(self):
        """Сохранение текущего состояния заданий в JSON"""
        try:
            tasks_data = {
                "tasks": []
            }
            
            for task in self.tasks.values():
                task_data = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "sprite_before": task.sprite_before_path,
                    "sprite_after": task.sprite_after_path,
                    "world_x": task.world_x,
                    "world_y": task.world_y,
                    "width": task.width,
                    "height": task.height,
                    "reward_users": task.reward_users,
                    "reward_money": task.reward_money,
                    "status": task.status
                }
                tasks_data["tasks"].append(task_data)
            
            with open(self.tasks_file, 'w', encoding='utf-8') as file:
                json.dump(tasks_data, file, ensure_ascii=False, indent=2)
            
            print(f"Состояние заданий сохранено в {self.tasks_file}")
            
        except Exception as e:
            print(f"Ошибка сохранения заданий: {e}")
    
    def activate_task(self, task_id):
        """
        Активация задания по ID
        
        Args:
            task_id (str): ID задания для активации
            
        Returns:
            bool: True если задание успешно активировано
        """
        if task_id not in self.tasks:
            print(f"Задание с ID '{task_id}' не найдено!")
            return False
        
        task = self.tasks[task_id]
        
        if task.status == TaskStatus.INACTIVE:
            task.set_status(TaskStatus.ACTIVE)
            self.active_tasks.append(task_id)
            print(f"Задание '{task.title}' активировано!")
            return True
        elif task.status == TaskStatus.ACTIVE:
            print(f"Задание '{task.title}' уже активно!")
            return False
        elif task.status == TaskStatus.COMPLETED:
            print(f"Задание '{task.title}' уже завершено!")
            return False
    
    def complete_task(self, task_id):
        """
        Завершение задания по ID
        
        Args:
            task_id (str): ID задания для завершения
            
        Returns:
            dict: Награды за задание {"users": int, "money": int} или None
        """
        if task_id not in self.tasks:
            print(f"Задание с ID '{task_id}' не найдено!")
            return None
        
        task = self.tasks[task_id]
        
        if task.status == TaskStatus.ACTIVE:
            task.set_status(TaskStatus.COMPLETED)
            
            # Убираем из активных, добавляем в завершенные
            if task_id in self.active_tasks:
                self.active_tasks.remove(task_id)
            self.completed_tasks.append(task_id)
            
            print(f"Задание '{task.title}' завершено!")
            print(f"Награды: Пользователи: {task.reward_users}, Деньги: {task.reward_money}")
            
            return {
                "users": task.reward_users,
                "money": task.reward_money
            }
        else:
            print(f"Нельзя завершить задание '{task.title}' - оно не активно!")
            return None
    
    def get_task_status(self, task_id):
        """
        Получение статуса задания по ID
        
        Args:
            task_id (str): ID задания
            
        Returns:
            str: Статус задания или None если не найдено
        """
        if task_id in self.tasks:
            return self.tasks[task_id].status
        return None
    
    def get_active_tasks(self):
        """
        Получение списка активных заданий
        
        Returns:
            list: Список объектов Task с активным статусом
        """
        return [self.tasks[task_id] for task_id in self.active_tasks if task_id in self.tasks]
    
    def get_completed_tasks(self):
        """
        Получение списка завершенных заданий
        
        Returns:
            list: Список объектов Task с завершенным статусом
        """
        return [self.tasks[task_id] for task_id in self.completed_tasks if task_id in self.tasks]
    
    def draw_tasks(self, screen, camera):
        """
        Отрисовка всех активных и завершенных заданий на карте
        
        Args:
            screen: Поверхность pygame для отрисовки
            camera: Объект камеры для расчета позиций
        """
        for task in self.tasks.values():
            task.draw(screen, camera)
    
    def draw_tasks_ui(self, screen):
        """
        Отрисовка UI панели с активными заданиями
        
        Args:
            screen: Поверхность pygame для отрисовки
        """
        if not self.active_tasks:
            return
        
        # Настройки UI
        panel_x = 20
        panel_y = 200
        panel_width = 400
        task_height = 60
        panel_height = len(self.active_tasks) * task_height + 40
        
        # Фон панели
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 180))  # Полупрозрачный черный
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Рамка панели
        pygame.draw.rect(screen, WHITE, (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Заголовок
        font_title = pygame.font.Font(None, 32)
        title_text = font_title.render("Активные задания:", True, WHITE)
        screen.blit(title_text, (panel_x + 10, panel_y + 10))
        
        # Список заданий
        font_task = pygame.font.Font(None, 24)
        font_desc = pygame.font.Font(None, 20)
        
        for i, task_id in enumerate(self.active_tasks):
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task_y = panel_y + 50 + i * task_height
                
                # Название задания
                title_surface = font_task.render(task.title, True, GOLD)
                screen.blit(title_surface, (panel_x + 10, task_y))
                
                # Описание задания
                desc_surface = font_desc.render(task.description, True, LIGHT_GRAY)
                screen.blit(desc_surface, (panel_x + 10, task_y + 25))
                
                # Награды
                reward_text = f"Награда: +{task.reward_users} польз., ${task.reward_money}"
                reward_surface = font_desc.render(reward_text, True, GREEN if task.reward_money >= 0 else (255, 100, 100))
                screen.blit(reward_surface, (panel_x + 10, task_y + 45))
    
    def check_task_interactions(self, player_x, player_y, player_width, player_height):
        """
        Проверка взаимодействий игрока с активными заданиями
        
        Args:
            player_x, player_y: Позиция игрока в мире
            player_width, player_height: Размеры игрока
            
        Returns:
            str: ID задания с которым произошло взаимодействие или None
        """
        for task_id in self.active_tasks:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.check_collision(player_x, player_y, player_width, player_height):
                    return task_id
        return None
    
    def reset_all_tasks(self):
        """Сброс всех заданий в неактивное состояние"""
        for task in self.tasks.values():
            task.set_status(TaskStatus.INACTIVE)
        
        self.active_tasks.clear()
        self.completed_tasks.clear()
        print("Все задания сброшены в неактивное состояние")
    
    def get_task_info(self, task_id):
        """
        Получение полной информации о задании
        
        Args:
            task_id (str): ID задания
            
        Returns:
            dict: Информация о задании или None
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "rewards": {
                    "users": task.reward_users,
                    "money": task.reward_money
                },
                "position": {
                    "x": task.world_x,
                    "y": task.world_y
                }
            }
        return None 