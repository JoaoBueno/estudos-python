import imdb
ia = imdb.IMDb()
movies = ia.search_movie('matrix')
for m in movies:
    print(m)


keywords = ia.search_keyword('dystopia')
print(keywords)