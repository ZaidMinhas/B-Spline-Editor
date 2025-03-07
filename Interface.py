import pygame
import numpy as np
from LinearStrategy import LinearStrategy
from BezierStrategy import BezierStrategy
from BSplineStrategy import BSplineStrategy

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1400, 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (139, 0, 0)
LIGHT_RED = (255, 102, 102)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interpolation")

# Store points as a list of (x, y) tuples
points = []
interpolated_points = []
linear_points = []
drawCurve  = drawLines = True


def get_points_array():
    return np.array(points)

def interpolate():
    global interpolated_points
    if drawCurve:
        interpolated_points = np.asarray(BSplineStrategy(get_points_array()))
    else:
        interpolated_points = []

    global linear_points
    if drawLines:
        linear_points = np.asarray(LinearStrategy(get_points_array()))
    else:
        linear_points = []

def draw_instructions():
    font = pygame.font.Font(None, 30)
    instructions = [
        "Instructions:",
        "Left Click: Add/Move Points",
        "Right Click: Delete Points",
        "Drag: Move Points",
        "Shift: Show/Hide Lines",
        "Space: Show/Hide Curve",
        "C: Clear Points"
    ]

    for i, line in enumerate(instructions):
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (WIDTH - 300, 20 + i * 30))

running = True
moving_point = None

while running:
    screen.fill(BLACK)

    # Draw points with outline
    for point in points:
        pygame.draw.circle(screen, LIGHT_RED, point, 7)  # Outer light red circle
        pygame.draw.circle(screen, DARK_RED, point, 5)   # Inner dark red circle

    for i_point in interpolated_points:
        pygame.draw.circle(screen, (0,0,255), i_point, 5)  # B-Spline points

    for l_points in linear_points:
        pygame.draw.circle(screen, (100,100,100), l_points, 1)  # Linear interpolation points

    draw_instructions()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if event.button == 1:  # Left-click to add or drag
                for i, point in enumerate(points):
                    if np.linalg.norm(np.array(point) - np.array(mouse_pos)) < 20:
                        moving_point = i
                        break
                else:
                    points.append(mouse_pos)
                    interpolate()


            elif event.button == 3:  # Right-click to delete
                points = [p for p in points if np.linalg.norm(np.array(p) - np.array(mouse_pos)) >= 10]
                interpolate()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                moving_point = None

        if event.type == pygame.MOUSEMOTION:
            if moving_point is not None:
                points[moving_point] = event.pos
                interpolate()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drawCurve = not drawCurve

                interpolate()

            if event.key == pygame.K_LSHIFT:
                drawLines = not drawLines
                interpolate()

            if event.key == pygame.K_c:
                points = []
                interpolate()

    pygame.display.flip()

pygame.quit()