from slide import Slide


def all_vertical(photo_set):
    slides = set()
    for photo1 in photo_set:
        for photo2 in photo_set:
            if photo1 == photo2:
                continue
            slides.add(Slide([photo1, photo2]))
    return slides
