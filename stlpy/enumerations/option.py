from enum import Enum, unique

class RobustnessMetrics(Enum):
    Standard = 'Traditional'
    AGM = "AGM"
    LSE = 'LSE'
    Smooth = 'Smooth'
    wSTL_Standard = 'wSTL_Standard'
    wSTL_AGM = 'wSTL_AGM'
    NewRobustness = 'NewRobustness'
    TimeRobustness = 'TimeRobustness'
    def __str__(self):
        return self.value