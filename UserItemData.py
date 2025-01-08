import datetime
import pickle

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
            
            if self.__min_ratings == 0:
                return data
            
            final_data = []
            for line in data:
                if self.get_number_of_ratings(data, line[1]) >= self.__min_ratings:
                    final_data.append(line)
            return final_data
        except FileNotFoundError:
            print('Error: File not found')
            return None
    
    def get_number_of_ratings(self ,data, movie_id):
        counter = 0
        for line in data:
            if line[1] == movie_id:
                counter += 1
        return counter
    
    def nrating(self):
        return len(self.data)
    
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
        for line in self.data:
            if line[0] == user_id and line[1] == movie_id:
                return line[2]
        return None

    def get_sum_of_ratings(self, data, movie_id):
        sum_of_ratings = 0
        for line in data:
            if line[1] == movie_id:
                sum_of_ratings += line[2]
        return sum_of_ratings
    
    def get_number_of_users(self):
        users = []
        for line in self.data:
            if line[0] not in users:
                users.append(line[0])
        return len(users)