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
* [手順書](https://github.com/AraiKanta/jfa-data-project/blob/docker-setting/doc/Docker%E7%92%B0%E5%A2%83%E6%A7%8B%E7%AF%89%E3%81%8B%E3%82%89SQLite%E2%86%92MySQL%E7%A7%BB%E8%A1%8C%E6%89%8B%E9%A0%86%E6%9B%B8.md)
