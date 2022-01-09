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
    

    def update_value(self, D):
        self.value = 0
        for book in sorted(self.books, key = lambda x: x.score, reverse=True)[:D]:
            self.value += book.score

    