import pygame as p
import random
botfile = "bot.png"
foodfile = "food.png"
toxinfile = "toxin.png"
size = [1320, 680]
tile_size = 40
world_map = []
botnow = 0
def Intersect(s1_x, s1_y, s2_x, s2_y):
    if ((s1_x>s2_x-50) and (s1_x<s2_x+50) and (s1_y>s2_y-50) and (s1_y<s2_y+50)):
        return 1
    else:
        return 0
def Touching(s1_x, s1_y, s2_x, s2_y):
    if ((s1_x>s2_x-30) and (s1_x<s2_x+30) and (s1_y>s2_y-30) and (s1_y<s2_y+30)):
        return 1
    else:
        return 0
class Bot:
    genomsize = 64
    botnumber = 16
    def __init__(self, xpos, ypos, filename, screen, gen=None):
        if gen == None:
            self.genom = [8] * Bot.genomsize
        else:
            self.genom = list(gen)
        self.energy = 90
        self.telomer = 4
        self.screen = screen
        self.x = xpos
        self.y = ypos
        self.bitmap = p.image.load(filename)
    def render(self):
        self.screen.blit(self.bitmap,(self.x, self.y))
    def genomedit(self):
        if random.randint(1, 4) == 1:
            x = random.randint(0, Bot.genomsize - 1)
            self.genom[x] = random.randint(0, 63)
    def read_genom(self, idx):
        genom = list(self.genom)
        a = genom[idx]
        repeat = True
        if self.energy < 1 or self.telomer < 1 or any(map(lambda t: Touching(self.x, self.y, t.x, t.y), toxin)):
            self.energy = 0
            self.x = -tile_size**2
            self.y = -tile_size**2
        else:
            if a > -1 and a < 8:
                if a == 0:
                    self.x -= tile_size
                    self.y -= tile_size
                elif a == 1:
                    self.x -= 0
                    self.y -= tile_size
                elif a == 2:
                    self.x += tile_size
                    self.y -= tile_size
                elif a == 3:
                    self.x += tile_size
                    self.y -= 0
                elif a == 4:
                    self.x += tile_size
                    self.y += tile_size
                elif a == 5:
                    self.x -= 0
                    self.y += tile_size
                elif a == 6:
                    self.x -= tile_size
                    self.y += tile_size
                elif a == 7:
                    self.x -= tile_size
                    self.y -= 0
                
                idx += 1
                self.energy -= 1
                repeat = False
            elif a > 7 and a < 16:
                for pice in food:
                    x, y = pice.x, pice.y
                    if Intersect(self.x, self.y, x, y):
                        pice.eaten = True
                        self.energy += 10
                idx += 1
            elif a > 15 and a < 24:
                for pice in toxin:
                    x, y = pice.x, pice.y
                    if Intersect(self.x, self.y, x, y):
                        pice.to_food = True
                idx += 1
            elif a > 23 and a < 32:
                idx += 1
            elif a > 31 and a < 64:
                idx += a + 1

        idx = idx % Bot.genomsize
        if self.energy > 90:
            self.energy = 90
        self.x = self.x % size[0]
        self.y = self.y % size[1]
        return (repeat, idx, self.x, self.y)
    def offspring(self):
        if botnow < Bot.botnumber and self.energy > 1 and self.telomer > 1:
            bots.append(Bot(self.x, self.y, botfile, self.screen, self.genom))
            idxes.append(0)
            xes.append(0)
            ys.append(0)
            self.telomer -=1
class Food:
    def __init__(self, xpos, ypos, filename, screen):
        self.screen = screen
        self.x = xpos
        self.y = ypos
        self.eaten = False
        self.bitmap = p.image.load(filename)
    def render(self):
        self.screen.blit(self.bitmap,(self.x, self.y))
class Toxin:
    def __init__(self, xpos, ypos, filename, screen):
        self.screen = screen
        self.x = xpos
        self.y = ypos
        self.to_food = False
        self.bitmap = p.image.load(filename)
    def render(self):
        self.screen.blit(self.bitmap,(self.x, self.y))
    def defuzeToxin(self):
        if self.to_food:
            world_map[self.x//tile_size][self.y//tile_size] = 1
            food.append(Food(self.x, self.y, foodfile, self.screen))
bots = []
food = []
toxin = []
idxes = []
xes = []
ys =[]