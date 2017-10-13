
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