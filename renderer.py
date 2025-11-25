import pygame
from settings import *
import random
import math

class Renderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
import pygame
from settings import *
import random

class Renderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        # PMingLiU/MingLiU are naturally thin Serif fonts. Removed bold=True for thinner strokes.
        # self.font = pygame.font.SysFont(['pmingliu', 'mingliu', 'simsun'], FONT_SIZE, bold=False)
        # ms gothic font
        self.font = pygame.font.SysFont('SimSun', FONT_SIZE)
        self.wall_chars = WALL_CHARS
        
        # Load Textures
        self.textures = {}
        self.load_textures()
        
    def load_textures(self):
        # Load texture 1
        try:
            texture = pygame.image.load('textures/test_brick.png').convert()
            texture = pygame.transform.scale(texture, (256, 256))
            
            # Pre-calculate brightness array for performance
            # 0 = black, 1 = white
            self.texture_data = []
            width, height = texture.get_size()
            for y in range(height):
                row = []
                for x in range(width):
                    r, g, b, a = texture.get_at((x, y))
                    # Simple grayscale conversion
                    brightness = (r + g + b) / (3 * 255) 
                    row.append(brightness)
                self.texture_data.append(row)
            self.tex_width = width
            self.tex_height = height
            print("Texture loaded successfully.")
        except Exception as e:
            print(f"Failed to load texture: {e}")
            self.texture_data = None

    def draw(self):
        self.screen.fill(BLACK)
        self.render_ascii_walls()

    def render_ascii_walls(self):
        list_objects = self.game.raycasting.ray_casting_result
        for depth, proj_height, texture, ray, offset in list_objects:
            # Always pass the real projected height to ensure correct texture scaling
            self.draw_ascii_column(None, ray, proj_height, offset, depth)

    def get_ascii_column(self, depth, height, texture):
        # This is now handled per-character in draw_ascii_column
        return None 

    def draw_ascii_column(self, _, ray, proj_height, offset, depth):
        # Hybrid spacing:
        # ASCII chars (narrow) are drawn on every ray (10px spacing).
        # CJK chars (wide) are drawn only on even rays (20px spacing) to prevent overlap.
        
        # We are drawing a vertical strip at 'ray' * SCALE
        x = ray * SCALE
        
        # Calculate the real top of the wall (ceiling)
        # Camera height is PLAYER_HEIGHT, so:
        # - (1 - PLAYER_HEIGHT) of wall is above eye level (ceiling)
        # - PLAYER_HEIGHT of wall is below eye level (floor)
        ceiling = HALF_HEIGHT - int(proj_height * (1 - PLAYER_HEIGHT))
        floor = HALF_HEIGHT + int(proj_height * PLAYER_HEIGHT)
        
        # Calculate start and end Y on screen
        y_start = int(max(0, ceiling))
        y_end = int(min(HEIGHT, floor))
        
        # Calculate number of chars to draw
        num_chars = int((y_end - y_start) / FONT_SIZE) + 1
        
        for i in range(num_chars):
            y = y_start + i * FONT_SIZE
            if y >= y_end:
                break
                
            # Calculate 3D distance including vertical AND horizontal components
            # Vertical offset from eye level based on screen position
            vertical_offset = depth * (y - HALF_HEIGHT) / DIST
            
            # Horizontal offset from screen center (left/right)
            horizontal_offset = depth * (x - HALF_WIDTH) / DIST
            
            # True 3D distance from camera to this point
            actual_distance = math.sqrt(depth * depth + vertical_offset * vertical_offset + horizontal_offset * horizontal_offset)
            
            # Calculate distance lighting intensity using actual 3D distance
            norm_depth = actual_distance / MAX_DEPTH
            dist_intensity = 1 - norm_depth * DARKNESS_FACTOR
            dist_intensity = max(0, min(1, dist_intensity))
                
            # Texture Mapping
            if self.texture_data:
                # Horizontal coordinate (u)
                tex_x = int(offset * (self.tex_width - 1))
                
                # Vertical coordinate (v) start and end for this character
                # The character covers FONT_SIZE pixels on screen
                # In wall space (0..1), this covers:
                v_start = (y - ceiling) / proj_height
                v_end = (y + FONT_SIZE - ceiling) / proj_height
                
                # Map to texture coordinates
                t_y_start = int(v_start * self.tex_height)
                t_y_end = int(v_end * self.tex_height)
                
                # Ensure we sample at least one pixel
                if t_y_end <= t_y_start:
                    t_y_end = t_y_start + 1
                
                # Average brightness over the vertical range
                # Handle wrapping/tiling simply by modulo
                total_brightness = 0
                count = 0
                
                # Optimization: If range is too large, just sample a few points
                step = 1
                if (t_y_end - t_y_start) > 10:
                    step = (t_y_end - t_y_start) // 10
                
                for ty in range(t_y_start, t_y_end, step):
                    sample_y = ty % self.tex_height
                    total_brightness += self.texture_data[sample_y][tex_x]
                    count += 1
                
                tex_brightness = total_brightness / max(1, count)
            else:
                tex_brightness = 1.0
            
            # Combine lighting
            final_intensity = dist_intensity * tex_brightness
            
            # Select Char
            char_index = int(final_intensity * (len(self.wall_chars) - 1))
            char_index = max(0, min(len(self.wall_chars) - 1, char_index))
            char = self.wall_chars[char_index]
            
            # Hybrid spacing check
            if ord(char) > 255:
                if ray % 2 != 0:
                    continue
            
            text_surface = self.font.render(char, True, WHITE)
            self.screen.blit(text_surface, (x, y))
