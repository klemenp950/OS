class SlopeOnePredictor:
    def __init__(self):
        self.__uid = None
        self.__dev_matrix = None
        self.__uuid = None
        self.__umid = None
        self.__matrix_ratings = None
        self.__rated_both = None
    
    def fit(self, uid):
        self.__uid = uid
        self.__uuid = sorted(list(self.__uid.data['userID'].unique()))
        self.__umid = sorted(list(self.__uid.data['movieID'].unique()))

        self.__matrix_ratings = [[None for _ in range(len(self.__umid))] for _ in range(len(self.__uuid))]
        self.__rated_both = [[None for _ in range(len(self.__umid))] for _ in range(len(self.__umid))]
        
        for (_, (uid, mid, rating, _)) in self.__uid.data.iterrows():
            if(mid in self.__umid and uid in self.__uuid):
                self.__matrix_ratings[self.__uuid.index(uid)][self.__umid.index(mid)] = rating
        
        self.__dev_matrix = [[0 for _ in range(len(self.__umid))] for _ in range(len(self.__umid))]
        for i in range(len(self.__umid)):
            for j in range(i, len(self.__umid)):
                if i == j:
                    self.__dev_matrix[i][j] = 0
                else:
                    dev = self.__dev(i, j)
                    self.__dev_matrix[i][j] = dev[0]
                    self.__dev_matrix[j][i] = 0 - dev[0]
                    self.__rated_both[i][j] = dev[1]
                    self.__rated_both[j][i] = dev[1]
    
    def __dev(self, i, j):
        num = 0
        den = 0

        for u in range(len(self.__uuid)):
            if(self.__matrix_ratings[u][i] and self.__matrix_ratings[u][j]):
                num += (self.__matrix_ratings[u][i] - self.__matrix_ratings[u][j])
                den += 1
        
        return ((num/den), den) if den > 0 else (0, den)
            
    
    def predict(self, userID, rec_seen=True):
        predictions = {}
        for el in range(len(self.__umid)):
            if self.__matrix_ratings[self.__uuid.index(userID)][el] == None:
                predictions[self.__umid[el]] = self.__get_prediction(userID, el)
            elif rec_seen:
                predictions[self.__umid[el]] = self.__matrix_ratings[self.__uuid.index(userID)][el]
        return predictions

    def __get_prediction(self, userID, i):
        num = 0
        dev = 0
        for j in range(len(self.__umid)):
            if self.__matrix_ratings[self.__uuid.index(userID)][j]:
                num += (self.__dev(i, j)[0] + self.__matrix_ratings[self.__uuid.index(userID)][j]) * self.__rated_both[i][j]
                dev += self.__rated_both[i][j]
        
        return num / dev if dev > 0 else 0