import foxglove
import time
from datetime import datetime
from foxglove.channels import SceneUpdateChannel
from foxglove.schemas import (
    Color,
    SpherePrimitive,
    SceneEntity,
    SceneUpdate,
    Vector3,
    Pose,
)


def stream_points_to_foxglove(points):
    scene_channel = SceneUpdateChannel("/scene")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"output_{timestamp}.mcap"

    # Build one big list of point like spheres
    spheres = []
    for x, y, z in points:
        spheres.append(
            SpherePrimitive(
                pose=Pose(position=Vector3(x=x, y=y, z=z)),
                size=Vector3(x=0.01, y=0.01, z=0.01),
                color=Color(r=1.0, g=0.0, b=0.0, a=1.0)
            )
        )
    print(f"Created {len(spheres)} sphere primitives.")

    entity = SceneEntity(
        id="points",      # give it a fixed id
        frame_id="map",  # coordinate frame
        spheres=spheres,  # all spheres together
    )

    with foxglove.open_mcap(file_name):
        foxglove.start_server()
        time.sleep(5)
        scene_channel.log(
            SceneUpdate(
                entities=[entity]
            )
        )
        print("Sent all points — press Ctrl+C to exit")
        while True:
            pass