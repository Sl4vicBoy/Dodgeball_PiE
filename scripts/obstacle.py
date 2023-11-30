import pygame.draw


class Obstacle(pygame.sprite.Sprite): #niezniszczalna przeszkoda 
    def __init__(self, width, height, x, y, color):
        super().__init__() 
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.collission_ball = True
        

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Midline(Obstacle): # linia po srodku 
    def __init__(self,width,height,x,y,color):
        super().__init__()
        self.collision_ball = False
        
    

class Destroyable_Obstacle(Obstacle):
    def __init__(self,width,height,x,y,color,time_to_live):
        super().__init__()
        self.time_to_live = time_to_live
    
    def destroy(self):
        pass


