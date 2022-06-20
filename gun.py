import math
import random
from random import choice, randint
import pygame
from Colors import *

WIDTH = 1000
HEIGHT = 600
GRAVITY = 0.9  # Сила тяжести
friction = 0.99
FPS = 30
pygame.font.init()
font = pygame.font.Font(None, 20)

textpos_kills_count = (10, 10)
textpos_shoots_count = (400, 300)
textpos_current_bullet_type = (10, 20)
textpos_control = (100, 10)


class GameObject:
    pass


class Bullet(GameObject):
    def __init__(self, x, y):
        """ Конструктор класса bullet
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)

    def move(self):
        """Переместить снаряд по прошествии единицы времени.

        Метод описывает перемещение снаряда за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на снаряд,
        и стен по краям окна.
        """
        def y_movement():
            """ Перемещение по Y """
            if self.vy != 0:
                self.vy = self.vy - GRAVITY
                self.y -= self.vy
                if self.y < 0:
                    self.vy = 0
                    self.vx = 0
                if self.y > HEIGHT - 100:  # Отталкивание от пола полотна высотой HEIGHT (down)
                    self.y = HEIGHT - 100 - 1
                    if abs(self.vy) < 2:
                        self.vy = 0
                    self.vy = -self.vy
                    self.vy *= 0.8  # Замедление после удара о землю

        def x_movement():
            """ Перемещение по X """
            if self.vx != 0:
                self.vx = self.vx * friction
                #Функционал для ооталкивания от стенок.
                """if WIDTH - self.r <= self.x:  # Отталкивание от стенок полотна шириной WIDTH (right)d
                    self.x = WIDTH - self.r - 1
                    self.vx = -self.vx
                    self.vx *= 0.6  # Замедление после удара о стену
                if self.x <= self.r:  # Отталкивание от стенок полотна шириной WIDTH (left)
                    self.x = self.r + 1
                    self.vx = -self.vx
                    self.vx *= 0.6  # Замедление после удара о стену"""
                if abs(self.vx) < 1 or self.x > WIDTH or self.x < 0:
                    self.vx = 0
                    self.vy = 0
                self.x += self.vx

        y_movement()
        x_movement()

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if abs(self.x - obj.x) <= self.r + obj.r and abs(self.y - obj.y) <= self.r + obj.r:
            return True
        else:
            return False

    def check_delete(self):
        """ Функция проверяет остановился ли снаряд и можно ли его удалять """
        if self.vx == 0 and self.vy == 0:
            return True
        return False


class AntiIronBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = GREY

    def draw(self):
        pygame.draw.polygon(self.screen, self.color,
                            ((self.x - self.r, self.y - self.r),
                             (self.x + self.r, self.y - self.r),
                             (self.x + self.r, self.y + self.r),
                             (self.x - self.r, self.y + self.r)))


class AntiAngryBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = RED

    def draw(self):
        pygame.draw.polygon(self.screen, self.color,
                            ((self.x, self.y - self.r),
                             (self.x + self.r, self.y + self.r),
                             (self.x - self.r, self.y + self.r)))


class Gun(GameObject):
    def __init__(self):
        self.x = 20
        self.y = 490
        self.screen = screen
        self.f2_power = 30  # начальная сила выстрела
        self.f2_on = 0  # 0 - выстрела еще не было, 1 - выстрел произошел.
        self.an = 1
        self.color = GREY
        self.kills_count = 0
        self.shoots_count = 0
        self.current_bullet_type = 'Bullet'
        self.gun_move_left = False
        self.gun_move_right = False
        self.cursor_on_the_left = False

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел снарядом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости снаряда vx и vy зависят от положения мыши.
        """
        global bullets
        new_bullet = 0
        if self.current_bullet_type == 'Bullet':
            new_bullet = Bullet(self.x, self.y)
        if self.current_bullet_type == 'Anti Angry Bullet':
            new_bullet = AntiAngryBullet(self.x, self.y)
        if self.current_bullet_type == 'Anti Iron Bullet':
            new_bullet = AntiIronBullet(self.x, self.y)
        self.an = math.atan2((event.pos[1]-new_bullet.y), (event.pos[0]-new_bullet.x))
        new_bullet.vx = self.f2_power * math.cos(self.an)
        new_bullet.vy = - self.f2_power * math.sin(self.an)
        bullets.append(new_bullet)
        self.f2_on = 0
        self.f2_power = 30
        self.shoots_count += 1

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""

        if event and event.pos[0] != self.x:
            self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))

        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
        if event.pos[0] < self.x:
            self.cursor_on_the_left = True
        else:
            self.cursor_on_the_left = False

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        if not self.cursor_on_the_left:
            pygame.draw.line(self.screen, self.color, (self.x, self.y),
                            ((self.x + self.f2_power * math.cos(self.an)),
                            (self.y + self.f2_power * math.sin(self.an))), width=10)
        else:
            pygame.draw.line(self.screen, self.color, (self.x, self.y),
                            ((self.x - self.f2_power * math.cos(self.an)),
                            (self.y - self.f2_power * math.sin(self.an))), width=10)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 8)

    def targets_destroed(self):
        self.kills_count += 1

    def switch_bullet_type(self, key):
        if key == 'z':
            self.current_bullet_type = 'Bullet'
        elif key == 'x':
            self.current_bullet_type = 'Anti Angry Bullet'
        elif key == 'c':
            self.current_bullet_type = 'Anti Iron Bullet'

    def move(self):
        if self.gun_move_left:
            self.x -= 12
        elif self.gun_move_right:
            self.x += 12


class Target(GameObject):
    def __init__(self):
        self.screen = screen
        self.x = randint(600, 780)
        self.y = randint(int(HEIGHT * 0.1),int(HEIGHT * 0.6))
        self.r = randint(8, 50)
        self.color = choice(GAME_COLORS)
        self.vx = randint(0, 5)
        self.vy = randint(0, 5)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        def y_movement():
            """ Перемещение по Y """
            self.y -= self.vy
            if self.y + self.r > HEIGHT * 0.5:  # Отталкивание от пола полотна высотой HEIGHT (down)
                self.y = HEIGHT * 0.5 - self.r - 1
                self.vy = -self.vy
            if self.y - self.r <= 5:  # Отталкивание от верха полотна высотой HEIGHT (down)
                self.y = self.r + 6
                self.vy = -self.vy

        def x_movement():
            """ Перемещение по X """
            if WIDTH - self.r <= self.x:  # Отталкивание от стенок полотна шириной WIDTH (right)
                self.x = WIDTH - self.r - 1
                self.vx = -self.vx
            if self.x <= self.r:  # Отталкивание от стенок полотна шириной WIDTH (left)
                self.x = self.r + 1
                self.vx = -self.vx
            self.x += self.vx
        y_movement()
        x_movement()

    def drop_bomb(self):
        global bombs
        new_bomb = Bomb(self.x, self.y, self.vx)
        bombs.append(new_bomb)


class AngryTarget(Target):
    def __init__(self):
        super().__init__()
        self.vx += 10
        self.color = RED

    def draw(self):
        pygame.draw.polygon(self.screen, self.color,
                            ((self.x, self.y - self.r),
                             (self.x + self.r, self.y + self.r),
                             (self.x - self.r, self.y + self.r)))


class IronTarget(Target):
    def __init__(self):
        super().__init__()
        self.color = GREY

    def draw(self):
        pygame.draw.polygon(self.screen, self.color,
                            ((self.x - self.r, self.y - self.r),
                             (self.x + self.r, self.y - self.r),
                             (self.x + self.r, self.y + self.r),
                             (self.x - self.r, self.y + self.r)))


class Bomb(GameObject):
    def __init__(self, x, y, dx):
        self.screen = screen
        self.x = x
        self.y = y
        #self.vx = dx
        self.vy = 5
        self.r = 10

    def draw(self):
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r)

    def move(self):
        #self.x += self.vx
        self.y += self.vy
        self.vy *= 1.05

    def check_delete(self):
        if self.y < HEIGHT * 0.88:
            return True
        else:
            return False


def choose_target():
    """ Случайный выбор типа мишени"""
    random_number = randint(1, 3)
    if random_number == 1:
        return Target()
    elif random_number == 2:
        return AngryTarget()
    elif random_number == 3:
        return IronTarget()


def action_checker():
    global finished
    global targets
    if event.type == pygame.QUIT:
        finished = True
    elif event.type == pygame.MOUSEBUTTONDOWN:
        gun.fire2_start()
    elif event.type == pygame.MOUSEBUTTONUP:
        gun.fire2_end(event)
        random_target = random.choice(targets)
        random_target.drop_bomb()
    elif event.type == pygame.MOUSEMOTION:
        gun.targetting(event)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_z:
            gun.switch_bullet_type('z')
        elif event.key == pygame.K_x:
            gun.switch_bullet_type('x')
        elif event.key == pygame.K_c:
            gun.switch_bullet_type('c')
        elif event.key == pygame.K_a:
            gun.gun_move_left = True
        elif event.key == pygame.K_d:
            gun.gun_move_right = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            gun.gun_move_left = False
        elif event.key == pygame.K_d:
            gun.gun_move_right = False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullets = []
targets = []
bombs = []
clock = pygame.time.Clock()
gun = Gun()
for i in range(3):
    targets.append(Target())

finished = False

while not finished:
    screen.fill(WHITE)
    kills_count = font.render(f"SCORE = {gun.kills_count}", True, [0, 123, 0])
    pygame.draw.rect(screen, LAND_COLOR, ((0, HEIGHT * 0.75), (WIDTH, HEIGHT)))
    pygame.draw.rect(screen, SKY_COLOR, ((0, 0), (WIDTH, HEIGHT * 0.75)))
    screen.blit(kills_count, textpos_kills_count)
    current_bullet_type = font.render(f"Current bullet type: {gun.current_bullet_type}", True, [0, 123, 0])
    screen.blit(current_bullet_type, textpos_current_bullet_type)
    controls = font.render('Press X,Y,Z to switch type of bullet. A - move left. D - move right', True, [0, 123, 0])
    screen.blit(controls, textpos_control)
    gun.draw()
    gun.move()
    for target in targets:
        target.move()
        target.draw()
    for bullet in bullets:
        bullet.draw()
    for bomb in bombs:
        bomb.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        action_checker()

    for bullet in bullets:
        bullet.move()
        if bullet.check_delete():
            bullets.remove(bullet)
        for target in targets:
            if bullet in bullets:
                if bullet.hittest(target):
                    bullets.remove(bullet)
                    if type(bullet) == Bullet and type(target) == Target\
                    or type(bullet) == AntiAngryBullet and type(target) == AngryTarget\
                    or type(bullet) == AntiIronBullet and type(target) == IronTarget:
                        gun.targets_destroed()
                        targets.remove(target)
                        targets.append(choose_target())
        for bomb in bombs:
            if bullet in bullets:
                if bullet.hittest(bomb):
                    bullets.remove(bullet)
                    bombs.remove(bomb)
    if bombs:
        for bomb in bombs:
            if bombs:
                bomb.move()
                if not bomb.check_delete():
                    bombs.remove(bomb)
    gun.power_up()

pygame.quit()
