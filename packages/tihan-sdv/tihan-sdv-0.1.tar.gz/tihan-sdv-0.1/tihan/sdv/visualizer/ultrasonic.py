import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Circle
from matplotlib.animation import FuncAnimation
import numpy as np

class UltrasonicVisualizer:
    def __init__(self, **kwargs):
        self.distances = {f'distance_{i+1}': kwargs.get(f'distance_{i+1}', 0) for i in range(8)}

        # Create the figure and axis
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.title('Sensor Visualization')
        # Set axis limits and aspect ratio
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_aspect('equal')

        # ----------------------------rectangular arena--------------------------------
        # Plot the rectangle (arena)
        self.initial_x = 0.25
        self.initial_y = 0.25

        self.rectangle_width = 0.4
        self.rectangle_height = 0.6
        self.rect = Rectangle((self.initial_x, self.initial_y), width=self.rectangle_width, height=self.rectangle_height, edgecolor='red', facecolor='red', alpha=0.5)
        self.ax.add_patch(self.rect)

        # ----------------------------ultrasonic sensors--------------------------------
        # Define the positions for the 8 ultrasonic sensors
        self.sensor_positions = {
            'S1': (self.initial_x, self.initial_y),
            'S2': (self.initial_x + self.rectangle_width, self.initial_y),
            'S3': (self.initial_x,  self.initial_y + self.rectangle_height),
            'S4': (self.initial_x + self.rectangle_width, self.initial_y + self.rectangle_height),
            'S5': (self.initial_x + self.rectangle_width / 2, self.initial_y),
            'S6': (self.initial_x + self.rectangle_width / 2, self.initial_y + self.rectangle_height),
            'S7': (self.initial_x,  self.initial_y + self.rectangle_height / 2),
            'S8': (self.initial_x + self.rectangle_width, self.initial_y+ self.rectangle_height / 2)
        }
        # Plot the ultrasonic sensors (small circles)
        self.sensor_radius = 0.015
        for pos in self.sensor_positions.values():
            sensor = Circle(pos, self.sensor_radius, color='blue')  # Sensor color is blue
            self.ax.add_patch(sensor)                      # Add the sensor to the plot 

        # Define colors for the waves (using different colors for each sensor)
        self.wave_colors = ['cyan', 'magenta', 'yellow', 'green', 'blue', 'orange', 'purple', 'red']

        # Maximum wave radius and number of frames in the animation
        self.max_wave_radius = 0.3  # Maximum radius for waves
        self.num_frames = 30  # Number of frames for the animation

        # Create the animation
        self.ani = FuncAnimation(self.fig, self.update, frames=self.num_frames, interval=100, repeat=True)

        # Display the animation
        plt.show()

    # Function to create Wi-Fi style waves (arcs expanding outward)
    def draw_wave(self, ax, center, max_radius, color, angle, num_arcs=5, frame=0):
        """Draws concentric arcs """
        arc_radius = (frame / num_arcs) * max_radius  # Increasing arc radius
        alpha = 0.2 + (frame / num_arcs) * 0.4  # Gradual transparency
        arc = Arc(center, arc_radius * 2, arc_radius * 2, angle=angle, theta1=0, theta2=180, color=color, alpha=alpha, lw=2)
        ax.add_patch(arc)

    # Function to calculate the angle for each sensor's wave direction
    def calculate_angle(self, sensor_pos):
        """Calculate the angle from sensor to the edge of the rectangle to direct the wave."""
        # Find the direction to the closest edge (outward)
        x, y = sensor_pos
        if x <= 0.25:  # Left of the rectangle
            return 90
        elif x >= 0.25 + self.rectangle_width:  # Right of the rectangle
            return -90
        elif y <= 0.1:  # Below the rectangle
            return 180
        elif y > 0.1 + self.rectangle_height:  # Above the rectangle
            return 0
        elif x == 0.45 and y == 0.25:
            return 180

        return 0  # Default direction if no clear outward direction

    # Function to update the plot for each frame of the animation
    def update(self, frame):
        self.ax.clear()  # Clear the current axes
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_aspect('equal')
        self.ax.add_patch(self.rect)  # Redraw the rectangle

        # Draw the ultrasonic sensors (repositioning them each frame)
        for pos in self.sensor_positions.values():
            sensor = Circle(pos, self.sensor_radius, color='blue')
            self.ax.add_patch(sensor)

        # Draw the Wi-Fi style waves from each sensor position
        for i, (sensor, pos) in enumerate(self.sensor_positions.items()):
            distance_key = f'distance_{i+1}'
            distance = self.distances.get(distance_key, 0)
            wave_radius = min(distance / 100, self.max_wave_radius)  # Scale distance to wave radius
            angle = self.calculate_angle(pos)  # Calculate the outward angle
            self.draw_wave(self.ax, pos, wave_radius, self.wave_colors[i], num_arcs=self.num_frames, frame=frame, angle=angle)
