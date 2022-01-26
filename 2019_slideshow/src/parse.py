from structures import Slide, Image
from create_slideshow import CreateSlideshowNaive
from output import output
from max_vertical import max_vertical


if __name__ == "__main__":
    # filename = "data/b_lovely_landscapes.txt"
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

    print("Slides in slideshow", len(slides))

    s = CreateSlideshowNaive(slides)
    slideshow, algoscore = s.create()

    output(slideshow, "Naive_B.txt")
    print("Algo Score", algoscore)
