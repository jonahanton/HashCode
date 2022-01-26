import re

image_string_re = re.compile(r"^(?P<orientation>\w)\s(?P<ntags>\d+)\s(?P<tags>[\w\s]+)$")

class Image:
    
    def __init__(self, image_string, id):
        self.id = id

        match = image_string_re.match(image_string)
        
        if match is None:
            raise ValueError("Image string didn't match")

        self.orientation = match.group("orientation")
        self.tags = set(match.group("tags").strip().split(" "))

    def __repr__(self):
        return f"Image({self.id}, '{self.orientation}', tags={self.tags})"