# Fitness Tracker

Fitness Tracker — это приложение для мониторинга физической активности, которое позволяет пользователям отслеживать прогресс в достижении фитнес-целей, записывать данные о тренировках и делиться своими достижениями.

## Функциональные возможности:

- **Регистрация и авторизация пользователей**: Пользователи могут создать аккаунт, войти в систему и начать отслеживать свою активность.
- **Мониторинг активности**: Пользователи могут записывать количество шагов, калорий и других метрик.
- **Цели и достижения**: Устанавливайте фитнес-цели и отслеживайте их прогресс. Получайте достижения за выполнение целей.
- **Комментарии к достижениям**: Пользователи могут комментировать свои достижения и делиться прогрессом.
- **Прогресс и аналитика**: Получайте отчеты о своих достижениях, включая среднее количество шагов и калорий за неделю.
- **Рейтинг и лидерборд**: Сравнивайте свои результаты с другими пользователями.

## Установка

### 1. Клонируйте репозиторий

```bash
    git clone https://github.com/Brossend/fitness-tracker-pyqt.git
    cd fitness-tracker-pyqt
```
### 2. Создайте виртуальное окружение

```bash
    python -m venv venv
```

### 3. Активируйте виртуальное окружение

- Windows:

```bash
    venv\Scripts\activate
```

- Linux/macOS:

```bash
    source venv/bin/activate
```

### 4. Установите зависимости

```bash
    pip install -r requirements.txt
```

### 5. Инициализируйте базу данных

Прежде чем запустить приложение, создайте базу данных с помощью скрипта db_setup.py

```bash
    python src/db_setup.py
```

### 5. Заполните БД для тестирования (опционально)

```bash
    python src/seed_database.py
```

### 7. Запустите приложение

```bash
    python src/main.py
```
Теперь приложение будет доступно на вашем локальном сервере.

## Структура проекта

````
fitness-tracker/
├── src/                     # Исходный код приложения
│   ├── main.py              # Главный файл для запуска приложения
│   ├── db_manager.py        # Управление базой данных
│   ├── login_widget.py      # Экран авторизации
│   ├── registration_widget.py # Экран регистрации
│   ├── dashboard_widget.py  # Личный кабинет
│   ├── achievements_widget.py # Экран достижений
│   ├── activity_widget.py   # Экран записи активности
│   ├── progress_widget.py   # Экран прогресса
│   └── analytics_widget.py  # Экран аналитики
├── database/                # Папка для хранения базы данных
│   └── fitness_tracker.db   # База данных SQLite
├── requirements.txt         # Зависимости проекта
└── README.md                # Этот файл
````

## Технологии

- **Python 3.x** — язык программирования
- **PyQt5** — библиотека для графического интерфейса
- **SQLite** — база данных для хранения данных о пользователях и активности
- **matplotlib** — для построения графиков и визуализации данных

## Изменения

Если вы хотите что-то изменить в проекте, пожалуйста, создайте форк репозитория и откройте pull request с предложенными изменениями.