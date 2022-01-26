

class Slide:

    def __init__(self, images):

        self.images = images
        self.ids = set()
        self.tags = set()
        
        orientations = set()
        
        for image in self.images:
            self.ids.add(image.id)
            self.tags.update(image.tags)

            orientations.add(image.orientation)

        if len(orientations) > 1:
            raise ValueError("Multiple Orientations passed.")

        self.orientation = orientations.pop()

    def __repr__(self):
        return f"Slide(ids={self.ids}, tags={self.tags})"