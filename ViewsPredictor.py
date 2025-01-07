from MovieData import MovieData

class ViewsPredictor:
    def __init__(self):
        self.__uim = None
    
    def fit(self, uim):
        self.__uim = uim
        self.__ratings = dict()
        md = MovieData('data/movies.dat')
        for line in md.data:
            movie_id = int(line[0])
            self.__ratings[movie_id] = uim.get_number_of_ratings(uim.data, movie_id)
    
    def predict(self, user_id, rec_seen=True):
        if self.__uim is None:
            raise ValueError("Error: fit() method was not called yet.")
        
        
        predictions = {}
        user_rated_movies = set()

        if not rec_seen:
            for (uid, mid, _, _) in self.__uim.data:
                if uid == user_id:
                    user_rated_movies.add(mid)

        for movie_id, avg_rating in self.__ratings.items():
            if rec_seen or movie_id not in user_rated_movies:
                predictions[movie_id] = avg_rating

        return predictions