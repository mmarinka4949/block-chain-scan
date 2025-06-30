# Privacy Analyzer

**Privacy Analyzer** — инструмент для оценки приватности Bitcoin-транзакции.

## Что делает

- Проверяет повторное использование адресов
- Анализирует входы на предмет input-clustering
- Обнаруживает равные выходы (output-splitting)
- Даёт базовую оценку приватности транзакции

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python privacy_analyzer.py <txid>
```

## Пример

```bash
python privacy_analyzer.py 4d1b6f...
```

## Применение

- Анализ анонимности пользователя
- Обнаружение слабых практик конфиденциальности
- Учебные цели

## Лицензия

MIT License
