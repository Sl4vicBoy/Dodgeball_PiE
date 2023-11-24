
screen_width, screen_height = (800),(600)
middle_line_width = (10)
border_parameters = (5)
class Obstacle:
    def __init__(self,width,height,x,y):
        self.obstacle_width = width
        self.obstacle_height = height
        self.obstacle_x = x
        self.obstacle_y = y
    def return_parameters(self):
        return (self.obstacle_x, self.obstacle_y, self.obstacle_width, self.obstacle_height)
    
middle_line = Obstacle(middle_line_width,screen_height,screen_width//2 - middle_line_width//2,0)
right_line =  Obstacle(border_parameters,screen_height,screen_width-border_parameters,0)
left_line = Obstacle(border_parameters,screen_height,0,0)
up_line = Obstacle(screen_width,border_parameters,0,0)
down_line = Obstacle(screen_width,border_parameters,0,screen_height-border_parameters)