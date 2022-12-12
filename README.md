# Сервис конвертации видео в текст

## Запуск
```bash
# Создание образа
docker build -t vt_converter .

# Создание и запуск контейнераdocker run -d --name vt_converter_container -p 80:80 vt_converter
(start after shutdown/reboot/auto-run: docker run --restart always -d  -p 8080:8080 vt_converter)
```
### URLs сервиса

#### OpenAPI документация по endpoints
http://127.0.0.1/docs

#### ReDoc документация по endpoints
http://127.0.0.1/redoc
