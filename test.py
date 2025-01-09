from UserItemData import UserItemData
import pandas as pd

uid = UserItemData('data/user_ratedmovies.dat')
# pd.set_option('display.max_rows', None)
for (_, (uid, mid, _, _)) in uid.data.iterrows():
    print(uid, mid)