from numba import jit


def get_tag_occurances(slideshow):
    tags = dict()

    for slide in slideshow:
        for tag in slide.tags:
            tags.setdefault(tag, 0)
            tags[tag] += 1

    return tags


def heuristic_score(slide, tags, slideshow_size):
    h1, h2, h3 = 0, 0, 0
    for tag in slide.tags:
        h1 += tags.get(tag) / slideshow_size
        h2 += (1 - tags.get(tag)) / slideshow_size

    # for tag in set(tags.keys()).difference(slide.tags):
    #     h3 += tags.get(tag) / slideshow_size

    return min(h1, h2)
