import argparse
import pprint

from book import Book
from library import Library

class Solution:

    def __init__(self):

        self.books = {}
        self.libraries = {}


    def import_from_file(self, filepath):

        with open(filepath, "r") as infile:

            self.B, self.L, self.D = [int(x) for x in infile.readline().strip().split()]

            book_scores = [int(x) for x in infile.readline().strip().split()]
            for i, score in enumerate(book_scores):
                self.books[i] = Book(i, score)
            
            for i in range(self.L):

                N, T, M = [int(x) for x in infile.readline().strip().split()]
                lib = Library(i, T, M)
                ids = [int(x) for x in infile.readline().strip().split()]
                for id in ids:
                    lib.add_book(self.books[id])
                lib.update_value(self.D)
                self.libraries[i] = lib


    
    def run_simulation(self):

        # sort libraries by value
        libraries_to_sign_up = sorted(self.libraries.items(), key = lambda item: item[1].value, reverse=True)

        signed_up_libraries = []
        shipped_books = []
        sign_up_log = []
        
        T = 0
        while T < self.D:

            print(f"{T} / {self.D}")

            # if no libraries are in the process of being signed up
            if len(sign_up_log) == 0:
                # sign up highest value library that hasn't yet been signed up
                if len(libraries_to_sign_up) > 0:
                    library_to_sign_up = libraries_to_sign_up.pop(0)[1]
                    sign_up_log.append((library_to_sign_up, T))
            else:
                # check if library being signed up has finished its sign up process
                library, sign_up_time = sign_up_log[0]
                if T - sign_up_time >= library.T:
                    library.signed_up = True
                    signed_up_libraries.append(library)
            
            # ship books from all signed up libraries
            for library in signed_up_libraries:
                sorted_books = sorted(library.books, key = lambda x: x.score, reverse=True)
                count = 0
                while count < library.M:
                    if len(sorted_books) == 0:
                        break
                    book = sorted_books.pop(0)
                    if not book.shipped:
                        book.shipped = True
                        shipped_books.append(book)
                        count += 1
            
            T += 1
        

        total_score = 0
        for book in shipped_books:
            total_score += book.score
        
        return total_score

            
            
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str,
                         help="Input filepath containing .txt file containing data")
    args = parser.parse_args()
    filepath = args.filepath

    sol = Solution()
    sol.import_from_file(filepath)
    score = sol.run_simulation()
    print(f"Score: {score}")