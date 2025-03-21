from dateutil.relativedelta import relativedelta
from collections import namedtuple
from collections import Counter
from datetime import datetime
from copy import deepcopy
import requests
import csv

MOVIE_API_URL = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={!!!!}"
GENRE_API_URL = "https://api.themoviedb.org/3/genre/movie/list?language=en"
THE_MOVIE_DB_HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
}


class MoviesAPI:

    def __init__(self, amount_of_pages):
        self.__amount_of_pages = max(amount_of_pages, 1)
        self.__pages_of_movies = []
        self.__movie_request_handler(self.__amount_of_pages)

    def __movie_request_handler(self, amount_of_pages):
        for i in range(amount_of_pages):
            response = requests.get(f"{MOVIE_API_URL}&page={i + 1}", headers=THE_MOVIE_DB_HEADERS)
            self.__pages_of_movies.append(response.json())

    def get(self, limit, offset=0):
        movie_list = []
        clamped_limit = min(max(limit, 1), self.__amount_of_pages)
        clamped_offset = min(max(offset, 0), self.__amount_of_pages - 1)

        for i in range(clamped_limit):
            i += clamped_offset
            movie_list.append(self.__pages_of_movies[i])

        return movie_list

    def get_all_movies(self):
        all_movie_list = []
        for movie in self.__pages_of_movies:
            all_movie_list.extend(movie["results"])

        return all_movie_list

    def get_all_with_steps(self, start, end, step):
        return self.get_all_movies()[start:end:step]

    def get_most_popular_title_name(self):
        temp_movies_list = self.get_all_movies()
        temp_movies_list.sort(key=lambda movie: movie["popularity"], reverse=True)

        return temp_movies_list[0]["title"]

    def get_movies_with_keywords(self, keywords):
        return list(filter(lambda movie: any(keyword.lower() in movie["overview"].lower() for keyword in keywords),
                           self.get_all_movies()))

    def get_all_genre(self):
        return requests.get(f"{GENRE_API_URL}", headers=THE_MOVIE_DB_HEADERS).json()["genres"]

    def delete_movies_with_genres(self, genres):
        return list(filter(lambda movie: not any(x in genres for x in movie["genre_ids"]), self.get_all_movies()))

    def get_most_popular_genre_name(self, limit=0):
        all_genres__which_been_used = []
        clamped_limit = min(max(limit, 1), 200)

        for movies in self.get_all_movies():
            all_genres__which_been_used.extend(movies["genre_ids"])

        most_popular = Counter(all_genres__which_been_used).most_common(clamped_limit)

        return list(map(lambda elements: tuple([self.get_genres_name_by_id(elements[0]), elements[1]]), most_popular))

    def get_genres_name_by_id(self, genre_id):
        all_genres = self.get_all_genre()

        for genre_obj in all_genres:
            if genre_obj["id"] == genre_id:
                return genre_obj["name"]

        return "undefined"

    def get_grouped_movie_by_genre(self):
        all_genres = self.get_all_genre()
        all_movies = self.get_all_movies()

        grouped_movies = []

        for genre in all_genres:
            temp_all_movies_name = []
            for movie in all_movies:
                if genre["id"] in movie["genre_ids"]:
                    temp_all_movies_name.append(movie["title"])

            grouped_movies.append((genre["name"], temp_all_movies_name))

        return grouped_movies

    def change_first_genre_id_of_movies(self, initial_movies_list, id_for_change):
        copy = deepcopy(initial_movies_list)

        for movie in copy:
            movie["genre_ids"][0] = id_for_change

        return [
            initial_movies_list,
            copy,
        ]

    def get_structured_films(self):
        Movie = namedtuple("Movie", ["Title", "Popularity", "Score", "Last_day_in_cinema"])
        list_of_movies = []

        delta = relativedelta(months=2, days=14)

        for movie in self.get_all_movies():
            last_day_in_cinema = datetime.strptime(movie["release_date"], "%Y-%m-%d") + delta
            list_of_movies.append(
                Movie(Title=movie["title"], Popularity=movie["popularity"], Score=int(movie["vote_average"]),
                      Last_day_in_cinema=last_day_in_cinema.strftime("%Y-%m-%d")))

        return sorted(list_of_movies, key=lambda movies: (movies.Score, movies.Popularity), reverse=True)

    def write_structure_movies_data_in_csv(self, file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            movies_structured = self.get_structured_films()
            writer.writerow(["Title", "Popularity", "Score", "Last_day_in_cinema"])

            for movie in movies_structured:
                writer.writerow([movie.Title, movie.Popularity, movie.Score, movie.Last_day_in_cinema])
