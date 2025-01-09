from MovieData import MovieData

class ViewsPredictor:
    def __init__(self):
        self.__uid = None
    
    def fit(self, uim):
        self.__uid = uim
        self.__ratings = dict()
        md = MovieData('data/movies.dat')
        for line in md.data:
            movie_id = int(line[0])
            self.__ratings[movie_id] = uim.get_number_of_ratings(movie_id)
    
    def predict(self, user_id, rec_seen=True):
        if self.__uid is None:
            raise ValueError("Error: fit() method was not called yet.")
        
        
        predictions = {}
        user_rated_movies = self.__uid.data[self.__uid.data['userID'] == user_id]['movieID'].unique()

        for movie_id, avg_rating in self.__ratings.items():
            if rec_seen or movie_id not in user_rated_movies:
                predictions[movie_id] = avg_rating

        return predictions