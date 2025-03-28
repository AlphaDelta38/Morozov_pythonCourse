from Movie_API import Movie_API


def main():
    movies_class = Movie_API(5)
    print(movies_class.initialize_movies())
    print(len(movies_class.movies))
    print(movies_class.get_grouped_movie_by_genre())
    movies_class.write_structure_movies_data_in_csv("./test.csv")



if __name__ == '__main__':
    main()
