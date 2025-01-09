from UserItemData import UserItemData
from MovieData import MovieData
from RandomPredictor import RandomPredictor
from Recommender import Recommender
from AveragePredictor import AveragePredictor
from ViewsPredictor import ViewsPredictor
from ItemBasedPredictor import ItemBasedPredictor

md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1000)
print(uim.nrating())
rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)
dict = rp.get_n_most_similar_movies(20)
for (film1, film2), v in dict.items():
    print("Film1:", md.get_title(int(film1)) + ", Film2:", md.get_title(int(film2)) + ", Podobnost:", v)