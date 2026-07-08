# 日付データ生成用
from datetime import date

# Djangoテスト用クラス
from django.test import TestCase

# URL名からURLを生成する
from django.urls import reverse

# テスト対象モデル
from history.models import (
    Match,
    Country,
    Competition,
)


# =====================================
# トップページテスト
# =====================================
class TopViewTest(TestCase):
    """
    トップページ表示テスト
    """

    def test_top_page(self):
        """
        トップページへアクセスできることを確認
        """

        # GETリクエスト送信
        response = self.client.get(
            reverse('history:top')
        )

        # ステータスコード200確認
        self.assertEqual(
            response.status_code,
            200
        )

        # 使用テンプレート確認
        self.assertTemplateUsed(
            response,
            'history/top.html'
        )


# =====================================
# 年別検索テスト
# =====================================
class YearSearchTest(TestCase):
    """
    年別検索画面テスト
    """

    def setUp(self):
        """
        テスト用データ作成

        毎回テスト実行前に呼ばれる
        """

        country = Country.objects.create(
            id=1,
            name='ブラジル'
        )

        competition = Competition.objects.create(
            id=1,
            name='親善試合'
        )

        Match.objects.create(
            id=1,
            match_date=date(2024, 6, 1),
            country=country,
            competition=competition,
            score_japan=2,
            score_opponent=1,
        )

    def test_year_search(self):
        """
        2024年検索で1試合取得できることを確認
        """

        response = self.client.get(
            reverse('history:year_search'),
            {
                'year': 2024
            }
        )

        # 正常表示確認
        self.assertEqual(
            response.status_code,
            200
        )

        # 2024年データが1件返ることを確認
        self.assertEqual(
            len(response.context['matches']),
            1
        )


# =====================================
# 試合詳細テスト
# =====================================
class MatchDetailTest(TestCase):
    """
    試合詳細画面テスト
    """

    def setUp(self):
        """
        テストデータ作成
        """

        country = Country.objects.create(
            id=1,
            name='ブラジル'
        )

        competition = Competition.objects.create(
            id=1,
            name='親善試合'
        )

        self.match = Match.objects.create(
            id=1,
            match_date='2024-06-01',
            country=country,
            competition=competition,
            score_japan=2,
            score_opponent=1,
        )

    def test_match_detail(self):
        """
        指定試合を取得できることを確認
        """

        response = self.client.get(
            reverse(
                'history:match_detail',
                args=[self.match.id]
            )
        )

        # 正常表示確認
        self.assertEqual(
            response.status_code,
            200
        )

        # 詳細画面の試合ID確認
        self.assertEqual(
            response.context['match'].id,
            self.match.id
        )


# =====================================
# 国別対戦成績テスト
# =====================================
class CountryRecordTest(TestCase):
    """
    国別対戦成績画面テスト
    """

    def setUp(self):
        """
        ブラジルとの試合を2試合作成

        ・1勝
        ・1引分
        """

        country = Country.objects.create(
            id=1,
            name='ブラジル'
        )

        competition = Competition.objects.create(
            id=1,
            name='親善試合'
        )

        # 勝利試合
        Match.objects.create(
            match_date='2024-01-01',
            country=country,
            competition=competition,
            score_japan=2,
            score_opponent=0,
        )

        # 引分試合
        Match.objects.create(
            match_date='2024-02-01',
            country=country,
            competition=competition,
            score_japan=1,
            score_opponent=1,
        )

    def test_country_record(self):
        """
        国別成績集計確認
        """

        response = self.client.get(
            reverse('history:country_record'),
            {
                'country_name': 'ブラジル'
            }
        )

        # 勝利数確認
        self.assertEqual(
            response.context['wins'],
            1
        )

        # 引分数確認
        self.assertEqual(
            response.context['draws'],
            1
        )

        # 敗北数確認
        self.assertEqual(
            response.context['losses'],
            0
        )

        # 日本得点確認
        self.assertEqual(
            response.context['goals_for'],
            3
        )

        # 失点確認
        self.assertEqual(
            response.context['goals_against'],
            1
        )


# =====================================
# 大会別成績テスト
# =====================================
class CompetitionRecordTest(TestCase):
    """
    大会別成績画面テスト
    """

    def setUp(self):
        """
        テストデータ作成
        """

        country = Country.objects.create(
            id=1,
            name='ブラジル'
        )

        competition = Competition.objects.create(
            id=1,
            name='キリンチャレンジカップ'
        )

        Match.objects.create(
            match_date='2024-01-01',
            country=country,
            competition=competition,
            score_japan=3,
            score_opponent=1,
        )

    def test_competition_record(self):
        """
        大会別集計結果確認
        """

        response = self.client.get(
            reverse('history:competition_record'),
            {
                'competition': 1 #国際親善試合
            }
        )

        # 勝利数確認
        self.assertEqual(
            response.context['wins'],
            1
        )

        # 引分数確認
        self.assertEqual(
            response.context['draws'],
            0
        )

        # 敗北数確認
        self.assertEqual(
            response.context['losses'],
            0
        )

        # 勝率確認
        self.assertEqual(
            response.context['win_rate'],
            100.0
        )

        # 試合数確認
        self.assertEqual(
            response.context['total_matches'],
            1
        )