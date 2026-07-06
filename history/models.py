from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Country(models.Model):
    """対戦国マスタ（countries テーブル）"""

    name = models.CharField('国名', max_length=100, unique=True)

    class Meta:
        db_table = 'countries'
        ordering = ['name']
        verbose_name = '対戦国'
        verbose_name_plural = '対戦国'

    def __str__(self):
        return self.name


class Competition(models.Model):
    """大会マスタ（competitions テーブル）"""

    name = models.CharField('大会名', max_length=100, unique=True)

    class Meta:
        db_table = 'competitions'
        ordering = ['name']
        verbose_name = '大会'
        verbose_name_plural = '大会'

    def __str__(self):
        return self.name


class Match(models.Model):
    """試合結果（matches テーブル）"""

    class Result(models.TextChoices):
        WIN = 'win', '○ 勝'
        DRAW = 'draw', '△ 分'
        LOSS = 'loss', '● 負'

    match_date = models.DateField('試合日')
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name='matches',
        verbose_name='対戦国',
    )
    competition = models.ForeignKey(
        Competition,
        on_delete=models.PROTECT,
        related_name='matches',
        verbose_name='大会',
    )
    score_japan = models.PositiveIntegerField(
        '日本の得点',
        validators=[MinValueValidator(0)],
    )
    score_opponent = models.PositiveIntegerField(
        '相手の得点',
        validators=[MinValueValidator(0)],
    )
    venue = models.CharField('会場', max_length=200)

    class Meta:
        db_table = 'matches'
        ordering = ['-match_date']
        verbose_name = '試合'
        verbose_name_plural = '試合'

    def __str__(self):
        return (
            f'{self.match_date:%Y/%m/%d} '
            f'vs {self.country.name} '
            f'{self.score_japan}-{self.score_opponent}'
        )

    @property
    def result(self):
        if self.score_japan > self.score_opponent:
            return self.Result.WIN
        if self.score_japan == self.score_opponent:
            return self.Result.DRAW
        return self.Result.LOSS

    @property
    def result_symbol(self):
        return {
            self.Result.WIN: '○',
            self.Result.DRAW: '△',
            self.Result.LOSS: '●',
        }[self.result]

    def clean(self):
        super().clean()
        if self.score_japan is None or self.score_opponent is None:
            return
        if self.score_japan < 0 or self.score_opponent < 0:
            raise ValidationError('得点は0以上で入力してください。')
