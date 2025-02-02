
from pygame import *
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# основыне переменные
BLUE = (100, 150, 255)
RED = (255, 0, 0)

display.set_caption("Моя игра")
window = display.set_mode((500, 500))
clock = time.Clock()
window.fill(BLUE)

class Area():
    def __init__(self, x, y, width, height, image):
        self.rect = Rect(x, y, width, height) #прямоугольник
        self.image = image

    def fill(self):
        window.blit(self.image, self.rect.topleft)
    
    def fill_color(self, color):
        draw.rect(window, color, self.rect)

class Player(Area):
    pass

class Enemy(Area):
    def __init__(self, x, y, width, height, image=None):
        super().__init__(x, y, width, height, image)
        self.direction = 2  # начальное направление движения врага

    def move(self):
        self.rect.y += self.direction
        if self.rect.bottom >= 500 or self.rect.top <= 0:
            self.direction *= -1

class Level():
    def __init__(self, player_start, barriers, enemy_positions, finish_position):
        self.player_start = player_start
        self.barriers = barriers
        self.enemy_positions = enemy_positions
        self.finish_position = finish_position


# загружаем изображения
image_hero = transform.scale(image.load(os.path.join(base_path, "images", "hero.png")), (40, 40))
image_barrier_h = transform.scale(image.load(os.path.join(base_path, "images", "platform_h.png")), (100, 20))
image_barrier_v = transform.scale(image.load(os.path.join(base_path, "images", "platform_v.png")), (20, 100))
image_enemy = transform.scale(image.load(os.path.join(base_path, "images", "enemy.png")), (40, 40))
image_ufo = transform.scale(image.load(os.path.join(base_path, "images", "ufo_3.png")), (96, 96))


levels = [
    Level(player_start=(100, 100),
          barriers=[
              Area(50, 50, 100, 20, image_barrier_h),
              Area(50, 100, 20, 100, image_barrier_v),
              Area(100, 150, 100, 20, image_barrier_h),
              Area(350, 50, 20, 100, image_barrier_v),
              Area(200, 250, 100, 20, image_barrier_h),
              Area(50, 400, 100, 20, image_barrier_h)
          ],
          enemy_positions=[(150, 200), (300, 300)],
          finish_position=(380, 420)),
    
    Level(player_start=(0, 0),
          barriers=[
              Area(50, 50, 100, 20, image_barrier_h),
              Area(50, 100, 20, 100, image_barrier_v),
              Area(150, 250, 20, 100, image_barrier_v),
              Area(100, 150, 100, 20, image_barrier_h),
              Area(250, 250, 100, 20, image_barrier_h),
              Area(350, 350, 100, 20, image_barrier_h),
              Area(400, 50, 20, 100, image_barrier_v),
              Area(50, 400, 100, 20, image_barrier_h)
          ],
          enemy_positions=[(100, 250), (200, 150), (300, 350)],
          finish_position=(380, 420))
]

current_level_index = 0

def load_level(level_index):
    global player, barriers, enemies, finish
    level = levels[level_index]
    player = Player(level.player_start[0], level.player_start[1], 40, 40, image_hero)
    barriers = level.barriers
    enemies = [Enemy(x, y, 40, 40, image_enemy) for x, y in level.enemy_positions]
    finish = Area(level.finish_position[0], level.finish_position[1], 96, 96, image_ufo)

load_level(current_level_index)

move_left = False
move_right = False
move_up = False
move_down = False

run = True
while run:
    window.fill(BLUE)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_LEFT:
                move_left = True
            if e.key == K_RIGHT:
                move_right = True
            if e.key == K_UP:
                move_up = True
            if e.key == K_DOWN:
                move_down = True
        if e.type == KEYUP:
            if e.key == K_LEFT:
                move_left = False
            if e.key == K_RIGHT:
                move_right = False
            if e.key == K_UP:
                move_up = False
            if e.key == K_DOWN:
                move_down = False
    
    # Сохраняем текущее положение игрока
    old_rect = player.rect.copy()

    if move_left:
        player.rect.x -= 3
    if move_right:
        player.rect.x += 3
    if move_up:
        player.rect.y -= 3
    if move_down:
        player.rect.y += 3


    # Ограничение движения по границам экрана
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.right > 500:  # Ширина окна
        player.rect.right = 500
    if player.rect.bottom > 500:  # Высота окна
        player.rect.bottom = 500
    
    for barrier in barriers:
        if player.rect.colliderect(barrier.rect):
            player.rect = old_rect


    for barrier in barriers:
        for enemy in enemies:
            if enemy.rect.colliderect(barrier.rect):
                enemy.direction *= -1

    # отрисовка прямоугольгика
    player.fill()
    finish.fill()
    for enemy in enemies:
        enemy.move()
        enemy.fill()
    for barrier in barriers:
        barrier.fill()



    if player.rect.colliderect(finish.rect):
        current_level_index += 1
        if current_level_index < len(levels):
            load_level(current_level_index)
        else:
            print("Вы победили!")
            run = False
    
    '''
    player.fill_color(RED)  # Игрок красный
    finish.fill_color((0, 255, 0))  # Финиш зеленый
    for barrier in barriers:
        barrier.fill_color((255, 255, 0))  # Барьеры желтые
    for enemy in enemies:
        enemy.fill_color((255, 0, 255))  
    '''
    display.update()
    clock.tick(40)
