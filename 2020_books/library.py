class Library:

    def __init__(self, id, T, M, books=None):
        self.id = id
        self.T = T
        self.M = M
        if books is None:
            self.books = []
        self.signed_up = False
        self.value = 0

    
    def __repr__(self):
        return f"Library(id:{self.id}, signed_up:{self.signed_up}, value:{self.value}, books:{self.books})"

    
    def add_book(self, book):
        self.books.append(book)

    
    def sort_books(self):
        self.books.sort(key = lambda x: x.score, reverse=True)

    