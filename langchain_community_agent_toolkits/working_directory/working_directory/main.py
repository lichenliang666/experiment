import pygame
import sys
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    player = pygame.Rect(400, 300, 50, 50)
    player_color = (0, 255, 0)

    # 创建围绕 player 的 10 个元素
    elements = []
    for i in range(10):
        angle = 2 * math.pi * i / 10
        distance = 100
        x = player.centerx + distance * math.cos(angle)
        y = player.centery + distance * math.sin(angle)
        element = pygame.Rect(x, y, 20, 20)
        elements.append(element)
    element_color = (255, 0, 0)

    angle_offset = 0  # 旋转角度偏移

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 移动 player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5

        # 更新围绕元素的位置，并添加旋转效果
        angle_offset += 0.02  # 旋转速度
        for i, element in enumerate(elements):
            angle = 2 * math.pi * i / 10 + angle_offset
            distance = 100
            element.x = player.centerx + distance * math.cos(angle) - element.width / 2
            element.y = player.centery + distance * math.sin(angle) - element.height / 2

        screen.fill((30, 30, 30))  # 深灰背景
        pygame.draw.rect(screen, player_color, player)
        for element in elements:
            pygame.draw.rect(screen, element_color, element)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()