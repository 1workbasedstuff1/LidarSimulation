import pygame, sys, math

class Robot:
    def __init__(self, x, y):
        self.Position = [x, y]
        self.Speed = [0, 0]
        self.Orientation = 0
        self.Control_speed = 0
        self.Turn_speed = 0
    
    def set_Speed(self, speedX, speedY):
        self.Speed[0] = speedX
        self.Speed[1] = speedY

    def set_Position(self, PosX, PosY):
        self.Position[0] = PosX
        self.Position[1] = PosY

    def set_Control_Speed(self, speed):
        self.Control_speed = speed

    def set_Orientation(self, bearing):
        self.Orientation = bearing

    def set_Turn_speed(self, speed):
        self.Turn_speed = speed

    def get_Position(self):
        return self.Position
    
    def get_Control_Speed(self):
        return self.Control_speed

    def get_Speed(self):
        return self.Speed
    
    def get_Orientation(self):
        return self.Orientation
    
    def get_Orientation_rads(self):
        return math.radians(self.get_Orientation())
    
    def get_Turn_speed(self):
        return self.Turn_speed
    


class Grid_Map:

    def __init__(self , pixel_width , pixel_height , num_of_xcells, num_of_ycells):

        assert pixel_width % num_of_xcells == 0, "Horizontal cell count must divide horizontal pixel count"
        assert pixel_height % num_of_ycells == 0, "Vertical cell count must divide vertical pixel count"

        self.width = pixel_width
        self.height = pixel_height
        self.x_cells = num_of_xcells
        self.y_cells = num_of_ycells

        self.cell_width = pixel_width//num_of_xcells
        self.cell_height = pixel_height//num_of_ycells

    def get_pixel_dim(self):
        return (self.width, self.height)
    
    def get_pixel_width(self):
        return self.width
    
    def get_pixel_height(self):
        return self.height
    
    def get_num_of_cells(self):
        return [self.x_cells, self.y_cells]
    
    def get_cell_dim(self):
        return [self.cell_width , self.cell_height]
    

class Lidar(Robot):
    def __init__(self, x, y, Orientation, angle, rotation_speed, max_range, samples_per_cycle):
        super().__init__(x, y)
        self.Orientation = Orientation
        self.angle = angle  # angle of lidar on robot
        self.rot_speed = rotation_speed
        self.range = max_range
        self.sample_rate = samples_per_cycle
        self.Abs_lidar_angle = Orientation + angle

    def get_lidar_angle(self):
        return (self.angle%360)

    def get_rot_speed(self):
        return self.rot_speed
    
    def get_sample_rate(self):
        return self.sample_rate
    
    def get_lidar_range(self):
        return self.range
    
    def set_lidar_angle(self, new_angle):
        self.angle = new_angle







def draw_cell(Map ,width_index , height_index):
    return pygame.Rect(width_index*Map.get_cell_dim()[0] , height_index*Map.get_cell_dim()[1] , Map.get_cell_dim()[0], Map.get_cell_dim()[1])

def draw_robot(robot_name):
    # Create a surface for the robot
    robot_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    robot_surface.fill((0, 0, 255))  # Blue color
    
    # Draw the red line on the robot surface
    rotation_rad = robot_name.get_Orientation_rads()
    start_pos = (25, 25)  # Center of the robot surface
    pygame.draw.line(robot_surface, (255, 0, 0), start_pos, (50, 25), 4)
    
    # Rotate the surface based on the robot's orientation
    rotated_surface = pygame.transform.rotate(robot_surface, -robot_name.get_Orientation())
    rotated_rect = rotated_surface.get_rect(center=(robot_name.get_Position()[0], robot_name.get_Position()[1]))

    return rotated_surface, rotated_rect

def check_collision(robot_rect, map_rects):
    return any(robot_rect.colliderect(cell) for cell in map_rects)


def draw_lidar_on_screen(screen, robot_name, lidar_name, map_rects):
    # Compute the absolute angle of the lidar in radians
    Absolute_lidar_angle = robot_name.get_Orientation() + lidar_name.get_lidar_angle()
    Angle = math.radians(Absolute_lidar_angle)
    
    # Compute the start and end position of the lidar line
    start_pos = (robot_name.get_Position()[0], robot_name.get_Position()[1]) #Simply draws line with length of line
    end_pos = (start_pos[0] + lidar_name.get_lidar_range() * math.cos(Angle), 
               start_pos[1] + lidar_name.get_lidar_range() * math.sin(Angle))
    
    # Initialize collision variables
    collision_point = None
    collided = False

    # Check for collision with any map rects
    for rect in map_rects:
        # Check if the line intersects the rectangle
        if rect.clipline(start_pos, end_pos):
            collided = True
            # Get the intersection points
            intersection_points = rect.clipline(start_pos, end_pos) #finds all collsion coordinates
            if intersection_points:
                # Calculate the distance from start_pos to the first intersection point
                collision_point = intersection_points[0]
                break

    # Draw the lidar line in the appropriate color
    color = (255, 0, 0) if collided else (0, 255, 0)
    pygame.draw.line(screen, color, start_pos, end_pos, 3)
    
    if collided and collision_point:
        # Calculate the length of the lidar line from start to collision
        length = math.hypot(collision_point[0] - start_pos[0], collision_point[1] - start_pos[1])
        #print(f"Lidar Angle: {Absolute_lidar_angle % 360}     Length: {length:.2f}")
    else:
        length = None
        #print(f"Lidar Angle: {Absolute_lidar_angle % 360}     Length:")

    # Update the lidar angle for the next frame
    lidar_name.set_lidar_angle(lidar_name.get_lidar_angle() + lidar_name.get_rot_speed())
    return [ Absolute_lidar_angle%360 , length]