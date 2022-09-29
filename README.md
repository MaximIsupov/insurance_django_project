Инструкция для запуска:

docker-compose up

docker-compose run --rm web python manage.py migrate(вынес из контейнера)

docker-compose run --rm web python manage.py search_index --rebuild

