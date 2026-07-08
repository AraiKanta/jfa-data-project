# CSVファイル読み込み用
import csv

# パス操作用
from pathlib import Path

# Djangoのカスタム管理コマンド基底クラス
from django.core.management.base import BaseCommand

# 取り込み対象モデル
from history.models import (
    Country,
    Competition,
    Match,
)


class Command(BaseCommand):
    """
    試合データ一括取込コマンド

    実行例:
        python manage.py import_matches

    取込対象:
        data/countries.csv
        data/competitions.csv
        data/matches.csv
    """

    # help は manage.py help 時に表示される
    help = "CSVから試合データを取り込み"

    def handle(self, *args, **options):
        """
        管理コマンド実行時に呼ばれるメイン処理

        処理順:
            1. 国マスタ取込
            2. 大会マスタ取込
            3. 試合データ取込
        """

        # CSV格納ディレクトリ
        base_dir = Path("data")

        # 国マスタ取り込み
        self.import_countries(
            base_dir / "countries.csv"
        )

        # 大会マスタ取り込み
        self.import_competitions(
            base_dir / "competitions.csv"
        )

        # 試合データ取り込み
        self.import_matches(
            base_dir / "matches.csv"
        )

        # 成功メッセージ表示
        self.stdout.write(
            self.style.SUCCESS("取込完了")
        )

    def import_countries(self, csv_path):
        """
        国マスタ取込

        CSV形式:
            id,name

        update_or_create を使用することで
        同じIDが存在する場合は更新、
        存在しない場合は新規登録する。
        """

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
        """
        大会マスタ取込

        CSV形式:
            id,name

        update_or_create により
        重複登録を防止する。
        """

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
        """
        試合データ取込

        CSV形式:

            id
            match_date
            country_id
            competition_id
            score_japan
            score_opponent
            goal_scorers
            yellow_cards
            red_cards
            venue

        外部キー:

            country_id
                ↓
            Country

            competition_id
                ↓
            Competition
        """

        with open(
            csv_path,
            encoding="utf-8-sig"
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                # 外部キーとなる国データ取得
                country = Country.objects.get(
                    id=row["country_id"]
                )

                # 外部キーとなる大会データ取得
                competition = Competition.objects.get(
                    id=row["competition_id"]
                )

                # 試合データ登録
                #
                # update_or_create を利用するため
                # 既存データは更新、
                # 存在しない場合は新規作成される
                Match.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        # 試合日
                        "match_date": row["match_date"],

                        # 対戦国
                        "country": country,

                        # 大会
                        "competition": competition,

                        # 得点

                        "score_japan": int(float(row["score_japan"])),
                        "score_opponent": int(float(row["score_opponent"])),


                        # 詳細情報
                        "goal_scorers": row["goal_scorers"],
                        "yellow_cards": row["yellow_cards"],
                        "red_cards": row["red_cards"],
                        "venue": row["venue"],
                    },
                )