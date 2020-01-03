# IMPORTS
import pygame
pygame.init()
import classesNYAST as c
c.theapp.init_game()
c.spells.print_spell_dict()
c.spells.activate_spell("harm")
c.spells.print_spell_dict()
