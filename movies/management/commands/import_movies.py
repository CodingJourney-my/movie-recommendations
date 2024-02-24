"""
このスクリプトは、MovieLensデータセットから映画データをインポートするためのカスタム管理コマンドです。
使用方法: python manage.py import_movies <path_to_u.item>
ここで、<path_to_u.item>は、u.itemファイルの絶対パスまたは相対パスです。
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import Movie, Genre
import csv
import datetime

class Command(BaseCommand):
    help = 'Imports movies and genres from the MovieLens dataset'

    def add_arguments(self, parser):
        parser.add_argument('data_file', type=str, help='Path to the u.item file containing the movies data')

    @transaction.atomic
    def handle(self, *args, **options):
        data_file = options['data_file']
        with open(data_file, encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter='|')
            
            for row in reader:
                movie_id = int(row[0])
                title = row[1]
                release_date_str = row[2]
                imdb_url = row[4]

                # 日付の解析
                release_date = None
                if release_date_str:
                    try:
                        release_date = datetime.datetime.strptime(release_date_str, '%d-%b-%Y').date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Release date format error for '{title}'"))

                movie, created = Movie.objects.get_or_create(
                    id=movie_id,
                    defaults={'title': title, 'release_date': release_date, 'imdb_url': imdb_url}
                )

                # ジャンルの処理
                genres = ['Unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 
                          'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 
                          'Thriller', 'War', 'Western']
                
                for i, genre_name in enumerate(genres):
                    is_genre = row[5+i] == '1'
                    if is_genre:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        movie.genres.add(genre)

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Movie '{title}' imported successfully."))
                else:
                    self.stdout.write(self.style.WARNING(f"Movie '{title}' already exists."))
