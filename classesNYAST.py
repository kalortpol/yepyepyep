# IMPORTS
import datetime
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from random import random
from random import seed
seed(1337)

# CLASSES
class App:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.frame_rate = 100
        self.dt = 1 / self.clock.tick(self.frame_rate)
        self.running = False

    def init_game(self):
        game_render.init()
        self.running = True
        self.main_loop()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            game_input.check_mouse()
        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]: # kollar vilka som är nedpressade och vilka som släpps
            game_input.check_key_state(event.type, event.key) # gå till check_key_state för att adda knappar
        else:
            pass

    def on_loop(self):
        effect.on_loop_effect()
        game_input.check_movement() # kontrollerar bools
        game_input.do_movement() # justerar position, kontrollerar hastighet
        player.blocker_list.clear()
        player._on_loop()
        spells.on_loop_spells()
        pass

    def on_render(self):
        game_render.render_tiles_to_screen("testmap.tmx") # Ersätt med hänvisning till rätt map automatiskt
        game_render.render_sprites_to_screen() # Ritar sprites
        game_ui.render_ui()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def main_loop(self):
        while (self.running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            clock = pygame.time.Clock()
            clock.tick(self.frame_rate)

        pygame.quit()

class Maps:
    def __init__(self):
        pass

    def load_map(self, map):
        pass

class Rendering:
    def __init__(self):
        self.size = self.width, self.height = 1024, 748
        self.screen = None
        self.running = True
        self.screen = None
        self.background = None
        self.rect_color = (255, 0, 0)
        self.poly_color = (0, 255, 0)
        self.blocker_list = []

    def init(self):
        pygame.display.set_caption('Dinos äventyr')
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()

    def render_tiles_to_screen(self, filename):
        tmx_data = load_pygame(filename)
        if tmx_data.background_color:
            self.screen.fill(pygame.Color(self.tmx_data.background_color))

        # iterate over all the visible layers, then draw them
        # according to the type of layer they are.
        for layer in tmx_data.visible_layers:

            # draw map tile layers
            if isinstance(layer, pytmx.TiledTileLayer):

                # iterate over the tiles in the layer
                for x, y, image in layer.tiles():
                    image.convert()
                    self.screen.blit(image, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

            # draw object layers
            elif isinstance(layer, pytmx.TiledObjectGroup):

                # iterate over all the objects in the layer
                for obj in layer:

                    # objects with points are polygons or lines
                    if hasattr(obj, 'points'):
                        pygame.draw.lines(self.screen, self.poly_color,
                                          obj.closed, obj.points, 3)
                    properties = obj.__dict__
                    if properties['name'] == 'blocker':
                        x = properties['x']
                        y = properties['y']
                        width = properties['width']
                        height = properties['height']
                        new_rect = pygame.Rect(x, y, width, height)
                        player.blocker_list.append(new_rect)

                    # some object have an image
                    elif obj.image:
                        obj.convert()
                        self.screen.blit(obj.image, (obj.x, obj.y))

                    # draw a rect for everything else
                    else:
                        pygame.draw.rect(self.screen, self.rect_color,
                                         (obj.x, obj.y, obj.width, obj.height), 3)
            # draw image layers
            elif isinstance(layer, pytmx.TiledImageLayer):
                if layer.image:
                    self.screen.blit(layer.image, (0, 0))

    def render_sprites_to_screen(self):
        player.sprite.convert()
        #self.screen.fill((0, 0, 0), player.sprite_rect)
        self.screen.blit(player.sprite, (player.sprite_rect.centerx - 16, player.sprite_rect.centery - 26)) # player sprite
        pass

class Input:
    def __init__(self):
        self.down_held = False
        self.up_held = False
        self.left_held = False
        self.right_held = False

    def check_key_state(self, key_state, event_key):
        if key_state == pygame.KEYDOWN:
            if event_key == pygame.K_DOWN:
                self.down_held = True
            elif event_key == pygame.K_UP:
                self.up_held = True
            elif event_key == pygame.K_LEFT:
                self.left_held = True
            elif event_key == pygame.K_RIGHT:
                self.right_held = True
            elif event_key == pygame.K_1:
                player.change_current_hp(-1)
                print(player.strength)
                print(player.current_hp)
            elif event_key == pygame.K_2:
                pass
            elif event_key == pygame.K_3:
                pass
            elif event_key == pygame.K_4:
                pass
        elif key_state == pygame.KEYUP:
            if event_key == pygame.K_DOWN:
                self.down_held = False
            elif event_key == pygame.K_UP:
                self.up_held = False
            elif event_key == pygame.K_LEFT:
                self.left_held = False
            elif event_key == pygame.K_RIGHT:
                self.right_held = False
            elif event_key == pygame.K_3:
                spells.charge_and_cast_spell(player, player)
        else:
            pass

    def check_movement(self):
        if self.down_held:
            player.y_direction = player.step
        if self.up_held:
            player.y_direction = -player.step
        if self.left_held:
            player.x_direction = -player.step
        if self.right_held:
            player.x_direction = player.step

        if not self.up_held:
                if player.y_direction < 0:
                    player.y_direction = 0
        if not self.down_held:
            if player.y_direction > 0:
                player.y_direction = 0
        if not self.right_held:
            if player.x_direction > 0:
                player.x_direction = 0
        if not self.left_held:
            if player.x_direction < 0:
                player.x_direction = 0
        else:
           pass

    def do_movement(self):
        move_cap = 300
        if player.check_can_move():
            if player.x_direction > move_cap:
                player.x_direction = move_cap
            elif player.x_direction < -move_cap:
                player.x_direction = -move_cap
            else:
                pass
            if player.y_direction > move_cap:
                player.y_direction = move_cap
            elif player.y_direction < -move_cap:
                player.y_direction = -move_cap
            else:
                pass
            if player.x_direction != 0 and player.y_direction != 0:
                if not player.check_player_collision(player.blocker_list):
                    player.location[0] += (0.5 * player.x_direction) * theapp.dt
                    player.location[1] += (0.5 * player.y_direction) * theapp.dt
                else:
                    player.x_direction = 0
                    player.y_direction = 0
            else:
                if not player.check_player_collision(player.blocker_list):
                    player.location[0] += player.x_direction * theapp.dt
                    player.location[1] += player.y_direction * theapp.dt
                else:
                    player.x_direction = 0
                    player.y_direction = 0

            player.sprite_rect.centery = player.location[1]
            player.sprite_rect.centerx = player.location[0]
        else:
            pass

    def check_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            print("Left", mouse_pos)


class Player:
    def __init__(self, name, sprite, level, max_hp, max_mp, strength, intelligence, agility):
        self.name = name
        self.sprite = pygame.image.load(sprite) # laddar bilden, kallas som attribut till objektet
        self.location = [500, 500] # x, y
        self.step = 20 # pixels per second
        self.sprite_rect = pygame.Rect((self.location[0], self.location[1]), (16, 8))
        self.sprite_rect.centery = self.location[1] # sprite position y
        self.sprite_rect.centerx = self.location[0] # sprite position x
        self.agility = agility
        self.strength = strength
        self.intelligence = intelligence
        self.x_direction = 0
        self.y_direction = 0
        self.can_move = True
        self.blocker_list = []
        self.max_hp = max_hp + (0.5 * self.strength)
        self.current_hp = 50 + effect.hp[0]
        self.max_mp = max_mp + (0.5 * self.intelligence)
        self.current_mp = 10 + effect.mp[0]
        self.max_stam = 50 + (0.5 * self.agility)
        self.current_stam = 50
        self.has_stam_regen = True
        self.stam_regen = 0.5
        self.can_move = True
        self.alive = True
        self.poisoned = False
        self.paralyzed = False
        self.has_hp_regen = True
        self.hp_regen = 0.005
        self.has_mp_regen = True
        self.mp_regen = 1
        self.can_cast_spell = True
        self.can_cast_spell_and_move = False
        self.spell_timer = 0
        self.spell_queue = []
        self.level = level
        self.buff_list = []
        self.debuff_list = []
        self.skills_dict = {"magic": 1, "swords": 1, "blocking": 1, "magic_resist": 1}
        self.mp_cost_reduction = 0

    def check_player_collision(self, blocker_list):
        # måste cleara blockers[]-listan efter varje loop! OBS!
        for blocker in blocker_list:
            next_sprite_rect = self.sprite_rect
            next_sprite_rect.centerx += self.x_direction * theapp.dt
            next_sprite_rect.centery += self.y_direction * theapp.dt
            if len(blocker_list) > 0:
                if next_sprite_rect.colliderect(blocker):
                    print("Collide")
                    return True
            else:
                print("Empty blocker list")

    def change_current_hp(self, change_hp):
        self.current_hp += change_hp

    def change_current_mp(self, change_mp):
        self.current_mp += change_mp

    def set_step(self, step_num):
        self.step = step_num

    def check_alive(self):
        if self.alive:
            return True
        else:
            return False

    def check_poisoned(self):
        if self.poisoned:
            return True
        else:
            return False

    def check_paralyzed(self):
        if self.paralyzed:
            return True
        else:
            return False

    def change_can_move(self, state):
        self.can_move = state

    def change_can_cast_spell(self, state):
        self.can_cast_spell = state

    def check_can_move(self):
        if self.can_move:
            return True
        else:
            return False

    def check_has_hp_regen(self):
        if self.has_hp_regen:
            return True
        else:
            return False

    def check_has_mp_regen(self):
        if self.has_mp_regen:
            return True
        else:
            return False

    def spell_cast_do(self, spell):
        real_cast_time = (spell.cast_time) - (0.01 * self.skills_dict["magic"])
        self.spell_timer += real_cast_time
        print("Casting {} spell".format(spell.name))
        self.spell_queue.append(spell)
        self.change_current_mp(-spell.mp_cost)

    def spell_cast_check(self):
        # kollar om det finns spells i kön som är redo att bli kastade
        if self.spell_timer <= 0:
            if len(self.spell_queue) > 0:
                # om det finns spell i kön och spell_timer är 0
                for spell_in_queue in self.spell_queue:
                    # itererar genom kön, kan alltså kasta flera spells!
                    if spell_in_queue.name == "Heal":
                        heal_amount = spell_in_queue.heal_self + (0.2 * self.skills_dict["magic"])
                        self.change_current_hp(heal_amount) # ändras sannolikt
                        print("Healed for {} hp".format(heal_amount))
                        self.spell_queue.remove(spell_in_queue)
                    if spell_in_queue.name == "Haste":
                        self.set_step(100)
                        print("Haste activated!")
                        self.spell_queue.remove(spell_in_queue)
                    if spell_in_queue.name == "Increase strength":
                        effect.add_buff("str_potion", effect.str, 100, 60)
                        print("Increase strength activated!")
                        self.spell_queue.remove(spell_in_queue)

    # minskar med 1 per sekund
    def reduce_spell_timer(self):
        if self.spell_timer > 0:
            self.spell_timer -= 1 * theapp.dt
            print(self.spell_timer)
        else:
            pass

    # ser till att timern aldrig blir < 0
    def spell_timer_prevent_negative(self):
        if self.spell_timer < 0:
            self.spell_timer = 0

    # spelaren står still under spell cast (som standard)
    def spell_timer_set_states(self):
        if self.spell_timer > 0:
            if self.intelligence < 80 or self.can_cast_spell_and_move:
                self.change_can_cast_spell(False)
            else:
                self.change_can_move(False)
                self.change_can_cast_spell(False)
            game_ui.display_spell_cast_bar()
        if self.spell_timer == 0:
            self.change_can_move(True)
            self.change_can_cast_spell(True)

    def spell_states_control(self):
        self.reduce_spell_timer()
        self.spell_timer_prevent_negative()
        self.spell_timer_set_states()

    def hp_regen_do(self):
        if self.current_hp < self.max_hp and self.has_hp_regen:
            self.current_hp += self.hp_regen

    def mp_regen_do(self):
        if self.current_mp < self.max_mp and self.has_mp_regen:
            self.current_mp += self.mp_regen

    def stamina_regen_do(self):
        if self.current_stam < self.max_stam and self.has_stam_regen:
            self.current_stam += self.stam_regen

    def limit_player_hp(self):
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def limit_player_mp(self):
        if self.current_mp > self.max_mp:
            self.current_mp = self.max_mp

    def limit_player_stam(self):
        if self.current_stam > self.max_stam:
            self.current_stam = self.max_stam

    def player_stats_do(self):
        self.hp_regen_do()
        self.mp_regen_do()
        self.stamina_regen_do()
        self.limit_player_hp()
        self.limit_player_mp()
        self.limit_player_stam()

    def get_player_spell_modifier(self):
        spell_modifier = (self.skills_dict["magic"] * 0.2) + (self.intelligence * 0.2)
        return spell_modifier

    def get_player_mp_cost_reduction(self):
        mp_cost_reduction = self.mp_cost_reduction
        return mp_cost_reduction

    def get_current_mp(self):
        current_mp = self.current_mp
        return current_mp

    def get_magic_resist(self):
        magic_resist = (0.15 * self.skills_dict["magic_resist"]) + (0.1 * self.intelligence)
        return magic_resist

    def hit_by_spell_check(self, effect_value):
        chance_bonus = 0.001 * abs(effect_value)
        random_num = random() + chance_bonus - (0.01 * self.get_magic_resist())
        if random_num > 0.95:
            self.gain_skill("magic_resist")
        else:
            pass

    def gain_skill(self, skill):
        skill_amount_random = random()
        if skill_amount_random < 33:
            skill_gain = 0.3
            self.skills_dict[str(skill)] += skill_gain
        if 67 > skill_amount_random > 33:
            skill_gain = 0.6
            self.skills_dict[str(skill)] += skill_gain
        if skill_amount_random > 66:
            skill_gain = 0.9
            self.skills_dict[str(skill)] += skill_gain

    # lägg allt som ska loopas här, och kalla denna från main on_loop!
    def _on_loop(self):
        self.player_stats_do()
        self.spell_states_control()
        self.spell_cast_check()

class Game_UI:
    def __init__(self):
        self.hp_sprite = pygame.image.load("hp_red.png")
        self.hp_start_sprite = pygame.image.load("hp_bar_start.png")
        self.hp_mid_sprite = pygame.image.load("hp_bar_mid.png")
        self.hp_end_sprite = pygame.image.load("hp_bar_end.png")
        self.mp_sprite = pygame.image.load("mp_blue.png")
        self.mp_start_sprite = pygame.image.load("mp_bar_start.png")
        self.mp_mid_sprite = pygame.image.load("hp_bar_mid.png")
        self.mp_end_sprite = pygame.image.load("mp_bar_end.png")
        self.spell_cast_bar = pygame.image.load("cast_bar.png")
        self.spell_cast_bar_rect = self.spell_cast_bar.get_rect()
        self.spell_cast_bar_rect.centerx = 1
        self.spell_cast_bar_rect.centery = 1

    def render_ui(self):
        self.display_hp()
        self.display_mp()
        self.display_stam()
        self.display_spell_cast_bar()

    def display_hp(self):
        hp_spritex = 32
        hp_spritey = 700
        hp_redx = 32
        index = 1
        game_render.screen.blit(self.hp_start_sprite, (0, 700))
        while True:
            if index < player.max_hp:
                game_render.screen.blit(self.hp_mid_sprite, (hp_spritex, hp_spritey))
                if index < player.current_hp:
                    game_render.screen.blit(self.hp_sprite, (hp_redx, hp_spritey))
                    index += 1
                    hp_spritex += 1
                    hp_redx += 1
                else:
                    index += 1
                    hp_spritex += 1
            elif index == player.max_hp:
                game_render.screen.blit(self.hp_end_sprite, (hp_spritex, hp_spritey))
                return False
            else:
                return False

    def display_mp(self):
        mp_spritex = 992
        mp_spritey = 700
        mp_bluex = 960
        index = 1
        game_render.screen.blit(self.mp_start_sprite, (992, 700))
        while True:
            if index < player.max_mp:
                game_render.screen.blit(self.mp_mid_sprite, (mp_spritex, mp_spritey))
                if index < player.current_mp:
                    game_render.screen.blit(self.mp_sprite, (mp_bluex, mp_spritey))
                    index += 0.5
                    mp_spritex -= 1
                    mp_bluex -= 1
                else:
                    index += 0.5
                    mp_spritex -= 1
            elif index == player.max_mp:
                game_render.screen.blit(self.mp_end_sprite, ((mp_spritex - 31), mp_spritey))
                return False
            else:
                return False

    def display_stam(self):
        pass

    def display_spell_cast_bar(self):
        spell_timer = spells.get_spell_timer()
        cast_time = spells.get_cast_time()
        time_left_cast = cast_time - spell_timer
        index = time_left_cast
        self.spell_cast_bar_rect.centerx = player.sprite_rect.centerx
        self.spell_cast_bar_rect.centery = player.sprite_rect.centery - 32

        while index > 0:
            #self.spell_cast_bar_rect.inflate(index, 0)
            game_render.screen.blit(self.spell_cast_bar,
                                    (self.spell_cast_bar_rect.centerx + index, self.spell_cast_bar_rect.centery))
            game_render.screen.blit(self.spell_cast_bar,
                                    (self.spell_cast_bar_rect.centerx - index, self.spell_cast_bar_rect.centery))
            index -= 1 * theapp.dt

class Monster(Player):
    pass

class Spells:
    def __init__(self, name, cast_time, damage, heal, heal_self, slow_type, paralyze_type, poison_type, mp_cost,
                 effect_sprite, self_effect_sprite, special_effect):
        self.name = name
        self.cast_time = cast_time # 1 = 1 sekund, FPS-justerat
        self.damage = damage
        self.heal = heal
        self.heal_self = heal_self
        self.slow_type = slow_type
        self.paralyze_type = paralyze_type
        self.mp_cost = mp_cost
        self.poison_type = poison_type
        self.effect_sprite = effect_sprite
        self.self_effect_sprite = self_effect_sprite
        self.special_effect = special_effect

    def cast_spell(self, caster):
        if caster.can_cast_spell:
            if caster.current_mp >= self.mp_cost:
                caster.spell_cast_do(self)
            else:
                print("You don't have enough mana for {}".format(self.name))
        else:
            print("You are already casting a spell ({})".format(self.name))

class Effects:
    def __init__(self):
        self.hp = [0, 0] # buffmängd, tid (sekunder)
        self.mp = [0, 0]
        self.stam = [0, 0]
        self.step = [0, 10]
        self.int = [0, 0]
        self.str = [0, 0]
        self.agi = [0, 0]
        self.str2 = 10
        pass

    def add_buff(self, effect_to_add, stat_affected, stat_amount, duration):
        player.buff_list.append(effect_to_add)
        stat_affected[0] = stat_amount
        stat_affected[1] = duration
        print(player.buff_list, stat_affected)

    def reduce_buff_timer(self):
        if self.hp[1] > 0:
            self.hp[1] -= 1 * theapp.dt
        if self.mp[1] > 0:
            self.mp[1] -= 1 * theapp.dt
        if self.stam[1] > 0:
            self.stam[1] -= 1 * theapp.dt
        if self.step[1] > 0:
            self.step[1] -= 1 * theapp.dt
        if self.int[1] > 0:
            self.int[1] -= 1 * theapp.dt
        if self.str[1] > 0:
            self.str[1] -= 1 * theapp.dt
        if self.agi[1] > 0:
            self.agi[1] -= 1 * theapp.dt

    def perform_effect(self): # lägg till alla buffar i denna metod utöver därifrån de utförs
            if len(player.buff_list) > 0:
                for buff in player.buff_list:
                    # lägg till buffar här nedan
                    # haste, använd som template
                    if buff in ["haste"]:
                        if self.step[1] < 0:
                            player.buff_list.remove("haste")
                            self.step[0] = 0
                            print("Flushed buff!", self.step[1], self.step[0], player.step)
                    # str potion
                    if buff in ["str_potion"]:
                        if not self.str[1] <= 0:
                            self.str[0] = 20
                        else:
                            player.buff_list.remove("str_potion")
                            self.str[0] = 0
                # lägg till buffs här ovan
            else:
                player.buff_timer = 0
                player.buff_list.clear()

    def on_loop_effect(self):
        self.reduce_buff_timer()
        self.perform_effect()

class Spells_new:
    # klassen ska ta över allt som har med spells att göra, inklusive spell-timers och att kalla rätt renderings-
    # metoder för att visa spell-grafik t ex cast-bar och själva spellsens grafik.
    def __init__(self):
        self.spell_cast_time = 0
        self.spell_timer = 0
        self.spell_timer_on = False
        self.caster = None
        self.victim = None
        self.casting_spell = False
        # lägg in spells i spell_dict enligt heal-mallen. Obs att key måste finnas i cast_spell-metoden
        self.spell_dict = {"heal": {"name": "heal", "mp_cost": 10, "effect_value": 10, "cast_time": 5,
                                    "spell_duration": 0, "type": "hp", "gfx": "blabla.png",
                                    "active": False},
                           "haste": {"name": "haste", "mp_cost": 10, "effect_value": 100, "cast_time": 5,
                                     "spell_duration": 120, "type": "movement_speed", "gfx": "blabla.png",
                                     "active": False},
                           "harm": {"name": "harm", "mp_cost": 10, "effect_value": -50, "cast_time": 10,
                                              "spell_duration": 0, "type": "hp", "gfx": "blabla.png",
                                              "active": True},
                           "spell_template": {"name": "template", "mp_cost": 0, "effect_value": 0, "cast_time": 0,
                                              "spell_duration": 0, "type": "0", "gfx": "blabla.png",
                                              "active": False}
                           }
                            # kopiera spell_template för att lägga till fler spells!

    # Aktiverar spellen som callas som attribut, deaktiverar alla andra spells
    def activate_spell(self, spell):
            for spell_in_dict in self.spell_dict:
                if ["active"]:
                    self.spell_dict[str(spell_in_dict)]["active"] = False
            self.spell_dict[str(spell)]["active"] = True

    def print_spell_dict(self):
        print(self.spell_dict)

    def check_timer_and_cast(self):
        if self.casting_spell:
            if self.spell_timer_on:
                if self.spell_timer < self.spell_cast_time:
                    game_ui.display_spell_cast_bar()
                    print("Waiting to cast")
                    print("cast time:", self.spell_cast_time)
                    print("spell timer:", self.spell_timer)
                if self.spell_timer >= self.spell_cast_time:
                    print("Casting now!")
                    spells.cast_spell(self.caster, self.victim)
                    self.caster = None
                    self.victim = None
                    self.spell_timer_on = False
                    self.spell_cast_time = 0

    def spell_timer_switch(self, state):
        self.spell_timer_on = state

    def get_spell_timer(self):
        return self.spell_timer

    def get_cast_time(self):
        return self.spell_cast_time

    def charge_and_cast_spell(self, caster, victim): # kalla denna för att påbörja spellcast
        if not self.casting_spell:
            self.casting_spell = True
            for spell_in_dict in self.spell_dict:
                if self.spell_dict[spell_in_dict]["active"]:
                    self.spell_cast_time = self.spell_dict[str(spell_in_dict)]["cast_time"]
                    print(self.spell_dict[spell_in_dict]["cast_time"], "är cast time enligt spell_dict, medan följande är spell_cast_time:", self.spell_cast_time)
            self.spell_timer_switch(True)
            self.caster = caster
            self.victim = victim
        else:
            print("You are already casting a spell")

    def spell_timer_control(self):
        if self.spell_timer_on:
            print(self.spell_cast_time)
            print(self.spell_timer)
            self.spell_timer += (1 * theapp.dt)
            self.check_timer_and_cast()
        if not self.spell_timer_on:
            self.spell_timer = 0


# metod som helt sköter castande och healing/skada osv.
    # OBS att damage ska vara av typ "hp" och ha negativt värde, precis som heal är typ "hp" med positivt värde.
    # tanken är att spelaren ska kunna ha EN spell aktiv åt gången, och sen kasta denna med högerklick
    # spelaren ska sedan efter casten få en cooldown där spelaren inte kan casta spells, beroende på hur lång CD
    # spellen har. Eller UO-style med cast time och sedan inte cooldown? Helst UO-varianten. Kika på detta och fixa.
    def cast_spell(self, caster, victim):
        spell_modifier = caster.get_player_spell_modifier()
        mp_cost_reduction = caster.get_player_mp_cost_reduction()
        caster_mp = caster.get_current_mp()
        victim_magic_resist = victim.get_magic_resist()
        if caster.can_cast_spell:
            for spell in self.spell_dict:
                if ["active"]:
                    if ["active"]:  # fixa bort den här jäveln, orkar inte fixa indentet
                        real_mp_cost = self.spell_dict[(spell)]["mp_cost"] - (self.spell_dict[(spell)]["mp_cost"] * mp_cost_reduction)
                        if not real_mp_cost > caster_mp:
                            caster.change_current_mp(-real_mp_cost)
                            spell_type = self.spell_dict[(spell)]["type"]
                            spell_effect_value = self.spell_dict[(spell)]["effect_value"]
                            real_spell_effect_value = spell_effect_value + (spell_effect_value * spell_modifier) # använd vid positiva
                            real_spell_effect_value_resisted = spell_effect_value + (spell_effect_value * spell_modifier) \
                                                        - (spell_effect_value * victim_magic_resist) # använd vid negativa
                            if spell_type in ["hp"]:
                                if spell_effect_value > 0:
                                    victim.change_current_hp(real_spell_effect_value)
                                if spell_effect_value < 0:
                                    victim.change_current_hp(real_spell_effect_value_resisted)
                                    victim.hit_by_spell_check(real_spell_effect_value_resisted)
                            if spell_type in ["mp"]:
                                if spell_effect_value > 0:
                                    victim.change_current_mp(real_spell_effect_value)
                                if spell_effect_value < 0:
                                    victim.change_current_mp(real_spell_effect_value_resisted)
                                    victim.hit_by_spell_check(real_spell_effect_value_resisted)
                            if spell_type in ["stam"]:
                                if spell_effect_value > 0:
                                    victim.change_current_stam(real_spell_effect_value)
                                if spell_effect_value < 0:
                                    victim.change_current_stam(real_spell_effect_value_resisted)
                                    victim.hit_by_spell_check(real_spell_effect_value_resisted)
                            if spell_type in ["str"]:
                                pass
                            if spell_type in ["agi"]:
                                pass
                            if spell_type in ["int"]:
                                pass
                            if spell_type in ["step"]:
                                pass
                            if spell_type in ["armor"]:
                                pass
                            if spell_type in ["skill"]:
                                pass
                        else:
                            print("Not enough mana for {}".format(self.spell_dict[(spell)]["name"]))
                else:
                    print("You need to choose a spell first")
        else:
            print("You cannot cast a spell right now")
        self.casting_spell = False
        self.spell_timer_switch(False)

    def on_loop_spells(self):
        self.spell_timer_control()

class IO:

    # OBS flytta hit allt som har med In/Out att göra. T ex registrering av mus- och tangentbordsklick osv.

    def __init__(self):
        pass

    def get_target(self):
        # metod för att registrera var man klickar! Detta ska sedan användas för att casta spells och i övrigt bara
        # var man klickar. Förslagsvis en rekt som följer muspekaren, och om man trycker på respektive musknapp
        # så kan man använda collide_rect för att se om mus-recten krockar med något objekt som är av klassen
        # "Button" t ex :) Blir skitbra det här.
        pass

    def on_loop_IO(self):
        # lägg metoderna här för att hantera event-queue som gäller tangentbords- och musklickningar osv. DVS
        # flytta dem från class Game hit för att det ska bli mer lättöverskådligt.
        pass

class Collisions:
    def __init__(self):
        pass
### OBJEKT
game_render = Rendering()
game_input = Input()
game_maps = Maps()
game_ui = Game_UI()
effect = Effects()
player = Player("Dino", "hero1.png", 1, 50, 10, 100, 100, 100) # name, image, level, max_hp, max_mp, str, int, agi
theapp = App()

# spells
spells = Spells_new()
heal = Spells("Heal", 3, 0, 0, 10, 0, 0, 0, 6, None, None, None)
haste = Spells("Haste", 5, 0, 0, 0, 0, 0, 0, 0, None, None, 1)
strength_spell = Spells("Increase strength", 5, 0, 0, 0, 0, 0, 0, 0, None, None, None)
# effects
