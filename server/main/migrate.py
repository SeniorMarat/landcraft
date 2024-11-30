import os
import psycopg2
from config import DB_CONFIG, MIGRATIONS_DIR
from psycopg2 import sql


def main():
    # Подключаемся к базе данных
    try:
        conn = psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return

    try:
        # Получаем список применённых миграций
        applied_migrations = get_applied_migrations(conn)
        print(f"Применённые миграции: {applied_migrations}")

        # Получаем список всех файлов миграции
        migration_files = sorted(os.listdir(MIGRATIONS_DIR))

        # Применяем только новые миграции
        for migration in migration_files:
            if migration not in applied_migrations:
                print(f"Применяем миграцию: {migration}")
                apply_migration(conn, migration, os.path.join(MIGRATIONS_DIR, migration))
                print(f"Миграция {migration} успешно применена.")
            else:
                print(f"Миграция {migration} уже применена.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
