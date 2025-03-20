import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Circle
from matplotlib.animation import FuncAnimation
import numpy as np

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
plt.title('Sensor Visualization')

# Plot the rectangle (arena)
initial_x = 0.25
initial_y = 0.25

rectangle_width = 0.4
rectangle_height = 0.6
rect = Rectangle((initial_x, initial_y), width=rectangle_width, height=rectangle_height, edgecolor='red', facecolor='red', alpha=0.5)
ax.add_patch(rect)

# Set axis limits and aspect ratio
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')

# Define the positions for the 8 ultrasonic sensors

sensor_positions = {
    'S1': (initial_x, initial_y),
    'S2': (initial_x + rectangle_width, initial_y),
    'S3': (initial_x, initial_y + rectangle_height),
    'S4': (initial_x + rectangle_width, initial_y + rectangle_height),
    'S5': (initial_x + rectangle_width / 2, initial_y),
    'S6': (initial_x + rectangle_width / 2, initial_y + rectangle_height),
    'S7': (initial_x, initial_y + rectangle_height / 2),
    'S8': (initial_x + rectangle_width, initial_y+ rectangle_height / 2)
}

# Plot the ultrasonic sensors (small circles)
sensor_radius = 0.015
for pos in sensor_positions.values():
    sensor = Circle(pos, sensor_radius, color='blue')
    ax.add_patch(sensor)

# Function to create Wi-Fi style waves (arcs expanding outward)
def draw_wave(ax, center, max_radius, color,angle, num_arcs=5, frame=0, ):
    """Draws concentric arcs """
    arc_radius = (frame / num_arcs) * max_radius  # Increasing arc radius
    alpha = 0.2 + (frame / num_arcs) * 0.4  # Gradual transparency
    arc = Arc(center, arc_radius * 2, arc_radius * 2, angle=angle, theta1=0, theta2=180, color=color, alpha=alpha, lw=2)
    ax.add_patch(arc)

# Define colors for the waves (using different colors for each sensor)
wave_colors = ['cyan', 'magenta', 'yellow', 'green', 'blue', 'orange', 'purple', 'red']

# Maximum wave radius and number of frames in the animation
max_wave_radius = 0.3  # Maximum radius for waves
num_frames = 30  # Number of frames for the animation

# Function to calculate the angle for each sensor's wave direction
def calculate_angle(sensor_pos):
    """Calculate the angle from sensor to the edge of the rectangle to direct the wave."""
    # Find the direction to the closest edge (outward)
    x, y = sensor_pos
    if x <= 0.25:  # Left of the rectangle
        return 90
    elif x >= 0.25 + rectangle_width:  # Right of the rectangle
        return -90
    elif y <= 0.1:  # Below the rectangle
        return 180
    elif y > 0.1 + rectangle_height:  # Above the rectangle
        return 0
    elif x == 0.45 and y == 0.25:
        return 180

    return 0  # Default direction if no clear outward direction

# Function to update the plot for each frame of the animation
def update(frame):
    ax.clear()  # Clear the current axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.add_patch(rect)  # Redraw the rectangle

    # Draw the ultrasonic sensors (repositioning them each frame)
    for pos in sensor_positions.values():
        sensor = Circle(pos, sensor_radius, color='blue')
        ax.add_patch(sensor)

    # Draw the Wi-Fi style waves from each sensor position
    for i, (sensor, pos) in enumerate(sensor_positions.items()):
        print(i,pos)
        angle = calculate_angle(pos)  # Calculate the outward angle
        # print(angle)
        draw_wave(ax, pos, max_wave_radius, wave_colors[i], num_arcs=num_frames, frame=frame, angle=angle)

# Create the animation
ani = FuncAnimation(fig, update, frames=num_frames, interval=100, repeat=True)

# Display the animation
plt.show()
