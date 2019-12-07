import implicit
import scipy
import pandas.io.sql as sqlio
from utilities import engine

sql_ratings = """
    SELECT
            user_id,
            game_id,
            ROUND(AVG(rating)) rating
    FROM
            core.ratings
    GROUP BY
            user_id,
            game_id
"""
ratings = sqlio.read_sql(sql_ratings, engine)
wide_ratings=ratings.pivot(index='game_id', columns='user_id', values='rating').fillna(0)

game_user_matrix=scipy.sparse.csr_matrix(wide_ratings)
user_game_matrix = game_user_matrix.T.tocsr()

model = implicit.als.AlternatingLeastSquares(factors=50)
model.fit(game_user_matrix)

all_recommendations=model.recommend_all(user_game_matrix)
print(all_recommendations)

all_recommendations_looped=[]
for user in range(0, wide_ratings.shape[1]):
    all_recommendations_looped.append(model.recommend(user, user_game_matrix))
print(all_recommendations_looped)

games=wide_ratings.index.values.tolist()

simtest=model.similar_items(games.index(5282))
simgames=[]
for tup in simtest:
    simgames.append(games[tup[0]])
    # TODO: use dictionary to map indices with ids!
print(simgames)
#Very good results! Similar games of GTA V based on ratings are:  GTA II, GTA IV, GTA San Andreas, GTA Vice City, ..., Read Dead Redemption, Skyrim

# sample user profile: GTA IV, GTA V and RDR 2
# game_ids 5279, 5282, 10158
sample_profile=[float(0)]*8951
sample_profile[games.index(5279)]=float(10)
sample_profile[games.index(5282)]=float(10)
sample_profile[games.index(10158)]=float(10)
sample_profile_csr=scipy.sparse.csr_matrix(sample_profile)
# sample user profile: Battlefield 1, Call of Duty: WWII and Tom Clancys Rainbow Six: Siege
# game_ids 1301, 2008, 13791
sample_profile_2=[float(0)]*8951
sample_profile_2[games.index(1301)]=float(10)
sample_profile_2[games.index(2008)]=float(10)
sample_profile_2[games.index(13791)]=float(10)
sample_profile_2_csr=scipy.sparse.csr_matrix(sample_profile_2)

rockstar_user_rec=model.recommend(0, sample_profile_csr, recalculate_user=True)
rockstar_recgames=[]
for tup in rockstar_user_rec:
    rockstar_recgames.append(games[tup[0]])
    #TODO: use dictionary to map indices with ids!
print(rockstar_recgames)

shooter_user_rec=model.recommend(0, sample_profile_2_csr, recalculate_user=True)
shooter_recgames=[]
for tup in shooter_user_rec:
    shooter_recgames.append(games[tup[0]])
    #TODO: use dictionary to map indices with ids!
print(shooter_recgames)


