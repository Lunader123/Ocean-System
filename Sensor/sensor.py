class Sensor:
    def __init__(self, energy_consumption):
        self.energy_consumption = energy_consumption

    def detect_depth(self):
        raise NotImplementedError("Subclasses must implement detect_depth")


class SonarSensor(Sensor):
    def __init__(self, energy_consumption, detection_range):
        super().__init__(energy_consumption)
        self.detection_range = detection_range

    def detect_depth(self):
        # Simulate sonar depth detection logic
        detected_depth = 50  # Replace with actual sonar detection logic
        self.energy_consumed += self.energy_consumption
        return detected_depth


class DepthCameraSensor(Sensor):
    def __init__(self, energy_consumption, detection_range):
        super().__init__(energy_consumption)
        self.detection_range = detection_range

    def detect_depth(self):
        # Simulate depth camera detection logic
        detected_depth = 20  # Replace with actual depth camera detection logic
        self.energy_consumed += self.energy_consumption
        return detected_depth