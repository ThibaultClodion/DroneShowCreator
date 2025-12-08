import json
import struct

# We want little-endian because FS runs on x86 & we read memory directly
ENDIANNESS = "<"

class Vector3():

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
    
    def toJSON(self):
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def toBinary(self, stream):
        stream.write(struct.pack(ENDIANNESS+'fff', self.x, self.y, self.z))


class KeyFrame():

    def __init__(self, frame=0, position=Vector3(0.0, 0.0, 0.0), color=Vector3(0.0, 0.0, 0.0)):
        self.frame = frame
        self.position = position
        self.color = color

    def __eq__(self, other):
        return (self.position == other.position) and (self.color == other.color)

    def toJSON(self):
        return {
            "frame": self.frame,
            "position": self.position.toJSON(),
            "color": self.color.toJSON()
        }
    
    def toBinary(self, stream):
        stream.write(struct.pack(ENDIANNESS+'I', self.frame))
        self.position.toBinary(stream)
        self.color.toBinary(stream)

class Object():

    def __init__(self):
        self.nbKeyFrames = 0
        self.keyframes = []

    def addKeyFrame(self, keyframe):
        # Avoid duplicates
        if self.keyframes and keyframe == self.keyframes[-1]:
            return
        
        self.nbKeyFrames += 1
        self.keyframes.append(keyframe)

    def toJSON(self):
        return {
            "nbKeyFrames": self.nbKeyFrames,
            "keyframes": [kf.toJSON() for kf in self.keyframes]
        }
    
    def toBinary(self, stream):
        stream.write(struct.pack(ENDIANNESS+'I', self.nbKeyFrames))

        for kf in self.keyframes:
            kf.toBinary(stream)

class Objects():

    def __init__(self):
        self.fps = 0
        self.nbObjects = 0
        self.objects = []

    def addObject(self, object):
        self.nbObjects += 1
        self.objects.append(object)

    def toJSON(self):
        return {
            "fps": self.fps,
            "nbObjects": self.nbObjects,
            "objects": [obj.toJSON() for obj in self.objects]
        }
    
    def toBinary(self, stream):
        stream.write(struct.pack(ENDIANNESS+'II', self.fps, self.nbObjects))

        for obj in self.objects:
            obj.toBinary(stream)

    def saveToFile(self, filepath, filename, binary=False):
        if binary:
            if not filename.endswith(".bin"):
                filename += ".bin"

            with open(filepath + filename, 'wb') as f:
                self.toBinary(f)
        else:
            if not filename.endswith(".json"):
                filename += ".json"

            with open(filepath + filename, 'w') as f:
                json.dump(self.toJSON(), f, indent=4)