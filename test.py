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
print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items.items():
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))