# Djangoショートカット関数
# render            : テンプレートを表示
# get_object_or_404 : データが存在しない場合に404エラーを返す
from django.shortcuts import render, get_object_or_404

# モデルを読み込む
from .models import Match, Country, Competition


# =====================================
# トップページ
# =====================================
def top(request):
    """
    トップページを表示する

    URL例:
        /

    テンプレート:
        history/top.html
    """

    return render(
        request,
        'history/top.html'
    )


# =====================================
# 年別検索
# =====================================
def year_search(request):
    """
    年度ごとの試合検索

    URL例:
        /year_search/
        /year_search/?year=2024

    処理内容:
        1. 試合データから年一覧を取得
        2. GETパラメータから選択年を取得
        3. 指定年の試合を検索
        4. テンプレートへ渡す
    """

    # match_dateから年だけを重複なしで取得
    # order='DESC'なので新しい年順で取得
    years = (
        Match.objects
        .dates(
            'match_date',
            'year',
            order='DESC'
        )
    )

    # GETパラメータから選択年を取得
    # 例:
    #   ?year=2024
    selected_year = request.GET.get('year')

    # 初期状態は空のQuerySet
    matches = Match.objects.none()

    # 年が指定されている場合のみ検索
    if selected_year:

        matches = (
            Match.objects
            .filter(
                match_date__year=selected_year
            )
            .select_related(
                'country',
                'competition'
            )
        )

    # テンプレートへ渡すデータ
    context = {
        'years': years,
        'selected_year': selected_year,
        'matches': matches,
    }

    return render(
        request,
        'history/year_search.html',
        context,
    )


# =====================================
# 試合詳細
# =====================================
def match_detail(request, match_id):
    """
    試合詳細画面

    URL例:
        /matches/1001/

    match_idから1試合取得して表示する
    """

    # Matchを取得
    # 存在しない場合は404エラー
    match = get_object_or_404(
        Match.objects.select_related(
            'country',
            'competition'
        ),
        pk=match_id
    )

    # 戻るボタンで検索条件を維持するため
    # GETパラメータを取得
    year = request.GET.get('year')
    country_name = request.GET.get('country_name')
    competition_id = request.GET.get('competition')

    # テンプレートへ渡すデータ
    context = {
        'match': match,
        'year': year,
        'country_name': country_name,
        'competition_id': competition_id,
    }

    return render(
        request,
        'history/match_detail.html',
        context
    )


# =====================================
# 国別対戦成績
# =====================================
def country_record(request):
    """
    国別対戦成績検索

    URL例:
        /country_record/?country_name=ブラジル

    処理:
        1. 国名検索
        2. 該当国との試合一覧取得
        3. 勝敗数集計
        4. 得失点集計
    """

    # 検索キーワード
    keyword = request.GET.get(
        'country_name',
        ''
    )

    # 初期値
    country = None
    matches = Match.objects.none()

    # 勝敗カウント
    wins = 0
    draws = 0
    losses = 0

    # 得点集計
    goals_for = 0
    goals_against = 0

    if keyword:

        # 国名部分一致検索
        country = Country.objects.filter(
            name__icontains=keyword
        ).first()

        if country:

            # 指定国との試合取得
            matches = (
                Match.objects
                .filter(country=country)
                .select_related(
                    'competition',
                    'country'
                )
            )

            # 集計処理
            for match in matches:

                goals_for += match.score_japan
                goals_against += match.score_opponent

                # 勝利
                if match.score_japan > match.score_opponent:
                    wins += 1

                # 引分
                elif match.score_japan == match.score_opponent:
                    draws += 1

                # 敗戦
                else:
                    losses += 1

    # テンプレートへ渡すデータ
    context = {
        'keyword': keyword,
        'country': country,
        'matches': matches,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'goals_for': goals_for,
        'goals_against': goals_against,
    }

    return render(
        request,
        'history/country_record.html',
        context,
    )


# =====================================
# 大会別成績
# =====================================
def competition_record(request):
    """
    大会別成績検索

    URL例:
        /competition_record/?competition=3

    処理:
        1. 大会選択
        2. 該当試合取得
        3. 勝敗集計
        4. 得失点集計
        5. 勝率計算
    """

    # 大会一覧
    competitions = Competition.objects.all()

    # 選択された大会ID
    selected_competition_id = request.GET.get(
        'competition'
    )

    # 初期値
    competition = None
    matches = Match.objects.none()

    wins = 0
    draws = 0
    losses = 0

    goals_for = 0
    goals_against = 0

    if selected_competition_id:

        # 大会取得
        competition = Competition.objects.get(
            pk=selected_competition_id
        )

        # 該当大会の試合取得
        matches = (
            Match.objects
            .filter(
                competition=competition
            )
            .select_related(
                'country',
                'competition'
            )
        )

        # 集計処理
        for match in matches:

            goals_for += match.score_japan
            goals_against += match.score_opponent

            # 勝利
            if match.score_japan > match.score_opponent:
                wins += 1

            # 引分
            elif match.score_japan == match.score_opponent:
                draws += 1

            # 敗北
            else:
                losses += 1

    # 試合数
    total_matches = len(matches)

    # 勝率
    win_rate = 0

    if total_matches:
        win_rate = round(
            wins / total_matches * 100,
            1
        )

    # テンプレートへ渡すデータ
    context = {
        'competitions': competitions,
        'selected_competition_id': selected_competition_id,
        'competition': competition,
        'matches': matches,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'goals_for': goals_for,
        'goals_against': goals_against,
        'total_matches': total_matches,
        'win_rate': win_rate,
    }

    return render(
        request,
        'history/competition_record.html',
        context,
    )