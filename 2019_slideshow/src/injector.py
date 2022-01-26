from structures import Slide, Image
from create_slideshow_injector import CreateSlideshowInjector

if __name__ == "__main__":
    # filename = "data/b_lovely_landscapes.txt"
    filename = "data/c_memorable_moments.txt"
    # filename = "data/a_example.txt"
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

    # print(vertical_images)
    print("Slides in slideshow", len(slides))

    s = CreateSlideshowInjector(slides)
    slideshow, algoscore = s.create()

    print("Algo Score", algoscore)
    # print(slideshow)
