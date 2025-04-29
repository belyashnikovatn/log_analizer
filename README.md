
# Django Log Analyzer CLI

CLI-приложение для анализа логов Django и генерации отчётов.

## Стек технологий
- Python 3.7+
- Модуль `argparse` для обработки аргументов командной строки
- Регулярные выражения для парсинга логов
- Тестирование с использованием `pytest`

## Установка зависимостей

Для установки всех зависимостей создайте виртуальное окружение и активируйте его:

```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/MacOS
source venv\Scripts\activate  # Для Windows
```
Затем установите зависимости:

```bash
pip install -r requirements.txt
```



## Запуск
После установки зависимостей, чтобы запустить приложение, используйте команду:
```bash
python main.py logs/app1.log logs/app2.log --report handlers
```

## Пример вывода

```bash
Total requests: 148

HANDLER              DEBUG  INFO  WARNING  ERROR  CRITICAL
/admin/dashboard/    1      12    0        0      0       
/admin/login/        0      12    0        0      0       
/api/v1/auth/login/  0      8     1        1      2       
/api/v1/cart/        0      8     1        0      0       
/api/v1/checkout/    0      14    0        1      0       
/api/v1/orders/      0      9     0        1      0       
/api/v1/payments/    0      9     0        2      1       
/api/v1/products/    0      9     1        1      1       
/api/v1/reviews/     0      20    0        0      0       
/api/v1/shipping/    0      7     0        1      0       
/api/v1/support/     0      16    0        0      0       
/api/v1/users/       0      8     0        0      1       
                     1      132   3        7      5
```


## Тесты
Для запуска тестов используйте команду
```bash
pytest --cov=.
```
Пример вывода:  

```bash
Name                               Stmts   Miss  Cover
------------------------------------------------------
log_analyzer\__init__.py               0      0   100%
log_analyzer\models.py                16      0   100%
log_analyzer\parser.py                25      0   100%
log_analyzer\reports\__init__.py       0      0   100%
log_analyzer\reports\handlers.py      39      0   100%
log_analyzer\utils.py                  9      0   100%
main.py                               35     11    69%
tests\test_handlers_report.py         81      0   100%
------------------------------------------------------
TOTAL                                205     11    95%
================= 13 passed in 0.50s ===============
```