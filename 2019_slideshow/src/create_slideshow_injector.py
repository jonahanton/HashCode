from score import pair_score
from heuristic import heuristic_score, get_tag_occurances
from numba import jit
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def score_slide_injection(next_slide, slideshow, slideshow_scores):
    inject_scores = ()

    # Score every possible position we can inject this slide
    # Score front edge add
    frontscore = pair_score(slideshow[0], next_slide)

    # Score back edge add
    backscore = pair_score(slideshow[-1], next_slide)

    # Get best of both
    if backscore > frontscore:
        best_score = backscore
        inject_loc = "back"
    else:
        best_score = frontscore
        inject_loc = "front"

    # Score injection adds
    for i in range(len(slideshow) - 1):
        # Calc scores for adding the slide between two
        inject_left_score = pair_score(slideshow[i], next_slide)
        inject_right_score = pair_score(slideshow[i + 1], next_slide)

        # Net increase in score is both minus original slideshow score
        score_increase = inject_left_score + inject_right_score - slideshow_scores[
            i]

        if score_increase > best_score:
            best_score = score_increase
            inject_scores = (inject_left_score, inject_right_score
                             )  # Save so we don't have to recalculate
            inject_loc = i

    return inject_loc, best_score, inject_scores


class CreateSlideshowInjector:
    def __init__(self, slides):
        self.slides = list(slides)
        self.slideshow = []
        self.algoscore = 0
        self.slideshow_scores = []

        # Tracking params
        self.injections = [0, 0]

    @jit()
    def inject_from_selection(self, selection):
        best_loc = None
        best_score = -1
        best_next_slide = None
        best_inject_scores = ()
        for next_slide in selection:
            iloc, score_increase, inject_scores = score_slide_injection(
                next_slide, self.slideshow, self.slideshow_scores)

            if score_increase > best_score:
                best_loc = iloc
                best_score = score_increase
                best_next_slide = next_slide
                best_inject_scores = inject_scores

        # Quit early
        if best_loc == None:
            print(best_next_slide)
            return False

        # Perform the injection
        if best_score > 0 or np.random.random() < 0.1:
            # Increase score
            self.algoscore += best_score

            if best_loc == "back":
                self.slideshow.append(best_next_slide)
                self.slideshow_scores.append(best_score)
                self.injections[0] += 1

            elif best_loc == "front":
                self.slideshow.insert(0, best_next_slide)
                self.slideshow_scores.insert(0, best_score)
                self.injections[0] += 1

            else:
                self.injections[1] += 1
                self.slideshow.insert(best_loc, best_next_slide)
                self.slideshow_scores[best_loc] = best_inject_scores[0]
                self.slideshow_scores.insert(best_loc, best_inject_scores[1])

        # Remove the injected slide
        self.slides.remove(best_next_slide)
        return True

    def create(self):
        tags = get_tag_occurances(self.slides)
        slideshow_size = len(self.slides)
        print("Sorting")
        self.slides.sort(
            key=lambda slide: heuristic_score(slide, tags, slideshow_size),
            reverse=True)
        print("Sorted")
        # Take initial random slide
        # Loop through all remaining slides and find best first pair
        slide = self.slides.pop(0)
        self.slideshow.append(slide)
        best_score = 0
        for other_slide in self.slides:
            score = pair_score(slide, other_slide)
            if score > best_score:
                next_slide = other_slide
                best_score = score

        self.algoscore += best_score
        self.slideshow_scores += [best_score]
        self.slideshow.append(next_slide)
        self.slides.remove(next_slide)

        pbar = tqdm(range(len(self.slides)))
        for i in pbar:
            go = self.inject_from_selection(
                self.slides[:min(10000, len(self.slides))])
            # print(len(self.slideshow), len(self.slides), self.algoscore)
            if not go:
                break

            if i % 100 == 0:
                pbar.set_description(
                    f"{len(self.slideshow)} {len(self.slides)} {self.algoscore}"
                )

        print(self.injections)
        print(self.algoscore)

        return self.slideshow, self.algoscore