# Docker環境構築からSQLite→MySQLデータ移行までの手順書

## 対象

-   Django 5
-   Docker / Docker Compose
-   MySQL 8.4
-   Windows + VS Code

------------------------------------------------------------------------

# 1. 必要ソフト

-   Docker Desktop
-   Git
-   VS Code

Docker確認

``` bash
docker --version
docker compose version
```

------------------------------------------------------------------------

# 2. プロジェクト構成

    project/
    ├─ Dockerfile
    ├─ docker-compose.yml
    ├─ requirements.txt
    ├─ manage.py
    ├─ history/
    └─ mysite/

------------------------------------------------------------------------

# 3. requirements.txt

``` txt
Django~=5.2
mysqlclient
```

------------------------------------------------------------------------

# 4. Dockerfile

``` dockerfile
FROM python:3.14
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
```

------------------------------------------------------------------------

# 5. docker-compose.yml

``` yaml
services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.4
    restart: always
    environment:
      MYSQL_DATABASE: jfa_match_history
      MYSQL_USER: django
      MYSQL_PASSWORD: django
      MYSQL_ROOT_PASSWORD: root
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD","mysqladmin","ping","-h","localhost","-uroot","-proot"]
      interval: 10s
      timeout: 5s
      retries: 10

volumes:
  mysql_data:
```

------------------------------------------------------------------------

# 6. settings.py

``` python
ALLOWED_HOSTS=["localhost","127.0.0.1"]
```
```python
# ============================================
# データベース設定（MySQL）
# Docker Compose の db サービスへ接続する
# ============================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "jfa_match_history",
        "USER": "django",
        "PASSWORD": "django",
        "HOST": "db",          # docker-compose.yml のサービス名
        "PORT": "3306",
    }
}
```

DATABASESはMySQLへ設定。

------------------------------------------------------------------------

# 7. 起動

``` bash
docker compose up --build
```

確認

``` bash
docker compose ps
```

期待結果

-   db: healthy
-   web: Up

------------------------------------------------------------------------

# 8. Migration

確認

``` bash
docker compose exec web python manage.py showmigrations
```

実行

``` bash
docker compose exec web python manage.py migrate
```

------------------------------------------------------------------------

# 9. SQLiteからエクスポート

SQLite設定で

``` bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > data.json
```

UTF-8で保存。

------------------------------------------------------------------------

# 10. data.jsonをDockerプロジェクトへ配置

manage.pyと同じ階層へ配置。

------------------------------------------------------------------------

# 11. MySQLへ取込

``` bash
docker compose exec web python manage.py loaddata data.json
```

成功例

    Installed 1123 object(s) from 1 fixture(s)

------------------------------------------------------------------------

# 12. データ確認

``` bash
docker compose exec web python manage.py shell
```

``` python
from history.models import Match
Match.objects.count()
```

------------------------------------------------------------------------

# 13. ブラウザ確認

http://localhost:8000

------------------------------------------------------------------------

# よくあるエラー

## Invalid HTTP_HOST

ALLOWED_HOSTSへlocalhostを追加。

## Can't connect to server on 'db'

MySQL起動待ちのためhealthcheckとdepends_on(condition:
service_healthy)を設定。

## Migration未実施

``` bash
docker compose exec web python manage.py migrate
```

## UnicodeDecodeError

UTF-8のdata.jsonを使用。

------------------------------------------------------------------------

# 完了チェック

-   Docker起動成功
-   MySQL healthy
-   Migration完了
-   loaddata成功
-   データ件数一致
-   Web画面表示成功

以上でDocker環境構築からSQLite→MySQL移行まで完了。

# その他
| コマンド                        | 使うタイミング                                     |
| --------------------------- | ------------------------------------------- |
| `docker compose up`         | 既にビルド済みで、単に起動したいとき                          |
| `docker compose up --build` | Dockerfile や requirements.txt を変更したとき       |
| `docker compose down`       | コンテナを停止・削除したいとき                             |
| `docker compose down -v`    | コンテナとボリューム（MySQLデータ含む）を削除したいとき（データが消えるので注意） |

## メモ 
* docker compose up：既存のイメージを使ってコンテナを起動する。
* docker compose up --build：イメージを再ビルドしてからコンテナを起動する。
* 通常の開発では docker compose up を使い、Dockerfile や依存ライブラリを変更したときだけ --build を付けるのがおすすめです。
* Djangoの管理画面を開く場合、
```bash
docker compose exec web python manage.py createsuperuser
```
を打ってからアカウントを作成。ログインする。

参考資料
[Docker Compose CLI リファレンス:](https://docs.docker.com/reference/cli/docker/compose/up/) 
[Docker Compose の概要:](https://docs.docker.com/compose/)

