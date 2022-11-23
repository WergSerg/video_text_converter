# Сервис конвертации видео в текст

## Запуск
```bash
# Создание образа
docker build -t vt_converter .

# Создание и запуск контейнера
docker run -d --name vt_converter_container -p 80:80 vt_converter
```
### URLs сервиса

#### OpenAPI документация по endpoints
http://127.0.0.1/docs

#### ReDoc документация по endpoints
http://127.0.0.1/redoc
