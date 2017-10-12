from math import sin, cos
import numpy as np


class Quaternion:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @classmethod
    def zero(cls):
        return cls()


class Scene:
    def __init__(self):
        self.objects = dict()
        self.cameras = dict()
        self.main_camera = None

    def add_object(self, name, obj):
        self.objects[name] = obj


    def add_camera(self, name, camera):
        self.cameras[name] = camera
        self.main_camera = camera

def translation_matrix(t=None):
    t = t or Vector3()
    return np.matrix([
        [1, 0, 0, t.x],
        [0, 1, 0, t.y],
        [0, 0, 1, t.z],
        [0, 0, 0, 1]
    ], dtype=np.float64)


def rotation_matrix(rotation=None):
    r = rotation or Vector3()
    rot_x = np.matrix([
        [1, 0, 0, 0],
        [0, cos(r.x), -sin(r.x), 0],
        [0, sin(r.x), cos(r.x), 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

    rot_y = np.matrix([
        [cos(r.y), 0, -sin(r.y), 0],
        [0, 1, 0, 0],
        [-sin(r.y), 0, cos(r.y), 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

    rot_z = np.matrix([
        [cos(r.z), -sin(r.z), 0, 0],
        [sin(r.z), cos(r.z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

    return rot_z * rot_x * rot_y


class Vector3:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def unity(cls):
        return cls(1,1,1)


def scale_matrix(scale=None):

    s = scale or Vector3.unity()

    return np.matrix([
        [s.x, 0, 0, 0],
        [0, s.y, 0, 0],
        [0, 0, s.z, 0],
        [0, 0, 0, 1]
    ],dtype=np.float64)


class HUD:
    pass


class Object3D:
    vertices = None
    edges = None

    def __init__(self, position=None, scale=None, rotation=None):
        self.position = translation_matrix(position)
        self.scale = scale_matrix(scale)
        self.rotation = rotation_matrix(rotation)


class Camera(Object3D):
    pass


class Cube(Object3D):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vertices = np.matrix([
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, -1],

            [1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, 1]
        ], dtype=np.float64)

        vertices = np.hstack([vertices/2, np.matrix(np.ones(vertices.shape[0])).T]).T

        self.vertices = vertices

    @property
    def transformed_vertices(self):
        return self.position * self.rotation * self.scale * self.vertices