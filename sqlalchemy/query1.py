# coding=utf-8

# 1 - imports
from actor import Actor
from base import Session
from contact_details import ContactDetails
from movie import Movie

# 2 - extract a session
session = Session()

# 3 - extract all movies
movies = session.query(Movie).all()

# 4 - print movies' details
print('\n### All movies:')
for movie in movies:
    print(f'{movie.title} was released on {movie.release_date}')
print('')
