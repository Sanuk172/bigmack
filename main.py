from io import BytesIO

import pygame
from functions import get_static


class BigMap:
    def __init__(self):
        self.image = None
        self.lon, self.lat = 60.153191, 55.156353
        self.layer = 'map'
        self.z = 0
        self.update_map()

    def update_map(self):
        map_params = {
            "l": "map",
            "z": self.z,
            "ll": ",".join(map(str, (self.lon, self.lat))),
            "size": "650,450"
        }
        image = BytesIO(get_static(**map_params))
        self.image = pygame.image.load(image)

    def draw(self, surf):
        surf.blit(self.image, (0, 0))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                self.z = min(self.z + 1, 21)
            if event.key == pygame.K_PAGEDOWN:
                self.z = max(self.z - 1, 0)
            if event.key == pygame.K_LEFT:
                self.lon = (self.lon - 180 - 200 * 2 ** (-self.z)) % 360 - 180
            if event.key == pygame.K_RIGHT:
                self.lon = (self.lon - 180 + 200 * 2 ** (-self.z)) % 360 - 180
            if event.key == pygame.K_UP:
                self.lat = min(self.lat + 70 * 2 ** (-self.z), 88)
            if event.key == pygame.K_DOWN:
                self.lat = min(self.lat - 70 * 2 ** (-self.z), -88)
            self.update_map()


pygame.init()
SIZE = W, H = 650, 450
screen = pygame.display.set_mode(SIZE)
app = BigMap()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        app.event_handler(event)
    screen.fill(pygame.Color('black'))
    app.draw(screen)
    pygame.display.flip()
