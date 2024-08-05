import pygame
import sys
import math
from A_HeaderFile3 import Robot, Grid_Map, draw_cell, draw_robot, check_collision, draw_lidar_on_screen, Lidar

Grid_plan = Grid_Map(800, 800, 10, 10)

robot1 = Robot(200, 200)
robot1.set_Control_Speed(3)
robot1.set_Turn_speed(2)

lidar1 = Lidar(robot1.get_Position()[0], robot1.get_Position()[1], robot1.get_Orientation(), robot1.get_Orientation(), 3, 160, 30)
# lidar initialized with robot1's position, orientation, rotation speed of 10, range of 100 pixels, 30 samples per cycle

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Grid_plan')
section_width = 800
section_height = 800
screen = pygame.display.set_mode((section_width * 2, section_height))
pygame.display.set_caption('Grid_plan')


Map = []
for i in range(10):  # sketches box around outside
    Map.append([0, i])
    Map.append([i, 0])
    Map.append([9, i])
    Map.append([i, 9])

Map.append([1, 5])
Map.append([2, 5])
Map.append([3, 5])
Map.append([4, 5])

map_rects = [draw_cell(Grid_plan, coords[0], coords[1]) for coords in Map]

Point_Cloud = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        robot1.set_Orientation(robot1.get_Orientation() + robot1.get_Turn_speed())
    if keys[pygame.K_RIGHT]:
        robot1.set_Orientation(robot1.get_Orientation() - robot1.get_Turn_speed())
    if keys[pygame.K_UP]:
        rads = robot1.get_Orientation_rads()
        # Update robot position based on orientation
        new_x = robot1.get_Position()[0] + robot1.get_Control_Speed() * math.cos(rads)
        new_y = robot1.get_Position()[1] + robot1.get_Control_Speed() * math.sin(rads)

        # Temporary set the new position
        robot1.set_Position(new_x, new_y)
        
        # Check for collision
        robot_surface, robot_rect = draw_robot(robot1)
        if check_collision(robot_rect, map_rects):
            # If collision detected, reset to previous position
            robot1.set_Position(robot1.get_Position()[0] - 2 * robot1.get_Control_Speed() * math.cos(rads), robot1.get_Position()[1] -2 * robot1.get_Control_Speed() * math.sin(rads))

    # Fill the left section with white and the right section with black
    screen.fill((255, 255, 255), (0, 0, section_width, section_height))  # Left side
    screen.fill((100, 100, 100), (section_width, 0, section_width, section_height))  # Right side

    # Draw the map on the left section
    for cell in map_rects:
        pygame.draw.rect(screen, (0, 0, 0), cell.move((0, 0)))  # Left section

    # Draw the robot and lidar on the left section
    robot_surface, robot_rect = draw_robot(robot1)
    screen.blit(robot_surface, (robot_rect.x, robot_rect.y))  # Left section
    #draw_lidar_on_screen(screen, robot1, lidar1, map_rects)  # Left section
    angle , lidar_length = draw_lidar_on_screen(screen, robot1, lidar1, map_rects) #in headerfile2
    print(angle , lidar1.get_lidar_angle(), lidar_length)
    lidar_rads = math.radians(angle)
    
    if lidar_length != None:
        Point_Cloud.append((robot1.get_Position()[0]+800 + lidar_length*math.cos(lidar_rads) , robot1.get_Position()[1] + lidar_length*math.sin(lidar_rads)))

    for points in Point_Cloud:
        pygame.draw.circle(screen, (0,255,255) , points , 1)

    # For the right side, draw a black display or other content if needed

    pygame.display.flip()
    clock.tick(60)