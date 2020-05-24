import pygame

class Laser:
    def __init__(self, x, y, color, step = 2):
        self.x = x
        self.y = y
        self.color = color
        self.step = step

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, 1, 1))

    def move(self):
        if self.color == (255, 255, 0):
            self.y += self.step
        else:
            self.y -= self.step

    def off_screen(self):
        return not (400-20 >= self.y >= 20)


class Player:
    def __init__(self, x, y, color, health=100):
        self.x = x
        self.y = y
        self.height = 23
        self.width = 21
        self.color = color
        self.val = 2.5
        self.health = health
        self.max_health = 100
        self.cool_down_counter = 0
        self.lasers = []
        self.alive = False


    def shoot(self, enemy):
        if enemy.alive:
            if self.cool_down_counter == 0:
                y1 = self.y
                if self.color == (255, 255, 0):
                    y1 += 11
                laser = Laser(self.x + 10, y1, self.color)
                self.lasers.append(laser)
                self.cool_down_counter = 1

    def healthbar(self, window):
        if self.color == (255, 255, 0):
            delta = -5 - 5 - self.height
        else:
            delta = 5
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.height + delta, self.width, 5))
        if self.health > 0:
            pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.height + delta, self.width * (self.health / self.max_health), 5))

    def move_lasers(self):
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen():
                self.lasers.remove(laser)

    def shooted(self, enemy):
        i = 0
        for i in range(len(enemy.lasers) - 1):
            if self.collide(enemy.lasers[i]):
                del enemy.lasers[i]
                if self.health > 0:
                    self.health -= 1

    def collide(self, enemy_l):
        return (self.x + self.width >= enemy_l.x >= self.x) & (self.y + self.height >= enemy_l.y >= self.y)

    def cooldown(self):
        if self.cool_down_counter >= 30:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move(self, enemy):
        self.alive = True
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x >= 20:
                self.x -= self.val

        if keys[pygame.K_RIGHT]:
            if self.x <= 400 - 20 - self.width:
                self.x += self.val

        if keys[pygame.K_SPACE]:
            self.shoot(enemy)

        self.move_lasers()
        self.shooted(enemy)
