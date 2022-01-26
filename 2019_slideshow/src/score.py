def slideshow_score(slideshow):
    score = 0
    for i in range(len(slideshow) - 1):
        slide_1 = slideshow[i]
        slide_2 = slideshow[i + 1]
        score += pair_score(slide_1, slide_2)
    return score


def pair_score(slide_1, slide_2):
    tags_1 = slide_1.tags
    tags_2 = slide_2.tags
    x = len(tags_1.intersection(tags_2))
    y = len(tags_1.difference(tags_2))
    z = len(tags_2) - x
    score = min(x, y, z)
    return score


if __name__ == "__main__":
    pass
