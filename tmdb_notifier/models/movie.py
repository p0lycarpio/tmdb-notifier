from tmdb_notifier.utils import readable_list

class Movie:
    def __init__(self, data: dict) -> None:
        self.id = data.get("id", int())
        self.title = data.get("title", "")
        self.original_title = data.get("original_title", "")
        self.year = int(data.get("release_date", int())[0:4])
        self.image = f"https://image.tmdb.org/t/p/w500{data.get('backdrop_path', '')}"
        self.overview = data.get("overview", "")
        self.poster = f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}"
        self.runtime = data.get("runtime", int())
        self.genres = readable_list([g.get("name") for g in data.get("genres", [])])
        self.languages = readable_list([l.get("iso_639_1") for l in data.get("spoken_languages", [])])
        self.original_language = data.get("original_language")
        self.url = f"https://www.themoviedb.org/movie/{self.id}"
        
    def set_credits(self, credits: dict) -> None:
        cast, crew = credits.get("cast", []), credits.get("crew", [])
        self.actors = readable_list([c.get("name") for c in cast])
        self.directors = readable_list([c.get("name") for c in crew  if c.get("job") == "Director"])
        self.writers = readable_list([c.get("name") for c in crew if c.get("job") == "Writer"])
        self.producers = readable_list([c.get("name") for c in crew if c.get("job") == "Producer"])
        self.composers = readable_list([c.get("name") for c in crew if c.get("job") == "Original Music Composer"])