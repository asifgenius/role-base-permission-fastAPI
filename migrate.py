from app.database.base import init_database


if __name__ == "__main__":
    init_database()
    print("Database schema is up to date.")
