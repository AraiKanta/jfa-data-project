import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from history.models import (
    Country,
    Competition,
    Match,
)


class Command(BaseCommand):
    help = "CSVから試合データを取り込み"

    def handle(self, *args, **options):

        base_dir = Path("data")

        self.import_countries(
            base_dir / "countries.csv"
        )

        self.import_competitions(
            base_dir / "competitions.csv"
        )

        self.import_matches(
            base_dir / "matches.csv"
        )

        self.stdout.write(
            self.style.SUCCESS("取込完了")
        )

    def import_countries(self, csv_path):

        with open(
            csv_path,
            encoding="utf-8-sig"
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                Country.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "name": row["name"],
                    },
                )

    def import_competitions(self, csv_path):

        with open(
            csv_path,
            encoding="utf-8-sig"
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                Competition.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "name": row["name"],
                    },
                )

    def import_matches(self, csv_path):

        with open(
            csv_path,
            encoding="utf-8-sig"
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                country = Country.objects.get(
                    id=row["country_id"]
                )

                competition = Competition.objects.get(
                    id=row["competition_id"]
                )

                Match.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "match_date": row["match_date"],
                        "country": country,
                        "competition": competition,
                        "score_japan": row["score_japan"],
                        "score_opponent": row["score_opponent"],
                        "venue": row["venue"],
                    },
                )