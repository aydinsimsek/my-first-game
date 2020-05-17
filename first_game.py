import pygame
pygame.init()

screenWidth = 650
screenHeight = 650 
window = pygame.display.set_mode((screenWidth, screenHeight)) 

pygame.display.set_caption("Aydin's Game")

clock = pygame.time.Clock()

bg = pygame.image.load('background.jpg')
walkRight = [pygame.image.load('right1.png'), pygame.image.load('right2.png'), pygame.image.load('right3.png'), pygame.image.load('right4.png'), pygame.image.load('right5.png'), pygame.image.load('right6.png'), pygame.image.load('right7.png'), pygame.image.load('right8.png'), pygame.image.load('right9.png')]
walkLeft = [pygame.image.load('left1.png'), pygame.image.load('left2.png'), pygame.image.load('left3.png'), pygame.image.load('left4.png'), pygame.image.load('left5.png'), pygame.image.load('left6.png'), pygame.image.load('left7.png'), pygame.image.load('left8.png'), pygame.image.load('left9.png')]
bulletEffect = pygame.mixer.Sound('bullet.wav')

score = 0 


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.distance = 10
        self.isJump = False
        self.jumpCount = 7
        self.left = False
        self.right = False
        self.walkCount = 0
        self.stand = True
        self.health = 100
        self.invisible = False 
        self.hitbox = (self.x + 18, self.y + 8, 25, 50)  

    def draw(self, window):
        if not self.invisible: 
            if self.walkCount + 1 >= 27:    
                self.walkCount = 0 

            if not self.stand:
                if self.left:
                    window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1

                elif self.right:
                    window.blit(walkRight[self.walkCount // 3], (self.x, self.y)) 
                    self.walkCount += 1 
            else:
                if self.right:
                    window.blit(walkRight[0], (self.x, self.y))
                else:
                    window.blit(walkLeft[0], (self.x, self.y))

            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (0.5 * (100 - self.health)), 10))
            self.hitbox = (self.x + 18, self.y + 8, 25, 50)

    def collide(self):
        if not self.invisible: 
            self.x = 50
            self.y = 420
            self.walkCount = 0
            self.isJump = False
            self.jumpCount = 7 
            font_col = pygame.font.SysFont('californianfb', 16, True)
            text = font_col.render('YOU GOT TOO CLOSE TO THE ENEMY AND TOOK DAMAGE!', 1, (255, 0, 0), True)
            window.blit(text, (325 - (text.get_width()/2), 125 - (text.get_height()/2)))  
            pygame.display.update()
            i = 0
            while i < 150:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 151
                        pygame.quit()
            if self.health > 10: 
                self.health -= 10
            else:
                self.invisible = True

    def block(self):
        if self.hitbox[0] < 350: 
            self.x = 300 
            self.y = 420
            self.walkCount = 0
            self.isJump = False
            self.jumpCount = 7
        else:
            self.x = 370
            self.y = 420
            self.walkCount = 0
            self.isJump = False
            self.jumpCount = 7
        

class projectile(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 10 * direction

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


class obstacle(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, 40, 70)  

    def draw(self, window):
        pygame.draw.rect(window, (150, 75, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, 40, 70)
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 2)


class enemy(object):
    attackRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png'), pygame.image.load('R10.png'), pygame.image.load('R11.png')]
    attackLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png'), pygame.image.load('L10.png'), pygame.image.load('L11.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.end = end
        self.path = [self.x, self.end] 
        self.attackCount = 0
        self.distance = 3
        self.hitbox = (self.x + 11, self.y + 2, 37, 57)
        self.health = 100
        self.invisible = False 

    def draw(self, window):
        if not self.invisible: 
            self.move() 
            if self.attackCount +1 >= 27:
                self.attackCount = 0

            if self.distance > 0:
                window.blit(self.attackRight[self.attackCount // 3], (self.x, self.y))
                self.attackCount += 1

            else:
                window.blit(self.attackLeft[self.attackCount // 3], (self.x, self.y))
                self.attackCount += 1

            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (0.5 * (100 - self.health)), 10)) 
            self.hitbox = (self.x + 11, self.y + 2, 37, 57)  
    
    def move(self):
        if self.distance > 0:
            if self.x + self.distance < self.path[1]:
                self.x += self.distance
            else:
                self.distance = self.distance * -1
                self.attackCount = 0
        else:
            if self.x - self.distance > self.path[0]:
                self.x += self.distance
            else:
                self.distance = self.distance * -1
                self.attackCount = 0

    def hit(self):
        if self.health > 10: 
            self.health -= 10
        else:
            self.invisible = True 
        

def gameWindow(): 
    window.blit(bg, (0, 0))
    tiny_guy.draw(window)
    tiny_enemy.draw(window)
    obs.draw(window)
    for bullet in ammunition:
        bullet.draw(window)
    text = font.render('Score: ' + str(score), 1, (255,0,0))
    window.blit(text, (480, 50))  
    pygame.display.update()
    if tiny_enemy.invisible:
        font_col = pygame.font.SysFont('californianfb', 36, True) 
        text = font_col.render('YOU WON!', 1, (255, 0, 0), True)
        window.blit(text, (325 - (text.get_width()/2), 125 - (text.get_height()/2)))  
        pygame.display.update()
    if tiny_guy.invisible:
        font_col = pygame.font.SysFont('californianfb', 36, True) 
        text = font_col.render('YOU LOST!', 1, (255, 0, 0), True)
        window.blit(text, (325 - (text.get_width()/2), 125 - (text.get_height()/2)))  
        pygame.display.update()  


# main loop
tiny_guy = player(100, 420, 64, 64)
tiny_enemy = enemy(400, 420, 64, 64, 550)
obs = obstacle(350, 420, 40, 70)
shootCount = 0 
ammunition = []
font = pygame.font.SysFont('arial', 30, True)  
ready = True

while ready:
    gameWindow() 
    clock.tick(24)
     
    if tiny_guy.hitbox[1] < tiny_enemy.hitbox[1] + tiny_enemy.hitbox[3] and tiny_guy.hitbox[1] + tiny_guy.hitbox[3] > tiny_enemy.hitbox[1]:
        if tiny_guy.hitbox[0] + tiny_guy.hitbox[2] > tiny_enemy.hitbox[0] + 20 and tiny_guy.hitbox[0] < tiny_enemy.hitbox[0] + tiny_enemy.hitbox[2]:
            if not tiny_enemy.invisible:
                tiny_guy.collide()

    if tiny_guy.hitbox[1] < obs.hitbox[1] + obs.hitbox[3] and tiny_guy.hitbox[1] + tiny_guy.hitbox[3] > obs.hitbox[1]:
        if tiny_guy.hitbox[0] + tiny_guy.hitbox[2] > obs.hitbox[0] and tiny_guy.hitbox[0] < obs.hitbox[0] + obs.hitbox[2]:
            tiny_guy.block()

    if shootCount > 0:
        shootCount += 1

    if shootCount > 10:
        shootCount = 0 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ready = False

    for bullet in ammunition:
        if not tiny_enemy.invisible:
            if bullet.y - bullet.radius < tiny_enemy.hitbox[1] + tiny_enemy.hitbox[3] and bullet.y + bullet.radius > tiny_enemy.hitbox[1]:
                if bullet.x + bullet.radius > tiny_enemy.hitbox[0] and bullet.x - bullet.radius < tiny_enemy.hitbox[0] + tiny_enemy.hitbox[2]:
                    tiny_enemy.hit()
                    score += 10 
                    ammunition.pop(ammunition.index(bullet))  

        if bullet.y - bullet.radius < obs.hitbox[1] + obs.hitbox[3] and bullet.y + bullet.radius > obs.hitbox[1]:
            if bullet.x + bullet.radius > obs.hitbox[0] and bullet.x - bullet.radius < obs.hitbox[0] + obs.hitbox[2]:
                ammunition.pop(ammunition.index(bullet)) 
        
        if 0 < bullet.x < 650:
            bullet.x += bullet.velocity
        else:
            ammunition.pop(ammunition.index(bullet))  

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootCount == 0:
        bulletEffect.play() 
        if tiny_guy.left:
            direction = -1
        else:
            direction = 1 
        if len(ammunition) < 10: 
            ammunition.append(projectile(round(tiny_guy.x + tiny_guy.width // 2), round(tiny_guy.y + tiny_guy.height // 2), 3, (0,0,0), direction))

        shootCount = 1 
        
    if keys[pygame.K_LEFT] and tiny_guy.x >= tiny_guy.distance:
        tiny_guy.x -= tiny_guy.distance
        tiny_guy.left = True
        tiny_guy.right = False
        tiny_guy.stand = False
    elif keys[pygame.K_RIGHT] and tiny_guy.x <= screenWidth - tiny_guy.distance - tiny_guy.width:
        tiny_guy.x += tiny_guy.distance
        tiny_guy.right = True
        tiny_guy.left = False
        tiny_guy.stand = False
    else:
        tiny_guy.stand = True 
        tiny_guy.walkCount = 0
        
    if not tiny_guy.isJump:
        if keys[pygame.K_UP]:
            tiny_guy.isJump = True
            tiny_guy.left = False
            tiny_guy.right = False
            tiny_guy.walkCount = 0
    else:
        if tiny_guy.jumpCount >= -7:
            constant = 1 
            if tiny_guy.jumpCount < 0:
                constant = -1 
            tiny_guy.y -= (tiny_guy.jumpCount ** 2) * 0.65 * constant
            tiny_guy.jumpCount -= 1
        else:
            tiny_guy.isJump = False
            tiny_guy.jumpCount = 7
        
            
pygame.quit()
