# Django Poll Platform

## Запуск

```bash
docker-compose up --build -d
docker-compose exec web uv run python manage.py migrate
docker-compose exec web uv run python manage.py create_demo_data
```

## Доступ

- Главная: http://localhost:8000/
- Админка: http://localhost:8000/admin/ (admin/admin123)

## Остановка

```bash
docker-compose down
```