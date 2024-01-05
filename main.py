# main.py
from Sensor import SonarSensor, DepthCameraSensor
from Robot import Robot
from MAP import UnderwaterMap
from PathPlanning import complete_coverage_path_planning

def main():
    # Assuming you have an underwater map instance
    underwater_map = UnderwaterMap(width=5, height=5)

    sonar_sensor = SonarSensor(energy_consumption=5, detection_range=100)
    depth_camera_sensor = DepthCameraSensor(energy_consumption=2, detection_range=30)

    robot = Robot(underwater_map)

    # Example usage
    detected_depth_sonar = sonar_sensor.detect_depth()
    print(f"Sonar detected depth: {detected_depth_sonar}, Energy consumed: {sonar_sensor.energy_consumed}")

    detected_depth_camera = depth_camera_sensor.detect_depth()
    print(f"Depth Camera detected depth: {detected_depth_camera}, Energy consumed: {depth_camera_sensor.energy_consumed}")

    # Move the robot
    robot.move("up")

    # Sense the depth at the new position
    current_depth = robot.sense()
    print(f"Robot's current depth: {current_depth}")

    # Display the underwater map
    underwater_map.display_map()

    # Perform path planning and visualization
    complete_coverage_path_planning((0, 0), underwater_map)

if __name__ == "__main__":
    main()
