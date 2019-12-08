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

games=wide_ratings.index.values.tolist()

def recommend(userid):
    user_ratings_sql = """
        SELECT
                user_id,
                game_id,
                ROUND(AVG(rating)) rating
        FROM
                core.ratings
        WHERE
                user_id="""+str(userid)+"""
        GROUP BY
                user_id,
                game_id
    """
    user_ratings=sqlio.read_sql(user_ratings_sql, engine)

    user_profile=[0]*wide_ratings.shape[0]
    for index, row in user_ratings.iterrows():
        user_profile[games.index(row['game_id'])] = row['rating']
    user_profile_csr = scipy.sparse.csr_matrix(user_profile)

    user_rec = model.recommend(0, user_profile_csr, recalculate_user=True)
    user_recgames = []
    for tup in user_rec:
        user_recgames.append((games[tup[0]], tup[1]))

    return user_recgames

print(recommend(1))
print(recommend(2))


