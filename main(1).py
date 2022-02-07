import os
import sys

import pygame
import requests

deviation_x = 0
deviation_y = 0
mpz = 15
mpt = 0
list_mpt = ["map", "sat"]

map_file = "map.png"


def update_map():
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={37.530887 + deviation_x},{55.703118 + deviation_y}&z={mpz}&l={list_mpt[mpt]}"
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
while pygame.event.wait().type != pygame.QUIT:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN and mpz < 19:
                mpz += 1
            if event.key == pygame.K_PAGEUP and mpz > 2:
                mpz -= 1
            if event.key == pygame.K_UP:
                deviation_y += 0.002 * (19 - mpz)
            if event.key == pygame.K_DOWN:
                deviation_y -= 0.002 * (19 - mpz)
            if event.key == pygame.K_RIGHT:
                deviation_x += 0.002 * (19 - mpz)
            if event.key == pygame.K_LEFT:
                deviation_x -= 0.002 * (19 - mpz)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mpt < 1:
                    mpt += 1
                else:
                    mpt = 0
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    update_map()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)