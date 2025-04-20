import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Get current working directory
current_dir = os.getcwd()
# Define filename to be saved
filename = 'SNM_analysis3.png'
# Full path
full_path = os.path.join(current_dir, filename)

# 1. Read CSV files with headers, replace with your own files
df1 = pd.read_csv('SNM3.3.1.csv')  # First voltage sweep (VQ)
df2 = pd.read_csv('3.2.1.csv')  # Second voltage sweep (VQB)

# 2. Extract data and column names
x1, y1 = df1.iloc[:, 0].values, df1.iloc[:, 1].values  # VQ and VQB values from first sweep
x2, y2 = df2.iloc[:, 0].values, df2.iloc[:, 1].values  # VQ and VQB values from second sweep
x_label, y_label = df1.columns[0], df1.columns[1]  # Column headers

# Combine coordinates into point arrays
A_points = np.column_stack((x1, y1))  # Points from first sweep
B_points = np.column_stack((x2, y2))  # Points from second sweep

# Function to calculate perpendicular distance from point to line
def point_to_line_distance(point, line_point, slope):
    """
    Calculate perpendicular distance from point to line with given slope
    Line equation: y = slope*x + c (where c is derived from line_point)
    """
    x0, y0 = point
    x1, y1 = line_point
    c = y1 - slope * x1
    return np.abs(slope * x0 - y0 + c) / np.sqrt(slope ** 2 + 1)


# Main function to find points with maximum distance
def find_max_distance_points(A_points, B_points, slope=1):
    """
    For each point in A_points, find nearest point in B_points based on perpendicular distance
    to line with given slope, then return the pair with maximum Euclidean distance
    """
    nearest_B_points = []
    distances_to_nearest_B = []

    for A in A_points:
        min_distance = float('inf')
        nearest_B = None

        for B in B_points:
            distance = point_to_line_distance(B, A, slope=slope)
            if distance < min_distance:
                min_distance = distance
                nearest_B = B

        nearest_B_points.append(nearest_B)
        distance_AB = np.linalg.norm(A - nearest_B)  # Euclidean distance
        distances_to_nearest_B.append(distance_AB)

    # Find maximum distance pair
    max_idx = np.argmax(distances_to_nearest_B)
    return A_points[max_idx], nearest_B_points[max_idx]


# Find vertices
vertex_A, vertex_B = find_max_distance_points(A_points, B_points)

# Data smoothing function
def smooth_data(x, y, window_size=3):
    """
    Apply moving average smoothing to data
    window_size must be odd and smaller than half the data length
    """
    window_size = min(max(3, window_size), len(x) // 2)
    if window_size % 2 == 0:
        window_size -= 1

    pad = window_size // 2
    y_padded = np.pad(y, (pad, pad), mode='edge')
    kernel = np.ones(window_size) / window_size
    return np.convolve(y_padded, kernel, mode='valid')


# Create figure
plt.figure(figsize=(10, 10), dpi=100)

# Plot smoothed curves
y1_smooth = smooth_data(x1, y1, window_size=5)
plt.plot(x1, y1_smooth, color='darkblue', linewidth=2, label='VTC - VQ sweep (0V-1.2V)')

y2_smooth = smooth_data(x2, y2, window_size=5)
plt.plot(x2, y2_smooth, color='darkred', linewidth=2, label='VTC - VQB sweep (0V-1.2V)')


# Function to plot and annotate squares
def plot_square(vertex_A, vertex_B):
    """Plot square and return side length"""
    x1, y1 = vertex_A
    x2, y2 = vertex_B

    # Calculate square vertices
    rect_vertices = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    rect_x = [v[0] for v in rect_vertices] + [rect_vertices[0][0]]
    rect_y = [v[1] for v in rect_vertices] + [rect_vertices[0][1]]

    plt.plot(rect_x, rect_y, color='black', linestyle='-', linewidth=2)

    # Calculate square side length (average of width and height)
    square_length = (abs(x2 - x1) + abs(y2 - y1)) / 2

    # Add annotation
    plt.text((x1 + x2) / 2, (y1 + y2) / 2,
             f'Side length: \n {square_length:.4f}V',
             ha='center', va='center', fontsize=65*square_length,
            )

    return square_length


SNM = plot_square(vertex_A, vertex_B)  # Static Noise Margin

# Add SNM annotation
plt.text(1.0, 1.0, f'Static Noise Margin: \n {SNM:.4f}V',
         ha='center', va='center', fontsize=20,
         )

# Formatting
plt.xlabel('VQ (V)', fontsize=12)
plt.ylabel('VQB (V)', fontsize=12)
plt.title('SRAM Butterfly Curve with Static Noise Margin', fontsize=14)
plt.legend(fontsize=15, frameon=True, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)
plt.axis('equal')  # Maintain aspect ratio

plt.tight_layout()
# Save figure
plt.savefig(full_path, dpi=300, bbox_inches='tight')
print(f"image saved successfully at: {full_path}")
plt.show()