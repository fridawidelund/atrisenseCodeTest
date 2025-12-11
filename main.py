import struct
import math
import matplotlib.pyplot as plt
from foxglove_streamer import stream_points_to_foxglove

def to_cartesian(x_angle_deg, y_angle_deg, distance_m):
    az = math.radians(x_angle_deg)
    el = math.radians(y_angle_deg)

    x = distance_m * math.cos(el) * math.cos(az)
    y = distance_m * math.cos(el) * math.sin(az)
    z = distance_m * math.sin(el)

    return x, y, z

def parse_and_convert_binary_data(file_path):
    record_format="<IfffH"
    record_size = struct.calcsize(record_format)
    records = []

    with open(file_path, "rb") as f:
        while chunk := f.read(record_size):
            if len(chunk) != record_size:
                print("Incomplete record found, stopping read.")
                break
            scan_number, x_angle, y_angle, distance, intensity = struct.unpack(record_format, chunk)
            x, y, z = to_cartesian(x_angle, y_angle, distance)
            records.append((scan_number, x_angle, y_angle, distance, intensity, x, y, z))

    return records

def plot_3d_points(points, num_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [p[0] for p in points[0:num_points]]
    ys = [p[1] for p in points[0:num_points]]
    zs = [p[2] for p in points[0:num_points]]

    ax.scatter(xs, ys, zs)
    plt.show()

def main():
    records = parse_and_convert_binary_data("./atrisense.bin") 
    points = [(r[-3:]) for r in records]
    plot_3d_points(points, -1)
    stream_points_to_foxglove(points)

if __name__ == "__main__":
    main()