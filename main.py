import pygame
import random
import math
import pygame_gui
from pygame import gfxdraw

# Initialize pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Lissajous Art")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def random_color():
    """Generate a random RGB color."""
    return [random.randint(50, 255) for _ in range(3)]

def lerp_color(color1, color2, t):
    """Linearly interpolate between two colors."""
    return [
        int(color1[i] + (color2[i] - color1[i]) * t) for i in range(3)
    ]

# Lissajous Curve class
class LissajousCurve:
    def __init__(self, amplitude_x, amplitude_y, freq_x, freq_y, delta, duration):
        self.amplitude_x = amplitude_x
        self.amplitude_y = amplitude_y
        self.freq_x = freq_x
        self.freq_y = freq_y
        self.delta = delta
        self.duration = duration
        self.time_elapsed = 0
        self.start_color = random_color()
        self.end_color = random_color()

    def update(self, dt):
        self.time_elapsed += dt

    def draw(self, surface):
        if self.time_elapsed > self.duration:
            return
        t = self.time_elapsed / self.duration  # Normalized lifetime
        color = lerp_color(self.start_color, self.end_color, t)
        for i in range(500):
            angle = i / 50  # Spread the points
            x = WIDTH // 2 + self.amplitude_x * math.sin(self.freq_x * angle + self.delta)
            y = HEIGHT // 2 + self.amplitude_y * math.sin(self.freq_y * angle)
            gfxdraw.pixel(surface, int(x), int(y), color)

# Initialize elements
lissajous_curves = []
curve_spawn_time = 0

# Pygame GUI setup
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
amplitude_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, HEIGHT - 120), (200, 20)),
    start_value=150,
    value_range=(50, 300),
    manager=manager
)
frequency_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, HEIGHT - 50), (200, 20)),
    start_value=3,
    value_range=(1, 10),
    manager=manager
)
duration_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((220, HEIGHT - 120), (200, 20)),
    start_value=7,
    value_range=(2, 15),
    manager=manager
)

# Clock for timing
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Time step in seconds
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

    # Update GUI elements
    manager.update(dt)

    # Read slider values
    amplitude = amplitude_slider.get_current_value()
    frequency = frequency_slider.get_current_value()
    duration = duration_slider.get_current_value()

    # Spawn new curves randomly
    curve_spawn_time += dt
    if curve_spawn_time > random.uniform(1, 3):  # Random spawn interval
        lissajous_curves.append(LissajousCurve(
            amplitude_x=random.randint(50, int(amplitude)),
            amplitude_y=random.randint(50, int(amplitude)),
            freq_x=random.randint(1, int(frequency)),
            freq_y=random.randint(1, int(frequency)),
            delta=random.uniform(0, 2 * math.pi),
            duration=random.uniform(2, duration)
        ))
        curve_spawn_time = 0

    # Update and draw curves
    for curve in lissajous_curves[:]:
        curve.update(dt)
        if curve.time_elapsed > curve.duration:
            lissajous_curves.remove(curve)
        else:
            curve.draw(screen)

    # Draw captions
    font = pygame.font.Font(None, 24)
    amplitude_label = font.render("Amplitude", True, WHITE)
    frequency_label = font.render("Frequency", True, WHITE)
    duration_label = font.render("Duration", True, WHITE)
    screen.blit(amplitude_label, (10, HEIGHT - 100))
    screen.blit(frequency_label, (10, HEIGHT - 70))
    screen.blit(duration_label, (220, HEIGHT - 100))

    # Draw GUI
    manager.draw_ui(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
