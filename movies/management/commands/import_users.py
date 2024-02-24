"""
このスクリプトは、MovieLensデータセットからユーザーデータをインポートするためのカスタム管理コマンドです。
使用方法: python manage.py import_users <path_to_u.user>
ここで、<path_to_u.user>は、u.userファイルの絶対パスまたは相対パスです。
"""

import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import User

class Command(BaseCommand):
    help = 'Imports users from the MovieLens dataset'

    def add_arguments(self, parser):
        parser.add_argument('data_file', type=str, help='Path to the u.user file containing the users data')

    @transaction.atomic
    def handle(self, *args, **options):
        data_file = options['data_file']
        with open(data_file, encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter='|')
            
            for row in reader:
                user_id = int(row[0])
                age = int(row[1])
                gender = row[2]
                occupation = row[3]
                zip_code = row[4]

                user, created = User.objects.get_or_create(
                    id=user_id,  # idフィールドを識別子として使用
                    defaults={
                        'age': age,
                        'gender': gender,
                        'occupation': occupation,
                        'zip_code': zip_code,
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'User {user.id} imported successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'User {user.id} already exists.'))
