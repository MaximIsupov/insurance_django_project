Инструкция для запуска:

docker-compose up

docker-compose run --rm web python manage.py migrate(вынес из контейнера)

docker-compose run --rm web python manage.py search_index --rebuild

добавлять отдельный контейнер на команду применить миграции - это не правильно Нужно либо вручную ее выполнять, либо в bash скрипт закладывать и подключать его в web контейнеру
-Исправил

пользователь добавил компанию, но не понятно как добавлять услуги, продукты
Услуги можно добавить на страничке пользователя, нажав на имя пользователя вверху. (Добавил новую ссылку, ведущую на страничку, в popup окне).

на сайте нет фильтров, одно из заданий было фильтры добавить Фильтры я добавил на страничку с поиском, Как дополнительные инструменты при глобальном поиске.
С SendGrid небольшие проблемы, аккаунт заморозили. Решу в ближайшее время.
