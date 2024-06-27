import pygame ,random

#init
pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Shooter")

#Setting the fps and clock
FPS = 60
clock = pygame.time.Clock()

#set colors
WHITE = (255 ,255 , 255)
BLACK = ( 0 , 0, 0)
RED = (255 , 0 , 0)
YELLOW = (255 ,255 , 0)
#game class
class Game():
    def __init__(self , target , bullet_group):
        self.PLAYER_STARTING_LIVES = 5
        self.score = 0
        self.player_lives = self.PLAYER_STARTING_LIVES
        
        self.font = pygame.font.Font('custom.ttf' , 50)
        self.target = target
        self.bullet_group = bullet_group
        
        self.frame_count = 0
        self.seconds = 0
        self.round_time = 0
        
        self.miss_sound = pygame.mixer.Sound('sounds/miss_sound.wav')
        self.hit_sound = pygame.mixer.Sound('sounds/hit_sound.wav')
        
        pygame.mixer.music.load('sounds/shooter_bg.wav')
    
    def update(self):
        self.draw()
        self.check_collisions()
        self.count_time()
        self.game_over()
      
    def draw(self):
        score_text = self.font.render('Score ' + str(self.score) , 1 , RED , YELLOW)
        score_rect = score_text.get_rect()
        score_rect.topleft = (20 , 10)
        
        lives_text = self.font.render('Lives ' + str(self.player_lives) , 1 , RED , YELLOW)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20 , 10)
        
        #blit the text
        display_surface.blit(score_text , score_rect)
        display_surface.blit(lives_text , lives_rect)
        pygame.draw.line(display_surface , BLACK , (0, 64) , (WINDOW_WIDTH , 64))
    
    def check_collisions(self):
        if pygame.sprite.spritecollide(self.target , self.bullet_group , True):
            self.hit_sound.play()
            self.reset()
            self.score += 1
            self.frame_count = 0
            self.seconds = 0
        for bullet in self.bullet_group:
            bullet.rect.x += bullet.velocity
            if bullet.rect.right > WINDOW_WIDTH:
                bullet.kill()
                self.player_lives -= 1
                self.miss_sound.play()
    
    def reset(self):
        self.target.rect.right = random.randint(WINDOW_WIDTH - 32 ,  WINDOW_WIDTH)
        self.target.rect.top = random.randint(74 , WINDOW_HEIGHT - 42)
    
      #framecounts
        self.frame_count = 0
        self.seconds = 0
    
    def count_time(self):
        self.frame_count += 1
        if self.frame_count == FPS:
            self.seconds += 1
            self.round_time += 1
            self.frame_count = 0
        if self.seconds == 5:
            self.player_lives -= 1
            self.reset()
            self.frame_count = 0
            self.seconds = 0
    
    def pause_game(self , main_text , sub_text):
        main_text = self.font.render(main_text ,1 , RED)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT // 2)
        
        
        sub_text = self.font.render(sub_text ,1 , RED)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT // 2 + 50)
        
        display_surface.blit(sub_text , sub_rect)
        display_surface.blit(main_text , main_rect)
        pygame.display.update()
        
    def game_over(self):
        if self.round_time == 60 or self.player_lives == 0:
            pygame.display.update()
            global run 
            is_paused = True
            while is_paused:
                self.pause_game("Press any space to continue" , "Final Score " + str(self.score))
                
                #updating the lives to fix the bug
                lives_text = self.font.render('Lives ' + str(self.player_lives) , 1 , RED , YELLOW)
                lives_rect = lives_text.get_rect()
                lives_rect.topright = (WINDOW_WIDTH - 20 , 10)
                display_surface.blit(lives_text , lives_rect)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_paused = False
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            is_paused = False
                            self.player_lives = self.PLAYER_STARTING_LIVES
                            self.score = 0
                
    
#target class
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load('image/target.png')
        self.rect = self.image.get_rect()
        self.rect.right = random.randint(WINDOW_WIDTH - 32 ,  WINDOW_WIDTH)
        self.rect.top = random.randint(74 , WINDOW_HEIGHT - 42)
        

#bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self , x , y):
        super().__init__()
        
        self.image = pygame.Surface((10 , 8))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        
        self.velocity = 10
    
    
    
#player class
class Player(pygame.sprite.Sprite):
    def __init__(self , x , y ):
        super().__init__()
        
        self.image = pygame.image.load('image/shooter.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        
        self.velocity = 5
        
    def update(self):
        self.move()
    
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_UP] and self.rect.top > 64:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity
        
    def shoot(self):
        bullet = Bullet(player.rect.right , player.rect.top + 20)
        bullet_group.add(bullet)
        
#bullet group
bullet_group = pygame.sprite.Group()

#player group
player_group = pygame.sprite.Group()
player = Player(32 , WINDOW_HEIGHT // 2)
player_group.add(player)

#target object
target = Target() 

#game object
my_game = Game(target , bullet_group)


pygame.mixer.music.play(-1 , 0.0)

#game loop
run = True
while run:
    display_surface.fill(WHITE)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    #game object
    my_game.update()
    
    #target group
    target.update()
    display_surface.blit(target.image , target.rect)
    
    #bullet group
    bullet_group.update()
    bullet_group.draw(display_surface)
    
    #player group 
    player_group.update()
    player_group.draw(display_surface)
         
    pygame.display.update()


#quit
pygame.quit()