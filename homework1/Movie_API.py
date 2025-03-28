from dateutil.relativedelta import relativedelta
from collections import namedtuple
from collections import Counter
from dotenv import load_dotenv
from datetime import datetime
from itertools import chain
from copy import deepcopy
import requests
import csv
import os


load_dotenv()

GENERAL_DOMAIN = os.getenv("GENERAL_DOMAIN_MOVIE_API_URL")
MOVIE_API_URL = GENERAL_DOMAIN + os.getenv("MOVIE_API_URL")
GENRE_API_URL = GENERAL_DOMAIN + os.getenv("GENRE_API_URL")
THE_MOVIE_DB_HEADERS = {
    "accept": "application/json",
    "Authorization": os.getenv("MOVIE_API_TOKEN")
}

CSV_COLUM_NAMES = ["Title", "Popularity", "Score", "Last_day_in_cinema"]
DATA_FORMAT = "%Y-%m-%d"
DATE_DELTA = relativedelta(months=2, days=14)

Movie = namedtuple("Movie", ["title", "popularity", "score", "last_day_in_cinema"])


class Movie_API:

    def __init__(self, amount_of_pages):
        self.__amount_of_pages = max(amount_of_pages, 1)
        self.limit_on_page = 0
        self.__movies = []

    def initialize_movies(self):
        response_pages = []
        for i in range(self.__amount_of_pages):
            response = requests.get(f"{MOVIE_API_URL}&page={i + 1}", headers=THE_MOVIE_DB_HEADERS)
            response_pages.append(response.json())

        self.limit_on_page = len(response_pages[0]["results"])
        self.__movies = list(chain.from_iterable(movie["results"] for movie in response_pages))

    def get_movies_with_limit(self, limit, offset=0):
        movies_amount = self.__amount_of_pages * self.limit_on_page
        clamped_limit = min(max(limit, 1), movies_amount)
        clamped_offset = min(max(offset, 0), movies_amount - clamped_limit)

        return list(self.__movies[i] for i in range(offset - 1, clamped_limit + clamped_offset))

    @property
    def movies(self):
        return self.__movies

    def get_movies_by_step(self, start, end, step):
        return self.__movies[start:end:step]

    def get_most_popular_title_name(self):
        temp_movies_list = self.__movies
        temp_movies_list.sort(key=lambda movie: movie["popularity"], reverse=True)

        return temp_movies_list[0]["title"]

    def get_movies_with_keywords(self, keywords):
        return list(filter(lambda movie: any(keyword.lower() in movie["overview"].lower() for keyword in keywords),
                           self.__movies))

    @staticmethod
    def get_all_genre():
        return requests.get(GENRE_API_URL, headers=THE_MOVIE_DB_HEADERS).json()["genres"]

    def delete_movies_with_genres(self, genres):
        return list(filter(lambda movie: not any(x in genres for x in movie["genre_ids"]), self.__movies))

    def get_most_popular_genre_name(self, limit=0):
        clamped_limit = max(limit, 1)
        genres_used = list(chain.from_iterable(movies["genre_ids"] for movies in self.__movies))
        most_popular = Counter(genres_used).most_common(clamped_limit)

        return list(map(lambda elements: (self.get_genres_name_by_id(elements[0]), elements[1]), most_popular))

    def get_genres_name_by_id(self, genre_id):
        genres = [genre_obj["name"] for genre_obj in self.get_all_genre() if genre_obj["id"] == genre_id]
        return genres[0] if genres else "undefined"

    def get_grouped_movie_by_genre(self):
        return [(genre["id"], [movie["title"] for movie in self.__movies if genre["id"] in movie["genre_ids"]])
                for genre in self.get_all_genre()]

    def change_first_genre_for_each(self, id_for_change):
        copy = deepcopy(self.__movies)

        for movie in copy:
            movie["genre_ids"][0] = id_for_change

        return self.__movies, copy,

    @staticmethod
    def __form_movie(movie):
        last_day_in_cinema = datetime.strptime(movie["release_date"], DATA_FORMAT) + DATE_DELTA
        return Movie(
                    title=movie["title"],
                    popularity=movie["popularity"],
                    score=movie["vote_average"],
                    last_day_in_cinema=last_day_in_cinema.strftime(DATA_FORMAT)
                )

    def get_structured_films(self):
        list_of_movies = [self.__form_movie(movie) for movie in self.__movies]
        return sorted(list_of_movies, key=lambda movies: (movies.score, movies.popularity), reverse=True)

    def write_structure_movies_data_in_csv(self, file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            movies_structured = self.get_structured_films()
            writer.writerow(CSV_COLUM_NAMES)
            writer.writerows(movies_structured)
