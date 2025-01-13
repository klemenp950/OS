import random
from MovieData import MovieData
class RandomPredictor:
    def __init__(self, min_rating, max_rating):
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.uim = None

    def fit(self, X):
        self.uim = X

    def predict(self, user_id, rec_seen=True):
        if self.uim is None:
            raise ValueError("Error: fit() method was not called yet.")
        
        ratings = dict()
        
        md = MovieData('data/movies.dat')

        for el in md.data:
            movie_id = int(el[0])
            if self.uim.get_rating(user_id, movie_id) is None:
                ratings[movie_id] = random.randint(self.min_rating, self.max_rating)
            elif rec_seen:
                ratings[movie_id] = self.uim.get_rating(user_id, movie_id)
        
        return ratings

