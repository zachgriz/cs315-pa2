
import pandas as pd
import functools
from functools import *
import math
from math import *
from itertools import count



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
    
    def addRating(self, rating):
        self.ratings.append(rating)

    def __str__(self):
        return "<" + str(self.id)+ ", " + self.title + ", " + self.genre + ">"

class MoviePair:
    def __init__(self, movie1, movie2):
        self.movie1 = movie1
        self.movie2 = movie2
        self.simScore = self.getSim(self)

    def getSim(self):
        mean1 = reduce(lambda a, b: a.rating + b.rating, self.movie1.ratings) / len(self.movie1.ratings)
        mean2 = reduce(lambda a, b: a.rating + b.rating, self.movie2.ratings) / len(self.movie2.ratings)

        normal1 = list(map(lambda a: a.rating - mean1, self.movie1.ratings))
        normal2 = list(map(lambda a: a.rating - mean2, self.movie2.ratings))

        min = len(normal1) if len(normal1) < len(normal2) else len(normal2)

        dp=0
        for i in range(min):
            dp += (normal1[i] * normal2[i])

        abs1 = 0
        for i in range(len(normal1)):
            abs1 += pow(normal1[i],2)
        
        abs1 = sqrt(abs1)

        abs2 = 0
        for i in range(len(normal2)):
            abs2 += pow(normal2[i],2)
        
        abs2 = sqrt(abs2)

        return dp / (abs1 * abs2)
ratingCount = 0
currentUser = 0

ratingFile = open("./movie-lens-data/ratings.csv", 'r')
movieFile = open("./movie-lens-data/movies.csv", 'r')
movies = []
ratings = []
users = []

next(movieFile)
for line in movieFile:
    data = line.split(",")
    movies.append(Movie(int(data[0]), data[1], data[2].strip()))

movieFile.close()

next(ratingFile)
for line in ratingFile:
    data = line.split(",")
    rate = Rating(int(data[0]),int(data[1]), float(data[2]))
    ratings.append(rate)
    movies[int(rate.movieId)-1].addRating(rate)
# MOVIE ID DOES NOT EQUAL INDEX
#NEED TO FIND SOMEOTHER WAY
    if rate.userId == currentUser:
        users[currentUser-1].addRating(rate)
    else:
        users.append(User(rate))
        currentUser +=1
