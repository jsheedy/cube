import numpy as np

from object3d import Object3D


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

        self.edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),

            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),

            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        )
        vertices = np.hstack([vertices/2, np.matrix(np.ones(vertices.shape[0])).T]).T

        self.vertices = vertices
