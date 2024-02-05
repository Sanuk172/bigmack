from io import BytesIO
import pygame_gui

import pygame
from functions import *


class BigMap:
    options = ['map', 'sat', 'map,skl']

    def __init__(self):
        self.image = None
        self.lon, self.lat = get_toponym_coord(get_toponym(geocode('Переулок лучевой 3 миасс')))
        self.layer = 'map'
        self.z = 17
        self.manager = pygame_gui.UIManager(SIZE)
        self.layers_select = (pygame_gui.elements.UIDropDownMenu(self.options, self.options[0],
                                                                 pygame.Rect(440, 10, 200, 30),
                                                                 self.manager))
        self.search_field = pygame_gui.elements.UITextEntryLine(pygame.Rect(175, 420, 300, 30), self.manager)
        self.update_map()

    def update_map(self):
        map_params = {
            "ll": ",".join(map(str, (self.lon, self.lat))),
            'z': self.z,
            "l": self.layer,
            'size': '650,450'
        }
        image = BytesIO(get_static(**map_params))
        self.image = pygame.image.load(image)

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                self.z = min(self.z + 1, 21)
            if event.key == pygame.K_PAGEDOWN:
                self.z = max(self.z - 1, 0)
            if event.key == pygame.K_LEFT:
                self.lon = (self.lon + 180 - 200 * 2 ** (-self.z)) % 360 - 180
            if event.key == pygame.K_RIGHT:
                self.lon = (self.lon + 180 + 200 * 2 ** (-self.z)) % 360 - 180
            if event.key == pygame.K_UP:
                self.lat = min(self.lat + 70 * 2 ** (-self.z), 89)
            if event.key == pygame.K_DOWN:
                self.lat = max(self.lat - 70 * 2 ** (-self.z), -89)
            self.update_map()
        self.manager.process_events(event)

    def gui_event_handler(self, event):
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.layers_select:
                self.layer = event.text
                self.update_map()

    def draw(self, surf):
        surf.blit(self.image, (0, 0))
        self.manager.draw_ui(surf)

    def update_gui(self, delta):
        self.manager.update(delta)


pygame.init()
SIZE = WIDTH, HEIGHT = 650, 450
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

app = BigMap()

running = True

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        app.event_handler(event)
        app.gui_event_handler(event)
    app.update_gui(time_delta)
    screen.fill('black')
    app.draw(screen)
    pygame.display.flip()
pygame.quit()
