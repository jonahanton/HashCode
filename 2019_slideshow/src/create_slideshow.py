from score import pair_score
from tqdm import tqdm


class CreateSlideshowNaive:
    def __init__(self, slides):
        self.slides = slides
        self.slideshow = []
        self.algoscore = 0

    def check_edges(self, slide):
        # Score front edge add
        frontscore = pair_score(self.slideshow[0], slide)

        # Score back edge add
        backscore = pair_score(self.slideshow[-1], slide)

        # Add slide to slideshow where most score
        if frontscore > backscore:
            return "f", frontscore
        else:
            return "b", backscore

    def add_to_edges(self):
        best_score = 0
        best_slide = None
        best_slide_loc = ""
        for slide in self.slides:
            loc, score = self.check_edges(slide)

            if score > best_score:
                best_score = score
                best_slide_loc = loc
                best_slide = slide

        # Quit early if no slide was found to add to score
        if not best_slide:
            return False

        # Add best score to total
        self.algoscore += best_score

        # Add slide to slideshow
        if best_slide_loc == "f":
            self.slideshow.insert(0, best_slide)
        else:
            self.slideshow.append(best_slide)

        # Remove slide from slides
        self.slides.remove(best_slide)

        # Keep on going
        return True

    def create(self):

        # Take initial random slide
        # Loop through all remaining slides and find best first pair
        slide = self.slides.pop()
        self.slideshow.append(slide)
        best_score = 0
        for other_slide in self.slides:
            score = pair_score(slide, other_slide)
            if score > best_score:
                next_slide = other_slide
        self.slideshow.append(next_slide)
        self.slides.remove(next_slide)

        go = True
        for i in tqdm(range(len(self.slides))):
            if go:
                go = self.add_to_edges()
            else:
                return self.slideshow, self.algoscore
