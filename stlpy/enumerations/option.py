from enum import Enum, unique

class RobustnessMetrics(Enum):
    AGM = "AGM"
    Standard = 'Traditional'
    Smooth = 'Smooth'
    wSTL = 'wSTL'
    NewRobustness = 'NewRobustness'
    def __str__(self):
        return self.value