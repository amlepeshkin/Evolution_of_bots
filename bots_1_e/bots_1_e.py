import pygame as p
from sprites import *
import random
botfile = "bot.png"
foodfile = "food.png"
toxinfile = "toxin.png"
# fulscreen size = [1370, 700]
size = [1320, 680]
window = p.display.set_mode(size)
p.display.set_caption("Evolution of bots")
screen = p.Surface(size)
a = True
tile_size = 40
world_map = []
botnow = 0
bots = []
food = []
toxin = []
idxes = []
xes = []
ys =[]
for i in range(Bot.botnumber):
    bots.append(Bot((random.randint(0, 1280))//40*40, (random.randint(0, 640))//40*40, botfile, screen))
    idxes.append(0)
    xes.append(0)
    ys.append(0)
def worldmap():
    global world_map
    world_map = []
    for i in range(33):
        world_map.append([])
        for j in range(17):
            world_map[i].append(0)
    for i in range(100):
        y = random.randint(0, 16)
        x = random.randint(0, 32)
        world_map[x][y] = random.randint(1, 2)

def fillmap():
    global food, toxin
    food = []
    toxin = []
    for row in world_map:
        for col in row:
            a = col
            x, y = world_map.index(row)*tile_size, row.index(col)*tile_size
            if a == 1:
                food.append(Food(x, y, foodfile, screen))
            elif a == 2:
                toxin.append(Toxin(x, y, toxinfile, screen))

def edit_genom():
    for bot in bots:
        bot.genomedit()
def render_all():
    for bot in bots:
        bot.render()
    for piece in food:
        piece.render()
    for piece in toxin:
        piece.render()
running = True
worldmap()
fillmap()
while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            p.quit()
    edit_genom()
    bots = list(filter(lambda b: b.energy > 0 and b.telomer > 0, bots))
    toxin = list(filter(lambda t: not t.to_food, toxin))
    food = list(filter(lambda f: not f.eaten, food))
    if food == [] and toxin == []:
        worldmap()
        fillmap()
    for i in range(len(bots)):
        for qwertyuiop in range(Bot.genomsize):
            botnow = len(bots)
            bots[i].offspring()
            (repeat, idxes[i], xes[i], ys[i]) = bots[i].read_genom(idxes[i])
            if not repeat:
                break
    for t in toxin:
        t.defuzeToxin()
    screen.fill([255, 255, 255])
    render_all()
    window.blit(screen, [0, 0])
    p.display.flip()
    p.time.delay(100)
p.quit()