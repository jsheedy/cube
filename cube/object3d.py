from datetime import datetime

from transformations import rotation_matrix, scale_matrix, translation_matrix
from vector import Vector3


class Object3D:
    vertices = None
    edges = None

    def __init__(self, position=None, angular_velocity=None, velocity=None, scale=None, rotation=None):
        self.position = position or Vector3()
        self.scale = scale or Vector3.unity()
        self.rotation = rotation or Vector3()
        self.update_time = datetime.now()
        self.velocity = velocity
        self.angular_velocity = angular_velocity

    def update(self):
        self.update_physics()

    def update_physics(self):
        if not self.velocity:
            return
        t1 = datetime.now()
        time_dot_delta_time = (t1 - self.update_time).total_seconds()
        self.update_time = t1
        self.position += self.velocity * time_dot_delta_time
        # FIXME: implement angular velocity
        # self.rotation += self.angular_velocity * time_dot_delta_time

    @property
    def T(self):
        return translation_matrix(self.position)

    @property
    def R(self):
        return rotation_matrix(self.rotation)

    @property
    def S(self):
        return scale_matrix(self.scale)

    @property
    def transformed_vertices(self):
        return self.vertices
        # return self.T * self.R * self.vertices
        # return self.T * self.R * self.S * self.vertices