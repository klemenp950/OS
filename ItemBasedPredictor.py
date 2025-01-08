from MovieData import MovieData

class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.__uim = None
        self.__min_values = min_values
        self.__threshold = threshold
        self.__list = None
    
    def fit(self, uim):
        self.__uim = uim
        self.__average_grades = [0] * uim.get_number_of_users()
        md = MovieData('data/movies.dat')
        self.__matrix = [[0] * md.nmovies() for _ in range(uim.get_number_of_users())]
        for (uid, mid, rating, _) in uim.data:
            self.__matrix[uid - 1][mid - 1] = rating
        
        for i in range(uim.get_number_of_users()):
            self.__average_grades[i] = sum(self.__matrix[i]) / self.count(self.__matrix[i])
        
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix[i])):
                if self.__matrix[i][j] != 0:
                    self.__matrix[i][j] = self.__matrix[i][j] - self.__average_grades[i]
        
        self.__similarity_matrix = [[0] * md.nmovies() for _ in range(md.nmovies())]

        for i in range(md.nmovies()):
            for j in range(i, md.nmovies()):
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

        for user_ratings in self.__matrix:
            if user_ratings[i1] != 0 and user_ratings[i2] != 0:
                num += user_ratings[i1] * user_ratings[i2]
                den1 += user_ratings[i1] ** 2
                den2 += user_ratings[i2] ** 2
        
        
        den = (den1 ** 0.5) * (den2 ** 0.5)
        return num / den if den != 0 else 0
    
    def similarity(self, i1, i2):
        return self.__similarity_matrix[i1][i2]

    @staticmethod
    def count(self, array):
        counter = 0
        for i in array:
            if i != 0:
                counter += 1
        return counter