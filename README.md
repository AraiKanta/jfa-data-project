# 実行手順
## 仮想環境を作る
```python -m venv myvenv```
## 仮想環境を起動する
```myvenv\Scripts\activate```
## Djangoのインストール
```pip install -r requirements.txt```
## サーバーを立ち上げる
```python manage.py runserver```
## アクセスする
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

# テスト編
## unitテスト&カバレッジ付き
```coverage run manage.py test```
## カバレッジ表示 
```coverage report```
