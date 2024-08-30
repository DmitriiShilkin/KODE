## Тестовое задание от KODE Education (результат):
1. Спроектирован и реализован на Python сервис, предоставляющий REST API интерфейс с методами:
- `GET /kode/v1/note/` вывод списка заметок;
- `POST /kode/v1/note/` добавление заметки;
- `POST /kode/v1/user/` регистрация пользователя;
- `POST /kode/v1/login/` аутентификация и авторизация пользователя.
2. Данные хранятся в базе данных PostgreSQL.
3. Сервер работает через REST API, для передачи данных используется формат json. 
4. Web-сервер реализован на асинхронном web-фреймворке fastapi. 
5. В коде проставлены type hints.
6. Запуск сервиса и требуемой им инфраструктуры производится в докер-контейнерах.
7. Для проверки работоспособности методов API используются автоматизированные тесты.

### Отчет о тестировании
```
============================= test session starts ==============================
platform linux -- Python 3.11.8, pytest-8.3.2, pluggy-1.5.0 -- /usr/local/bin/python
rootdir: /app
configfile: pyproject.toml
plugins: asyncio-0.24.0, anyio-4.4.0
asyncio: mode=Mode.AUTO, default_loop_scope=None
collecting ... collected 3 items

src/tests/test_api/test_note.py::TestNoteApi::test_get_multi PASSED      [ 33%]
src/tests/test_api/test_note.py::TestNoteApi::test_create PASSED         [ 66%]
src/tests/test_api/test_user.py::TestUserApi::test_create_user PASSED    [100%]

======================== 3 passed, 10 warnings in 8.59s ========================
```
### Инструкция для запуска
1. Запустить сервис, выполнив в консоли linux из корневой папки команду `bash start.sh`.  
Дождаться надписи `Application startup complete.`
2. Проверить работу API, перейдя в браузере по адресу `http://127.0.0.1:8000/kode/docs/`.
3. Завершить работу сервиса, нажав клавиши `ctrl+c`.
4. Запустить тесты, выполнив в консоли linux из корневой папки команду `bash run_tests.sh`.

### Стек
- Python v3.11.8
- fastapi v0.112.2
- SQLAlchemy v2.0.32
- alembic v1.13.2
- pytest v8.3.2
- uvicorn v0.30.6
