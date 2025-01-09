import datetime
import pickle
import pandas as pd

class UserItemData:
    def __init__(self, path=None, pickle_path=None, start_date='1.1.0001', end_date='31.12.9999', min_ratings=0):
        if pickle_path:
            self.__path, self.__start_date, self.__end_date, self.__min_ratings, self.data = self.__load_from_db(pickle_path)
        else:
            self.__path = path
            self.__start_date = datetime.datetime.strptime(start_date, '%d.%m.%Y')
            self.__end_date = datetime.datetime.strptime(end_date, '%d.%m.%Y')
            self.__min_ratings = min_ratings
            self.data = self.__load_data()
        
    def __load_data(self):
        data = []
        try:
            with open(self.__path, 'r') as f:
                next(f)
                for line in f:
                    userID, movieID, rating, date_day, date_month, date_year, date_hour, date_minute, date_second = line.strip().split('\t')
                    date = datetime.datetime(int(date_year), int(date_month), int(date_day), int(date_hour), int(date_minute), int(date_second))
                    if self.__start_date <= date <= self.__end_date:
                        data.append([int(userID), int(movieID), float(rating), date])
            
            df = pd.DataFrame(data, columns=['userID', 'movieID', 'rating', 'date'])
            movie_counts = df['movieID'].value_counts()
            valid_movies = movie_counts[movie_counts >= self.__min_ratings].index
            df = df[df['movieID'].isin(valid_movies)]
            return df
        
        except FileNotFoundError:
            print('Error: File not found')
            return None
    
    def save_to_db(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    def __load_from_db(path):
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print('Error: File not found')
            return None
        except pickle.UnpicklingError:
            print('Error: Unpickling error')
            return None
    
    def get_rating(self, user_id, movie_id):
        rating = self.data[(self.data['userID'] == user_id) & (self.data['movieID'] == movie_id)]['rating']
        if rating.empty:
            return None
        return rating.values[0]
    
    def get_number_of_users(self):
        return len(self.data['userID'].unique())
    
    def nrating(self):
        return len(self.data)
    
    def get_sum_of_ratings(self, movie_id):
        movie_ratings = self.data.groupby('movieID')['rating'].sum()
        if movie_id in movie_ratings:
            return movie_ratings[movie_id]
        else:
            return 0
    
    def get_number_of_ratings(self, movie_id):
        movie_ratings_count = self.data.groupby('movieID')['rating'].count()
        if movie_id in movie_ratings_count:
            return movie_ratings_count[movie_id]
        else:
            return 0
    
    def get_avg_rating(self, movie_id):
        return self.get_sum_of_ratings(movie_id) / self.get_number_of_ratings(movie_id)