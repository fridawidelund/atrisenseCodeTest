# atrisenseCodeTest

struct AtrisenseRecord {
uint32_t scan_number;
float x_angle_deg;
float y_angle_deg;
float distance_m;
uint16_t intensity;
};

Your task is to:

1. Decode the Atrisense binary into structured records.
2. Convert each record into Cartesian coordinates (x, y, z).
3. (Optional) Visualize the resulting point cloud in any tool you prefer (foxglove, other point cloud viewers).

Please ensure the solution is ready for production.
Solution can be made in either C++ or Python.
When done, please send us a link to the git repo/Pull reqeust or mail us the source code so we can invite you for a technical discussion.

The atrisense.bin file was added to the repository for convenience. I dont usually commit data to a git repo :D
