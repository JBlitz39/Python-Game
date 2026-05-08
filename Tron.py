import pygame
import time
import random
from start_screen import StartScreen

class Player:
    def __init__(self, x, y, b, c, image):
        self.x = x
        self.y = y
        self.speed = 1
        self.bearing = b
        self.colour = c
        self.rect = pygame.Rect(self.x - 1, self.y -1, 2, 2)
        
        self.start_boost = time.time()
        
        self.powerup = None
        self.in_powerup = False
        self.end_time = 0
        self.temp = 0
        
        self.image = image
        self.curRect = [self.rect]

    def draw(self):
        self.rect = pygame.Rect(self.x -1, self.y -1, 2, 2)
        if self.image:
            screen.blit(pygame.transform.scale(self.image, (2, 2)), self.rect)
        else:
            pygame.draw.rect(screen, self.colour, self.rect)

    def move(self):
        self.x += self.bearing[0]
        self.y += self.bearing[1]

    def add_powerup(self, powerup):
        if self.powerup == None:
            pickup_fx.play()
            self.powerup = powerup.effect

    def apply_powerup(self):
        if self.in_powerup == False:
            powerup_fx.play()
            self.end_time = time.time() + 3
            self.in_powerup = True
            match self.powerup:
                case "speedUp":
                    self.speed *=2
                case "pauseEnemy":
                    for obj in objects:
                        if obj != self:
                            self.temp = obj.speed
                            obj.speed = 0
                case "reverseMovement":
                    if objects[0] == self:
                        bearingx[1] = (-2, 0)
                        bearingy[1] = (0, -2)
                    else:
                        bearingx[0] = (-2, 0)
                        bearingy[0] = (0, -2)
                    
        else:
            if time.time() > self.end_time:
                self.end_time = 0
                self.in_powerup = False
                match self.powerup:
                    case "speedUp":
                        self.speed = int(self.speed / 2)
                    case "pauseEnemy":
                        for obj in objects:
                            if obj!= self:
                                obj.speed = self.temp
                    case "reverseMovement":
                        if objects[0] == self:
                            bearingx[1] = (2, 0)
                            bearingy[1] = (0, 2)
                        else:
                            bearingx[0] = (2, 0)
                            bearingy[0] = (0, 2)
                self.powerup = None


class PowerUp:
    def __init__(self, effect, x, y):
        self.effect = effect
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - 16, self.y - 16, 32, 32)
        match effect:
            case "speedUp":
                self.image = pygame.image.load('assets/speedup.png').convert_alpha()
            case "pauseEnemy":
                self.image = pygame.image.load('assets/pause.png').convert_alpha()
            case "reverseMovement":
                self.image = pygame.image.load('assets/reverse.png').convert_alpha()

    def draw(self):
        screen.blit(pygame.transform.scale(self.image, (32, 32)), self.rect)




def new_game():
    new_p1 = Player(50, (height - offset)/2, (2, 0), p1_colour, p1_image)
    new_p2 = Player(width - 50, (height - offset) / 2, (-2, 0), p2_colour, None)
    return new_p1, new_p2



restart_game = True
while restart_game == True:
    restart_game = False
    width = 700
    height = 760
    start_screen = StartScreen(width, height)
    if start_screen.run() == False:
        pygame.quit()
    else:
        pygame.init()

        offset = height-width
        screen = pygame.display.set_mode((width,height))
        p1_image = pygame.image.load('assets/path1.png').convert_alpha()
        bg_image = pygame.image.load('assets/bgimage.png').convert_alpha()
        screen_rect = pygame.Rect(0, offset, width, height-offset)
        pygame.mixer.music.load('assets/bgmusic.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0.0)
        death_fx = pygame.mixer.Sound('assets/death.mp3')
        death_fx.set_volume(0.2)
        pickup_fx = pygame.mixer.Sound('assets/pickup.mp3')
        pickup_fx.set_volume(0.2)
        powerup_fx = pygame.mixer.Sound('assets/powerup.mp3')
        powerup_fx.set_volume(0.2)





            




        powerup_time = time.time()
        font = pygame.font.Font(None, 72)


        powerups = ["speedUp", "pauseEnemy", "reverseMovement"]
        pu_objects = []
        pu_rects = []

        #Colours are below
        black = (0,0,0)
        p1_colour = (0,255,255)
        p2_colour = (255,0,255)

        pygame.display.set_caption("Tron")

        clock = pygame.time.Clock()
        check_time = time.time()


        objects = []
            
        path = []
        p1 = Player(50, (height- offset) / 2, (2, 0), p1_colour, p1_image)
        p2 = Player(width - 50, (height - offset) /2, (-2, 0), p2_colour, None)
        objects.append(p1)
        path.append((p1.rect, '1'))
        #[(rect, '1'), (rect, '2')]
        objects.append(p2)
        path.append((p2.rect, '2'))

        player_score = [0,0]


        #append only adds one value, we need that one value to be a list of other values to add multiple

        wall_rects = [pygame.Rect([0, offset, 15, height]), pygame.Rect([0, offset, width, 15]),
                     pygame.Rect([width-15, offset, 15, height]), pygame.Rect([0, height-15, width, 15])]

        
        start_time = time.time()

        bearingx = [(2, 0), (2, 0)]
        bearingy = [(0, 2), (0, 2)]


        new = False
        done = False
        while not done:
            if restart_game == True:
                break

            
            if time.time() - start_time > 20:
                speed = 2
            elif time.time() - start_time > 10:
                speed = 1
            else:
                speed = 0.5


            
            screen.fill(black)
            screen.blit(pygame.transform.scale(bg_image, (width, int(height-offset))), screen_rect)

            for rect in wall_rects:
                pygame.draw.rect(screen, (128, 0, 128), rect, 0)

            return_text = font.render("Return", True, (255, 255, 255))
            return_rect = return_text.get_rect(center = (width//4, offset/2))
            screen.blit(return_text, return_rect)

            
            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if return_rect.collidepoint(event.pos):
                        restart_game = True
                        break
                elif event.type == pygame.KEYDOWN:
                    #Player1
                    new_bearing = objects[0].bearing
                    if event.key == pygame.K_w:
                        new_bearing = (0, -bearingy[0][1])
                    elif event.key == pygame.K_s:
                        new_bearing = (0, bearingy[0][1])
                    elif event.key == pygame.K_a:
                        new_bearing = (-bearingx[0][0], 0)
                    elif event.key == pygame.K_d:
                        new_bearing = (bearingx[0][0], 0)
                    elif event.key == pygame.K_e:
                        objects[0].apply_powerup()

                    if (objects[0].bearing != (-new_bearing[0], -new_bearing[1])):
                        objects[0].bearing = new_bearing

                    #Player2
                    new_bearing = objects[1].bearing
                    if event.key == pygame.K_UP:
                        new_bearing = (0, -bearingy[1][1])
                    elif event.key == pygame.K_DOWN:
                        new_bearing = (0, bearingy[1][1])
                    elif event.key == pygame.K_LEFT:
                        new_bearing = (-bearingx[1][0], 0)
                    elif event.key == pygame.K_RIGHT:
                        new_bearing = (bearingx[1][0], 0)
                    elif event.key == pygame.K_PERIOD:
                        objects[1].apply_powerup()

                    if (objects[1].bearing != (-new_bearing[0], -new_bearing[1])):
                        objects[1].bearing = new_bearing
                        
            if restart_game == True:
                continue
            
            cur_time = time.time()
            if (cur_time - powerup_time) > 5:
                new_effect = random.choice(powerups)#['speedup', 'pauseenemy', 'reversemovement']
                new_x = random.randint(31, width - 31) #randint = random integer (whole number)
                new_y = random.randint(offset + 31, height - 31)
                new_obj = PowerUp(new_effect, new_x, new_y + offset)
                pu_objects.append(new_obj)
                pu_rects.append(new_obj.rect)
                powerup_time = cur_time

            


            
            breakAll = False
            for obj in objects:
                if breakAll == True:
                    break
                    
                for i in range(obj.speed):
                    if (obj.rect, '1') in path or (obj.rect, '2') in path or obj.rect.collidelist(wall_rects) > -1:
                        if (time.time() - check_time) >= 0.1:
                            check_time = time.time()
                            power_time = check_time

                            
                            death_fx.play()
                            if obj.colour == p1_colour:
                                player_score[1] +=1
                            else:
                                player_score[0] +=1
                            
                            new = True
                            start_time = time.time()
                            new_p1, new_p2 = new_game()
                            objects = [new_p1, new_p2]
                            path = [(new_p1.rect, '1'), (new_p2.rect, '2')]
                            pu_objects = []
                            pu_rects = []
                            bearingx = [(2, 0), (2, 0)]
                            bearingy = [(0, 2), (0, 2)]
                            breakAll = True
                            break

                            
                    else:
                        if obj.in_powerup == True:
                            obj.apply_powerup()
                        index = obj.rect.collidelist(pu_rects) #pu_rects = [rect1, rect2, rect3] pu_objects = [powerup1, powerup2, powerup3]
                        if index > -1:
                            obj.add_powerup(pu_objects[index])
                            pu_objects.pop(index)
                            pu_rects.pop(index)
                            
                        
                        path.append((obj.rect, '1')) if obj.colour == p1_colour else path.append((obj.rect, '2'))
                        
                    obj.draw()
                    obj.move()

            for rect in path:
                if new is True:
                    path = []
                    new = False
                    break
                #rect = (rect, player)
                #Loops through each position of list. Rect is like a box and we access values inside of the box.
                if rect[1] == '1':
                    pygame.draw.rect(screen, p1_colour, rect[0], 0)
                    screen.blit(pygame.transform.scale(objects[0].image, (2, 2)), rect[0])
                else:
                    pygame.draw.rect(screen, p2_colour, rect[0], 0)
            
            for obj in pu_objects:
                obj.draw()

            
            #powerups = ["speedUp", "pauseEnemy", "reverseMovement"]
            pu_display1_rect = pygame.Rect(0, 0, offset - 4, offset - 4)
            pu_display2_rect = pygame.Rect(width - offset - 4, 0, offset - 4, offset - 4)
            if objects[0].powerup:
                match objects[0].powerup:
                    case "speedUp":
                        pu_image = pygame.image.load('assets/speedup.png').convert_alpha()
                    case "pauseEnemy":
                        pu_image = pygame.image.load('assets/pause.png').convert_alpha()
                    case "reverseMovement":
                        pu_image = pygame.image.load('assets/reverse.png').convert_alpha()
                screen.blit(pygame.transform.scale(pu_image, (offset - 4, offset - 4)), pu_display1_rect)
            if objects[1].powerup:
                match objects[1].powerup:
                    case "speedUp":
                        pu_image = pygame.image.load('assets/speedup.png').convert_alpha()
                    case "pauseEnemy":
                        pu_image = pygame.image.load('assets/pause.png').convert_alpha()
                    case "reverseMovement":
                        pu_image = pygame.image.load('assets/reverse.png').convert_alpha()
                screen.blit(pygame.transform.scale(pu_image, (offset - 4, offset - 4)), pu_display2_rect)
            
            
            
            #display score on the screen
            score_text = font.render('{0} : {1}'.format(player_score[0], player_score[1]), 1, (255, 153, 51))
            score_text_pos = score_text.get_rect()
            score_text_pos.centerx = int(width/2)
            score_text_pos.centery = int(offset/2)
            screen.blit(score_text, score_text_pos)

            

            pygame.display.flip()
            
            clock.tick(60 * speed)
            
            
        pygame.quit()
