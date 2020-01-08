import pygame
import pytmx
import pyscroll
from sys import exit

pygame.init()

class Rendering:
    def __init__(self):
        self.size = self.width, self.height = 1024, 748
        self.screen = None
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
        # map_rect = pygame.Rect((0, 0), (self.width, self.height))
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, screen_size, clamp_camera=True, tall_sprites=1)
        self.map_layer.zoom = 2
        # make the PyGame SpriteGroup with a scrolling map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)


    def init_sprites(self):
        # Add sprites to the group
        self.group.add(engine.player) # lista ut hur skiten funkar.. om jag orkar
        #self.group.add(monster_dummy)
        #self.group.add(monster_dummy2)
        # Center the layer and sprites on a sprite


    def draw_and_blit(self):
        # Draw the layer
        self.group.center(engine.player.rect)
        self.group.draw(self.screen)
        self.group.update()
        pygame.display.flip()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = [100, 100]
        self.image = engine.file.hero_img
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

class Game_input():
    def __init__(self):
        pass

    def handle_key(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            engine.player.move_player(0, -1)
        if pygame.key.get_pressed()[pygame.K_s]:
            engine.player.move_player(0, 1)
        if pygame.key.get_pressed()[pygame.K_a]:
            engine.player.move_player(-1, 0)
        if pygame.key.get_pressed()[pygame.K_d]:
            engine.player.move_player(1, 0)
        if pygame.key.get_pressed()[pygame.K_p]:
            print(engine.get_dt())
            print(engine.get_fps())

    def handle_mouse(self):
        pass

    def handle_event(self):
        pass

class Engine:
    """Här ska alla objekt ligga, de ska sedan aldrig kallas direkt utan alltid via inneboende metoder.
    Gör gärna en metod som hjälper till att kalla andra objekts metoder.
    Håll hela programmet OOP"""
    def __init__(self):
        self.running = False
        self.clock = pygame.time.Clock()
        # all objects below, everything will be initiated correctly hopefully
        self.file = Files()
        self.rendering = Rendering()
        self.player = Player()
        self.game_input = Game_input()
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
        self.rendering.init_graphics()
        self.rendering.init_sprites()
        self.running = True
        self.main_loop()

    def on_event(self, event):
        pass

    def on_loop(self):
        self.game_input.handle_key()
        pass

    def on_render(self):
        self.rendering.draw_and_blit()

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

class Files:
    def __init__(self):
        self.hero_img = pygame.image.load("hero1.png")


engine = Engine()
engine.start()
