import pandas as pd

movies = pd.read_csv("movie-lens-data/movies.csv")
links = pd.read_csv("movie-lens-data/links.csv")
ratings = pd.read_csv("movie-lens-data/ratings.csv")
tags = pd.read_csv("movie-lens-data/tags.csv")

df = pd.merge(ratings, movies, on="movieId")

movie_matrix = df.pivot_table(index='userId', columns='title', values='rating')

corr_matrix = movie_matrix.corr(method='pearson', min_periods = 50)