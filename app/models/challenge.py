class Challenge:
    def __init__(self, id, coordinates, image_path, location_name=None, owner=None):
        self.id = id
        self.coordinates = coordinates
        self.image_path = image_path
        self.location_name = location_name
        self.owner = owner
