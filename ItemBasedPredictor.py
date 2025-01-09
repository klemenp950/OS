from MovieData import MovieData
import pandas as pd

class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.__uid = None
        self.__min_values = min_values
        self.__threshold = threshold
        self.__all_movies_list = list()
        self.__relevant_movies = list()
    
    def fit(self, uim):
        self.__uid = uim
        self.__uuid = sorted(list(self.__uid.data['userID'].unique()))
        self.__umid = sorted(list(self.__uid.data['movieID'].unique()))
        # print(self.__umid)
        self.__matrix_ratings = [[None for _ in range(len(self.__umid))] for _ in range(len(self.__uuid))]
        
        for (_, (uid, mid, rating, _)) in self.__uid.data.iterrows():
            if(mid in self.__umid and uid in self.__uuid):
                self.__matrix_ratings[self.__uuid.index(uid)][self.__umid.index(mid)] = rating

        self.__df_matrix_ratings = pd.DataFrame(self.__matrix_ratings, columns=self.__umid, index=self.__uuid)
        self.__df_matrix_ratings.replace(0, pd.NA, inplace=True)

        self.__averages = list(self.__df_matrix_ratings.mean(axis=1, skipna=True))

        for i in range(len(self.__matrix_ratings)):
            for j in range(len(self.__matrix_ratings[i])):
                if self.__matrix_ratings[i][j]:
                    self.__matrix_ratings[i][j] = self.__matrix_ratings[i][j] - self.__averages[i]
        
        self.__similarity_matrix = [[0 for _ in range(len(self.__umid))] for _ in range(len(self.__umid))]

        for i in range(len(self.__umid)):
            for j in range(i, len(self.__umid)):
                if i == j:
                    self.__similarity_matrix[i][j] = 1
                else:
                    sim = self.__sim(i, j)
                    self.__similarity_matrix[i][j] = sim
                    self.__similarity_matrix[j][i] = sim

    def __sim(self, i1, i2):
        num = 0
        den1 = 0
        den2 = 0
        counter = 0

        for user_ratings in self.__matrix_ratings:
            if user_ratings[i1] and user_ratings[i2]:
                num += user_ratings[i1] * user_ratings[i2]
                den1 += user_ratings[i1] ** 2
                den2 += user_ratings[i2] ** 2
                counter += 1
        
        
        den = (den1 ** 0.5) * (den2 ** 0.5)
        return num / den if den != 0 and counter >= self.__min_values and num / den > self.__threshold else 0
    
    def similarity(self, i1, i2):
        return self.__similarity_matrix[self.__umid.index(i1)][self.__umid.index(i2)]
    
    def predict(self, userID, rec_seen=True):
        if self.__uid is None:
            raise ValueError("Error: fit() method was not called yet.")
        
        predictions = {}

        for j in range(len(self.__matrix_ratings[0])):
            if self.__matrix_ratings[self.__uuid.index(userID)][j] is None:
                num = 0
                den = 0
                for i in range(len(self.__matrix_ratings[0])):
                    if self.__matrix_ratings[self.__uuid.index(userID)][i]:
                        num += self.__similarity_matrix[j][i] * self.__matrix_ratings[self.__uuid.index(userID)][i]
                        den += self.__similarity_matrix[j][i]
                if den != 0:
                    predictions[self.__umid[j]] = (num / den) + self.__averages[self.__uuid.index(userID)]
        
        if rec_seen:
            for el in self.__umid:
                if self.__matrix_ratings[self.__uuid.index(userID)][self.__umid.index(el)]:
                    predictions[el] = self.__matrix_ratings[self.__uuid.index(userID)][self.__umid.index(el)]
        else:
            return predictions
        
    def get_n_most_similar_movies(self, n):
        return_dict = dict()
        for i in range(len(self.__similarity_matrix)):
            for j in range(i, len(self.__similarity_matrix[i])):
                if i != j:
                    return_dict[(self.__umid[i], self.__umid[j])] = self.__similarity_matrix[i][j]
        
        return dict(sorted(return_dict.items(), key=lambda x: x[1], reverse=True)[:n])