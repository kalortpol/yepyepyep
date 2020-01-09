import pygame
import pytmx
import pyscroll
from sys import exit
import os

"""RENDERING CALSS"""
class Rendering:
    def __init__(self):
        self.size = self.width, self.height = 1024, 748
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.running = True
        self.background = None
        self.tmx_data = None
        self.map_data = None
        self.map_layer = None
        self.group = None

    def init_graphics(self):
        pygame.display.set_caption('Dinos äventyr')
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.background = pygame.Surface(self.screen.get_size())
        self.tmx_data = pytmx.load_pygame("real_map.tmx")
        # Make data source for the map
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        # Make the scrolling layer
        screen_size = (self.width, self.height)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, screen_size, clamp_camera=True, tall_sprites=1)
        self.map_layer.zoom = 2
        # make the PyGame SpriteGroup with a scrolling map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)


    def init_sprites(self):
        # Add sprites to the group
        self.group.add(player) # lista ut hur skiten funkar.. om jag orkar
        #self.group.add(monster_dummy)
        #self.group.add(monster_dummy2)
        # Center the layer and sprites on a sprite


    def draw_and_blit(self):
        # Draw the layer
        self.group.center(player.rect)
        self.group.draw(self.screen)
        self.group.update()
        pygame.display.flip()

""" objekt för rendering-klassen"""
rendering = Rendering()


"""FILES CLASS"""
class File():
    def __init__(self):
        """
        image_list är alla bilder i image-mappen som har hittats av
        get_file()
        """
        self.image_list = list()

        """
        loaded_images_dict är ett dict med alla bilder som har pygame.image.load:ats
        """
        self.loaded_images_dict = dict()

        self.map_dict = dict()

    """
     Söker igenom my_dir (ange alltså directory som argument).
     Lagrar filer i listor, just nu
     .png-filer i self.image_dict
     .tmx-filer i self.map_dict
    """

    def get_files(self, my_dir):
        file_list = next(os.walk(str(my_dir)))[2]
        print(file_list)
        for found_file in file_list:
            if not found_file in self.image_list:
                if ".png" in found_file:
                    self.image_list.append(found_file)
                if ".tmx" in found_file:
                    self.map_dict.append(str(found_file))

    """				
     Denna metod kallas för att få tag i rätt map utifrån, metoden kallas med map:ens filnamn som argument.
     Funkar med och utan string-formatering.
    """

    def get_map(self, map_to_get):
        for map_item in self.map_dict:
            if map_item == str(map_to_get):
                return map_to_get
            else:
                print("Map not found!")

    """ 
     Denna metod kan kallas utifrån för att få tag i rätt bild, kan kallas med eller utan string-formatering. 
     Det är filnamnet som ska vara argument.
     Den laddar alla bilder 1(!) gång med convert_alpha() och sedan gör den inte det igen,
     för att undvika onödiga laddningar. 
    """

    def get_image(self, file_name):
        if str(file_name) in self.loaded_images_dict:
            return self.loaded_images_dict[str(file_name)]
        if not str(file_name) in self.loaded_images_dict:
            image = pygame.image.load(str(file_name)).convert_alpha()
            self.loaded_images_dict[str(file_name)] = image
            return self.loaded_images_dict[str(file_name)]

""" objekt för file-klassen"""
file = File()


"""PLAYER CLASS (PARENT TO MONSTER)"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = [100, 100]
        self.image = file.get_image("hero1.png")
        self.rect = self.image.get_rect()
        self.xvel, self.yvel = 0, 0
        self.vitals = {"hp": 100, "mp": 100, "stam": 100}
        self.stats = {"str": 10, "agi": 10, "int": 10}
        self.can_states = {"spells": True, "move": True}
        self.dt = 0

    def move_player(self, xvel, yvel):
        self.xvel = xvel * engine.get_dt()
        self.yvel = yvel * engine.get_dt()

        self.position[0] += self.xvel
        self.position[1] += self.yvel
        self.rect.center = self.position

""" objekt för player-klassen"""
player = Player()


""" INPUT-CLASS"""
class Game_input():
    def __init__(self):
        pass

    def handle_key(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            player.move_player(0, -1)
        if pygame.key.get_pressed()[pygame.K_s]:
            player.move_player(0, 1)
        if pygame.key.get_pressed()[pygame.K_a]:
            player.move_player(-1, 0)
        if pygame.key.get_pressed()[pygame.K_d]:
            player.move_player(1, 0)
        if pygame.key.get_pressed()[pygame.K_p]:
            print(engine.get_dt())
            print(engine.get_fps())

    def handle_mouse(self):
        pass

    def handle_event(self):
        pass

""" input-objektet"""
game_input = Game_input()


""" GAME ENGINE """
class Engine:
    """Här ska alla objekt ligga, de ska sedan aldrig kallas direkt utan alltid via inneboende metoder.
    Gör gärna en metod som hjälper till att kalla andra objekts metoder.
    Håll hela programmet OOP"""
    def __init__(self):
        self.running = False
        self.clock = pygame.time.Clock()
        # all objects below, everything will be initiated correctly hopefully
        rendering.init_graphics()
        self.loops = 0
        self.fps = 900

    def get_fps(self):
        return self.clock.get_fps()

    def get_dt(self):
        return self.clock.tick(self.fps) / 10

    """Lägg till alla metoder som måste kallas för att initiera objekt osv.
    Jag har markerat den punkt som det hittills fungerar vid med en kommentar"""
    def start(self):
        """Här under fungerar metoderna garanterat tillsammans"""
        rendering.init_graphics()
        rendering.init_sprites()
        self.running = True
        self.main_loop()

    def on_event(self, event):
        pass

    def on_loop(self):
        game_input.handle_key()
        pass

    def on_render(self):
        rendering.draw_and_blit()

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(self.fps)

""" game-engine-objektet"""
engine = Engine()


engine.start()
