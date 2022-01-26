from structures.slide import Slide
from structures.image import Image


def max_vertical(photo_set):
    slides = set()
    photos_used = set()
    for photo1 in photo_set:
        max_tags = 0
        if photo1 in photos_used:
            continue
        for photo2 in photo_set:
            if photo2 in photos_used or photo2 == photo1:
                continue
            total_tags = photo1.tags.intersection(photo2.tags)
            if len(total_tags) > max_tags:
                max_tags = len(total_tags)
                slide = Slide({photo1, photo2})
        slides.add(slide)
        photos_used.update(slide.images)
    return slides


if __name__ == '__main__':
    filename = "data/c_memorable_moments.txt"
    with open(filename, 'r') as images_pointer:
        image_strings = images_pointer.readlines()[1:]

    vertical_images = set()
    slides = set()

    for id, image_string in enumerate(image_strings):
        image = Image(image_string.strip(), id)

        if image.orientation == "V":
            vertical_images.add(image)
        else:
            slide = Slide([image])
            slides.add(slide)

    # Add vertical slides to available slides
    slides.update(max_vertical(vertical_images))
    print(len(slides))
