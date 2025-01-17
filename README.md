# Fitness Tracker

Fitness Tracker — это приложение для мониторинга физической активности, которое позволяет пользователям отслеживать прогресс в достижении фитнес-целей, записывать данные о тренировках и делиться своими достижениями.

## Функциональные возможности:

- **Регистрация и авторизация пользователей**: Пользователи могут создать аккаунт, войти в систему и начать отслеживать свою активность. Включает возможность смены пароля, обновления профиля и выхода из системы.
- **Мониторинг активности**: Пользователи могут записывать количество шагов, калорий и другие метрики. Это включает:
  - Добавление записей о ежедневной активности (шаги, калории).
  - Редактирование, скачивание, загрузка и удаление записей активности.
- **Цели и достижения**: Пользователи могут устанавливать фитнес-цели (например, количество шагов за неделю или сожженные калории) и отслеживать их прогресс. Также можно получать достижения за выполнение целей.
- **Прогресс и аналитика**: Пользователи могут получать отчеты о своих достижениях, включая:
  - Среднее количество шагов и калорий за неделю.
  - Графики прогресса по целям.
  - Напоминания о достижениях и дедлайнах.
- **Добавление активности**: Пользователи могут добавлять активности вручную, включая:
  - Шаги, калории и другие данные.
  - Возможность редактировать, скачивать, загружать и удалять активности.
- **Уведомления**: Система уведомлений будет информировать пользователей:
  - Напоминания о добавлении активности за день.
  - Напоминания о приближении дедлайна целей.
- **Профиль пользователя**: Пользователи могут просматривать и редактировать свой профиль:
  - Изменение имени, email и пароля.
  - Удаление аккаунта.
- **История активности**: Пользователи могут просматривать свою историю активности с фильтрами:
  - По датам, типам активности и т.д.

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
    python src/db/db_setup.py
```

### 5. Заполните БД для тестирования (опционально)

```bash
    python src/seed/seed_database.py
```

### 7. Запустите приложение

```bash
    python -m src.main
```
Теперь приложение будет доступно на вашем локальном сервере.

## Структура проекта

````
fitness-tracker/
├── assets/                  # Директория для ассетов (Фотографии, иконки и т.д.)
│   └── images/                 # Директория с изображениями
│       └── photo.png/jpg           # Фотография
├── database/                # Директория для баз данных (Директория генерируется при разворачивании приложения)
│   └── fitness_tracker.db      # База данных приложения
├── resources/               # Фотографии, шрифты и прочее
├── schema/                  # Директория со схемами
│   └── schema.sql              # Схема БД
├── src/                     # Исходный код приложения
│   ├── db/                     # Директория со скриптами для БД
│   │   ├── db_manager.py           # Методы для взаимодействия с БД
│   │   └── db_setup.py             # Скрипт инициализации БД
│   ├── notification/           # Директория со скриптами для системы уведомлений
│   │   └── notification_manager.py # Менеджер уведомлений
│   ├── seed/                   # Директория со скриптами для создания моковых данных
│   │   └── seed_database.py        # Скрипт для заполнения БД моковыми данными
│   ├── state/                  # Директория с глобальными переменными
│   │   └── state_session.py        # Класс глобального состояния пользователя
│   ├── widget/                  # Директория с виджетами приложения
│   │   └── widget_*название*.py    # Виджет приложения
│   └── main.py              # Главный файл для запуска приложения
├── test/                    # Директория со скриптами или файлами для тестирования
│   └── txt/                    # Директория с файлами для тестирования
│       └── test.txt                # Файл для тестирования
├── .gitignore               # Исключение файлов Git
├── README.md                # Этот файл
└── requirements.txt         # Зависимости проекта
````

## Технологии

- **Python 3.x** — язык программирования;
- **PyQt5** — библиотека для графического интерфейса;
- **SQLite** — база данных для хранения данных о пользователях и активности;
- **matplotlib** — для построения графиков и визуализации данных.

## Изменения

Если вы хотите что-то изменить в проекте, пожалуйста, создайте форк репозитория и откройте pull request с предложенными изменениями.