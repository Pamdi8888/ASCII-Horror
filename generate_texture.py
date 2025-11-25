import pygame
import os

# Initialize pygame (needed for Surface)
pygame.init()

# Settings
WIDTH, HEIGHT = 256, 256
BRICK_W = 64
BRICK_H = 32
MORTAR_SIZE = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create surface
surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill(BLACK) # Mortar color (background)

# Draw bricks
rows = HEIGHT // BRICK_H
cols = WIDTH // BRICK_W

for r in range(rows):
    for c in range(cols + 1): # +1 to handle offset wrapping if needed
        
        # Calculate position
        x = c * BRICK_W
        y = r * BRICK_H
        
        # Offset every other row
        if r % 2 == 1:
            x -= BRICK_W // 2
            
        # Draw brick rect (inset by mortar size)
        rect = pygame.Rect(
            x + MORTAR_SIZE // 2, 
            y + MORTAR_SIZE // 2, 
            BRICK_W - MORTAR_SIZE, 
            BRICK_H - MORTAR_SIZE
        )
        
        pygame.draw.rect(surface, WHITE, rect)

# Ensure directory exists
if not os.path.exists('textures'):
    os.makedirs('textures')

# Save
save_path = 'textures/test_brick.png'
pygame.image.save(surface, save_path)
print(f"Texture saved to {save_path}")
