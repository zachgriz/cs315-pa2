
from sys import maxsize
import pandas as pd
import functools
from functools import *
import math
from math import *
import itertools
from itertools import count
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class User:
    def __init__(self, rate):
        self.id = rate.userId        
        self.ratings = []
        self.addRating(rate)

    def addRating(self, rating):
        self.ratings.append(rating)

class Rating:
    _ids = count(0)
    def __init__(self, userId, movieId, rating):
        self.id = next(self._ids)
        self.userId = userId
        self.movieId = movieId
        self.rating = rating

class Movie:
    def __init__(self, id, title, genre):
        self.id = id
        self.title = title
        self.genre = genre
        self.ratings = []
        self.pairs = []
        self.neighbors = []
    
    def addRating(self, rating):
        self.ratings.append(rating)

    def addPair(self, pair):
        self.pairs.append(pair)

    def getNeighbors(self):
        self.pairs.sort(key= lambda x: x.simScore, reverse=True)
        top = self.pairs[:5]
        for pair in top:
            if pair.movie1.id == self.id:
                self.neighbors.append(pair.movie2)
            else:
                self.neighbors.append(pair.movie1)

        return self.neighbors

    def __str__(self):
        return "<" + str(self.id)+ ", " + self.title + ", " + self.genre + ">"

class MoviePair:
    def __init__(self, movie1, movie2):
        self.movie1 = movie1
        self.movie2 = movie2
        self.simScore = 0
        self.getSim()

    def getSim(self):
        if len(self.movie1.ratings) == 0 or len(self.movie2.ratings) == 0:
            self.simScore = 0
            return
        mean1 = sum(x.rating for x in self.movie1.ratings) / len(self.movie1.ratings)
        mean2 = sum(x.rating for x in self.movie2.ratings) / len(self.movie2.ratings)

        normal1 = np.array(list(map(lambda a: a.rating - mean1, self.movie1.ratings)))
        normal2 = np.array(list(map(lambda a: a.rating - mean2, self.movie2.ratings)))

        maxsize = max(normal1.size, normal2.size)

        fit1 = np.resize(normal1, maxsize)
        fit2 = np.resize(normal2, maxsize)

        self.simScore = cosine_similarity([fit1], [fit2])[0][0]

        # minsize = min(len(normal1), len(normal2))

        # dp=0
        # for i in range(minsize):
        #     dp += (normal1[i] * normal2[i])

        # abs1 = 0
        # for i in range(len(normal1)):
        #     abs1 += pow(normal1[i],2)
        
        # abs1 = sqrt(abs1)

        # abs2 = 0
        # for i in range(len(normal2)):
        #     abs2 += pow(normal2[i],2)
        
        # abs2 = sqrt(abs2)

        # if dp == 0:
        #     self.simScore = 0
        # else:
        #     self.simScore = dp / (abs1 * abs2)
            
ratingCount = 0
currentUser = 0

ratingFile = open("./movie-lens-data/ratings.csv", 'r')
movieFile = open("./movie-lens-data/movies.csv", 'r')
movies = {}
ratings = []
users = []
pairs = []

next(movieFile)
for line in movieFile:
    data = line.split(",")
    movies[int(data[0])] = Movie(int(data[0]), data[1], data[2].strip())

movieFile.close()

next(ratingFile)
for line in ratingFile:
    data = line.split(",")
    rate = Rating(int(data[0]),int(data[1]), float(data[2]))
    ratings.append(rate)
    movie = movies[rate.movieId]
    movie.addRating(rate)
    if rate.userId == currentUser:
        users[currentUser-1].addRating(rate)
    else:
        users.append(User(rate))
        currentUser +=1

ratingFile.close()

pairs = list(itertools.combinations(movies.items(), 2))

for pair in pairs[:10000]:

    movie1 = pair[0][1]
    movie2 = pair[1][1]
    mpair = MoviePair(movie1, movie2)
    movie1.addPair(mpair)
    movie2.addPair(mpair)

print(movies[1].getNeighbors())