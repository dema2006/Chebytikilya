import os
import sys

import pygame
import requests


mpz = 15
mpt = "map"

map_file = "map.png"


def update_map():
    map_request = f"http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&z={mpz}&l={mpt}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
update_map()
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
while True:
    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_PAGEDOWN and mpz < 19:
                mpz += 1
                print(1)
            if i.key == pygame.K_PAGEUP and mpz > 2:
                mpz -= 1
                print(2)
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    update_map()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


# Удаляем за собой файл с изображением.
os.remove(map_file)