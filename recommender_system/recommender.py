import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the synthetic data
user_data = pd.read_csv('D:/Fashion-Recommender/users.csv')
item_data = pd.read_csv('D:/Fashion-Recommender/items.csv')
ratings_data = pd.read_csv('D:/Fashion-Recommender/ratings.csv')

# Aggregate duplicate entries by calculating the mean rating
ratings_data = ratings_data.groupby(['user_id', 'item_id'], as_index=False).mean()

# Pivot the ratings matrix
ratings_matrix = ratings_data.pivot(index='user_id', columns='item_id', values='rating').fillna(0)

# Compute the cosine similarity matrix
user_similarity = cosine_similarity(ratings_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=ratings_matrix.index, columns=ratings_matrix.index)

def predict_ratings(user_id):
    user_ratings = ratings_matrix.loc[user_id]
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)
    similar_users_ratings = ratings_matrix.loc[similar_users.index]
    weighted_ratings = similar_users_ratings.T.dot(similar_users) / similar_users.sum()
    return weighted_ratings
