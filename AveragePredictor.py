from MovieData import MovieData
from UserItemData import UserItemData

class AveragePredictor:
    def __init__(self, b):
        self.__uim = None
        self.__b = b
    
    def fit(self, uim):
        self.__uim = uim
        self.__ratings = dict()
        global_sum_of_ratings = 0
        global_counter = 0
        movie_dict = dict()  # movie_id: (number_of_ratings, sum_of_ratings)
        md = MovieData('data/movies.dat')
        uid = UserItemData('data/user_ratedmovies.dat')

        for el in md.data:
            movie_id = int(el[0])

            sum_of_ratings = uid.get_sum_of_ratings(uid.data, movie_id)
            global_sum_of_ratings += sum_of_ratings
            number_of_ratings = uid.get_number_of_ratings(uid.data, movie_id)
            global_counter += number_of_ratings

            movie_dict[movie_id] = (number_of_ratings, sum_of_ratings)
        
        global_avg = float(global_sum_of_ratings / global_counter)
        for movie_id, (number_of_ratings, sum_of_ratings) in movie_dict.items():
                    self.__ratings[movie_id] = (sum_of_ratings + self.__b * global_avg) / (number_of_ratings + self.__b)

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