import sqlite3


# Функция для склонения слов с числами
def num_word(value, words, show=True):
    num = value % 100
    if num > 19:
        num = num % 10
    out = str(value) + ' ' if show else ''
    match num:
        case 1:
            out += words[0]
        case 2 | 3 | 4:
            out += words[1]
        case _:
            out += words[2]
    return out


# Функция, создающая таблицу при её отсутствии
def create_database():
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT
        )
    """)

    connection.commit()
    connection.close()


# Функция, добавляющая новую заметку
def add_note(title, content):
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO notes (title, content)
        VALUES (?, ?)
    """, (title, content))

    connection.commit()
    connection.close()


# Функция, получающая список заметок
def get_all_notes():
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    connection.close()
    return notes


def get_note_by_id(id):
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes WHERE id = ?", (id,))
    note = cursor.fetchone()

    connection.close()
    return note


# Функция поиска заметок
def search_notes(query):
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM notes
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY title
    """, ("%{}%".format(query), "%{}%".format(query)))
    notes = cursor.fetchall()

    connection.close()
    return notes


# Функция удаления заметки
def delete_note(id):
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?", (id,))
    result = cursor.rowcount

    connection.commit()
    connection.close()

    return result


# Основная функция
def main():
    print("Добро пожаловать в менеджер заметок!")
    create_database()

    while True:
        print(
            "\nЧто вы хотите сделать?\n1. Добавить заметку\n2. Просмотреть список заметок\n3. Поиск заметок\n4. Удалить заметку\n5. Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            title = input("Введите название заметки: ")
            content = input("Введите содержание заметки: ")
            add_note(title, content)

        elif choice == "2":
            notes = get_all_notes()
            count = "нет заметок" if not notes else num_word(len(notes), ["заметка:", "заметки:", "заметок:"])
            print(f"\n‣ У вас {count}\n")
            if not notes:
                continue
            for note in notes:
                title = note[1][:100] + "…" if len(note[1]) > 100 else note[1]
                print(f"[{note[0]}] {title}")
            id = input("\nВведите [ID] заметки, чтобы просмотреть её, или \"-\", чтобы выйти в главное меню: ")
            if id != "-":
                note = get_note_by_id(id)
                print(
                    "\n‣ Нет заметки с таким ID" if not note else f"\n‣ Открыта заметка [{note[0]}]:\n\n{note[1]}\n\n{note[2]}")


        elif choice == "3":
            query = input("Введите ключевое слово или фразу для поиска: ")
            notes = search_notes(query)
            text = "Ничего не найдено" if not notes else "Нашёл " + num_word(len(notes),
                                                                             ["заметку:", "заметки:", "заметок:"])
            print(f"\n‣ {text}\n")
            if not notes:
                continue
            for note in notes:
                title = note[1][:100] + "…" if len(note[1]) > 100 else note[1]
                print(f"[{note[0]}] {title}")

            id = input("\nВведите [ID] заметки, чтобы просмотреть её, или \"-\", чтобы выйти в главное меню: ")
            if id != "-":
                note = get_note_by_id(id)
                print(
                    "Нет заметки с таким ID" if not note else f"\nОткрыта заметка [{note[0]}]:\n\n{note[1]}\n\n{note[2]}")


        elif choice == "4":
            id = input("Введите идентификатор заметки для удаления: ")
            result = delete_note(id)
            print(f"\n‣ Успешно удалена заметка с ID = {id}" if result else "\n‣ Нет заметки с таким ID")

        elif choice == "5":
            print("\n‣ До свидания!")
            exit()

        else:
            print("\n‣ Неизвестный выбор.")


if __name__ == "__main__":
    main()
