from enum import Enum, unique

class RobustnessMetrics(Enum):
    AGM = "AGM"
    Standard = 'Traditional'
    LSE = 'LSE'
    Smooth = 'Smooth'
    wSTL_Standard = 'wSTL_Standard'
    wSTL_AGM = 'wSTL_AGM'
    NewRobustness = 'NewRobustness'
    def __str__(self):
        return self.value