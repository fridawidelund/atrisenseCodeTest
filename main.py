import time
import numpy as np
import matplotlib.pyplot as plt
from foxglove_streamer import stream_points_to_foxglove

def parse_and_convert_binary_data():
    with open("./atrisense.bin", "rb") as f:
        data = f.read()

    dt = np.dtype([('scan_number', '<u4'), ('x_angle_deg', '<f4'), ('y_angle_deg', '<f4'), 
                ('distance', '<f4'), ('intensity', '<u2')])
    raw_records = np.frombuffer(data, dtype=dt)

    # Vectorized cartesian conversion
    x_angles_rad = np.radians(raw_records['x_angle_deg'])
    y_angles_rad = np.radians(raw_records['y_angle_deg'])
    distances = raw_records['distance']

    x = distances * np.cos(y_angles_rad) * np.cos(x_angles_rad)
    y = distances * np.cos(y_angles_rad) * np.sin(x_angles_rad)
    z = distances * np.sin(y_angles_rad)

    points = np.stack([x, y, z], axis=1)
    return points

def plot_3d_points(points, num_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs, ys, zs = points[:num_points].T
    ax.scatter(xs, ys, zs)
    plt.show()

def main():
    start = time.perf_counter()
    points = parse_and_convert_binary_data()    
    end = time.perf_counter()
    print(f"Execution time: {(end - start)*1000:.3f} ms.")
    print(f"Parsed {len(points)} points.")
    print(points.shape)
    stream_points_to_foxglove(points)
    plot_3d_points(points, -1)

if __name__ == "__main__":
    main()