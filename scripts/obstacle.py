class Obstacle:
    def __init__(self,width,height,x,y):
        self.obstacle_width = width
        self.obstacle_height = height
        self.obstacle_x = x
        self.obstacle_y = y
    def return_parameters(self):
        return self.obstacle_x, self.obstacle_y, self.obstacle_width, self.obstacle_height