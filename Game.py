# This program simulates a memory game with a 4x4 grid

# importing libraries
import pygame, random, time


def main():   
    # initialize all pygame modules (some need initialization)    
    pygame.init()    
    # create a pygame display window    
    pygame.display.set_mode((500, 400))    
    # set the title of the display window    
    pygame.display.set_caption("Momo's Memory game")    
    # get the display surface   
    w_surface = pygame.display.get_surface()    
    # create a game object   
    game = Game(w_surface)    
    # start the main game loop by calling the play method on the game object    
    game.play()   
    # quit pygame and clean up the pygame window   
    pygame.quit()
    
class Game:
    # An object in this class represents a complete game.
    def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')
      
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
      
      # === game specific objects
        # keeps track of score
        self.score = 0
        self.board_size = 4
        self.board = [] 
        self.create_board()
        # list of tiles that have been clicked on
        self.exposed_tiles = []
        # list of tiles that are matching
        self.matching_tiles = []
        # list of tiles that are not matching
        self.non_matching_tiles = []
        
     
    # function that plays the game
    # self is the Game
    def play(self):
        while not self.close_clicked: 
            self.handle_events()
            self.draw()  
      
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second  
            
    # function that creates board with images
    # self is the Game
    def create_board(self):
        # list to be filled with all images
        image_list = []
        # append image_list with all images except cover image
        for i in range(1,9):
            image_list.append('C:\\Users\\momoa\\OneDrive\\Desktop\\Cmput\\image' + str(i) + '.bmp')
        # C:\Users\momoa\OneDrive\Desktop\Cmput\image0.bmp
        # creating list of 16 images
        image_list = image_list + image_list
        # shuffling list
        random.shuffle(image_list)
        
        
        # list of indices of images on board   
        position_list = list(range(0,16))
        width = 100
        height = self.surface.get_height()//self.board_size 
        for row_index in range(0,self.board_size):
            row = []
            for col_index in range(0,self.board_size):
                x = col_index * width
                y = row_index * height
                # image is equal to first image in image_list
                self.image = image_list[position_list[0]]
                # remove that first image from position_list
                position_list.pop(0)
                # make image with Tile class
                tile = Tile(x,y,self.image,self.surface)
                # add image to board
                row.append(tile)
            self.board.append(row)
            
            
    # handles user input and changes game appropriately
    # self if the Game
    def handle_events(self):
        events = pygame.event.get()
        # draw the cover on every tile in non_matching_tiles
        for tile in self.non_matching_tiles:
            tile.make_expose_false()
            # pause before doing so
            time.sleep(0.2)
        
        # always draw images of ones that are matching
        for tile in self.matching_tiles:
            tile.make_expose_true()
        
        # clear non_matching_tiles
        self.non_matching_tiles = []
        
        for event in events:
            
            if event.type == pygame.QUIT:
                self.close_clicked = True
            
            # if click is observed and the game is still going
            if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                for row in self.board:          
                    for tile in row: 
                        # reveal the tile and append it to exposed_tiles
                        tile.reveal_tile(event.pos, self) 
                        # if there are two tiles in exposed_tiles
                        if len(self.exposed_tiles) == 2:
                            # if two images are the same
                            if self.exposed_tiles[0].image == self.exposed_tiles[1].image:
                                # append them to matching_tiles
                                self.matching_tiles.append(self.exposed_tiles[0])
                                self.matching_tiles.append(self.exposed_tiles[1])
                            
                            # if two images are not the same
                            if self.exposed_tiles[0].image != self.exposed_tiles[1].image: 
                                # append to non_matching_tiles
                                self.non_matching_tiles.append(self.exposed_tiles[0])
                                self.non_matching_tiles.append(self.exposed_tiles[1])
                                
                                # show two tiles that are not matching
                                # loop will then go back to beginning where it will display 
                                # as false again but pause before doing so
                                for tile in self.non_matching_tiles:
                                    tile.make_expose_true()
                             
                            # clear exposed_tiles 
                            self.exposed_tiles = []
                    
                 
    # draw the board
    # self is the Game
    def draw(self):          
        self.surface.fill(self.bg_color)  
        # clear the display surface first  
        
        for row in self.board:            
            for tile in row:
                # if the boolean tile.get_expose()is True then draw the image
                if tile.get_expose() == True:
                    tile.draw()  
                # if the boolean is false draw the cover
                elif tile.get_expose() == False:
                    tile.draw_cover()
                # draw the score
                self.draw_score()  
        # update display
        pygame.display.update()
         
    # updates game for the next frame
    # self is the Game
    def update(self):        
        # keeps track of score by second  
        self.score = pygame.time.get_ticks() // 1000 

    # draws the score
    # self is the Game
    def draw_score(self):
        size = self.surface.get_width()       
        fg_color = pygame.Color('white')                
        font = pygame.font.SysFont('', 90)               
        text_string = '' + str(self.score)        
        text_box = font.render(text_string, True, fg_color, self.bg_color)        
        #surface_height = self.surface.get_width()        
        #text_box_height = text_box.get_width()    
        # draw on top right corner
        location = (self.surface.get_width() - text_box.get_width(), 0)               
        self.surface.blit(text_box, location)
    
    # check if the game should continue
    # self is the Game
    def decide_continue(self):
        # self.continue_game is initially false
        self.continue_game = False
        # if any tile in the board is still covered
        # self.continue_game is True and game keeps going
        for row in self.board:
            for tile in row:
                if tile.get_expose()== False:
                    self.continue_game = True
        return self.continue_game
    
    # function that appends exposed_tiles with a tile
    # parameters are: self- Game
    #                 appended_tile - tile to be appended into exposed_tiles
    def append_exposed_tiles(self, appended_tile):
        self.exposed_tiles.append(appended_tile)
            
    
    
# class that represents Tile objects  
class Tile:
    def __init__(self,x,y,image, surface):
        self.x = x
        self.y = y
        self.color = pygame.Color('white')
        self.surface = surface    
        self.image = image
        # boolean that represents whether or not image is covered
        # False = covered
        # True = uncovered
        self.expose = False
        
    
    # draw the image of the tile
    # self is the Tile
    def draw(self):
        
        color = pygame.Color('black')        
        border_width = 5
        image = pygame.image.load(self.image)        
        self.rect = pygame.Rect(self.x, self.y, image.get_width(), image.get_height())        
        pygame.draw.rect(self.surface, color, self.rect, border_width,)        
        self.surface.blit(image, self.rect)
        
    # draw the cover
    # self is the Tile
    def draw_cover(self):
        color = pygame.Color('black')        
        border_width = 5
        image = pygame.image.load('C:\\Users\\momoa\\OneDrive\\Desktop\\Cmput\\image0.bmp')        
        self.rect = pygame.Rect(self.x, self.y, image.get_width(), image.get_height())        
        pygame.draw.rect(self.surface, color, self.rect, border_width,)        
        self.surface.blit(image, self.rect) 
        
    # reveal the tile 
    # parameters: self - the tile object
    #             pos - position of the click
    #             other - Game object containing exposed_tiles
    def reveal_tile(self, pos, other):
        # only reveal tile if it has not been revealed yet
        if self.expose == False:
            # check if there is collision between tile and click
            if self.rect.collidepoint(pos):
                # flip tile and show image
                self.expose = True
                # append tile to exposed_tile
                other.append_exposed_tiles(self)
        return self.expose
             
    # function that returns expose boolean
    # self is Tile
    def get_expose(self):
        return self.expose
    
    # function that turns expose boolean to True
    # parameter is Tile
    def make_expose_true(self):
        self.expose = True
    
    # function that turns expose boolean to False
    # parameter is Tile
    def make_expose_false(self):
        self.expose = False
        
main()
    
