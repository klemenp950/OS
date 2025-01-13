class MovieData:
    def __init__(self, path):
        self.__path = path
        self.data = self.__load_data()
    
    def __load_data(self):
        data = []
        with open(self.__path, 'r', encoding='ISO-8859-1') as f:
            next(f)
            for line in f:
                line = line.strip().split('\t')
                data.append(line)
        return data
    
    def nmovies(self):
        return len(self.data)

    def get_title(self, id):
        for line in self.data:
            if int(line[0]) == id:
                return line[1]
        return None

    def get_ids_and_titles(self):
        return [(int(line[0]), line[1]) for line in self.data]