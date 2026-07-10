# ローカルにプロジェクトを直接クローンした場合の手順
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

# 環境構築後の実行確認
* F5のDebug実行で確認できます。
* <img width="247" height="470" alt="image" src="https://github.com/user-attachments/assets/bb50d118-b1f9-4031-9f83-ad4711db2512" />

# テスト編
## unitテスト&カバレッジ付き
```coverage run manage.py test```
## カバレッジ表示 
```coverage report```

# Dockerの環境構築について
