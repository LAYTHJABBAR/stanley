from .base import BaseRule
import math
from constants import MINIMUM_DISTANCE

class FollowRule(BaseRule):
    '''
    Rule to follow a detected person
    '''

    def isActive(self):
        return self.camera.closestDetection() != None

    def update(self):
        detection = self.camera.closestDetection()
        if detection == None:
            return

        xDistance = detection.x
        zDistance = detection.z - MINIMUM_DISTANCE
        heading = 0

        # enforce minimum distance where possible
        if detection.z < MINIMUM_DISTANCE:
            heading = self.headingChange(xDistance, MINIMUM_DISTANCE)
        else:
            heading = self.headingChange(xDistance, zDistance)

        self._targetPosition = (zDistance, xDistance)
        self._targetYaw = heading

    def headingChange(self, xDistance, zDistance):
        isLeftward = xDistance < 0

        changeRadians = math.atan(abs(xDistance) / zDistance)
        changeDegrees = math.degrees(changeRadians)

        return float((0.0 - changeDegrees) if isLeftward == True else changeDegrees)

    def reset(self):
        super().reset()

    def name(self) -> str:
        return 'follow'