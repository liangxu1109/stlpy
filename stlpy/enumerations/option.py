from enum import Enum, unique

class RobustnessMetrics(Enum):
    AGM = "AGM"
    Standard = 'Traditional'
    def __str__(self):
        return self.value