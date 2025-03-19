import streamlit as st
from datetime import datetime
import os

# Для генерации .ics-файлов
from ics import Calendar, Event

# ============ ДАННЫЕ ============

# Пример списка новостей
news_data = [
    {
        "id": 1,
        "title": "Новость 1",
        "description": "Короткое описание новости 1",
        "image_url": None,  # Пока нет URL, будет заглушка
        "date": "2025-02-10",
        "likes": 10,
        "dislikes": 2
    },
    {
        "id": 2,
        "title": "Новость 2",
        "description": "Короткое описание новости 2",
        "image_url": None,
        "date": "2025-02-12",
        "likes": 5,
        "dislikes": 1
    },
    {
        "id": 3,
        "title": "Новость 3",
        "description": "Короткое описание новости 3",
        "image_url": None,
        "date": "2025-02-13",
        "likes": 0,
        "dislikes": 0
    },
]

# Пример списка событий
events_data = [
    {
        "id": 101,
        "title": "Событие A",
        "description": "Описание события A",
        "date": "2025-02-20"
    },
    {
        "id": 102,
        "title": "Событие B",
        "description": "Описание события B",
        "date": "2025-03-01"
    },
    {
        "id": 103,
        "title": "Событие C",
        "description": "Описание события C",
        "date": "2025-04-15"
    },
]

# ============ ФУНКЦИИ ============

def update_reaction(news_id, reaction_type):
    """Обновляем счетчики лайков/дизлайков в памяти (имитация сервера)."""
    for news in news_data:
        if news["id"] == news_id:
            if reaction_type == "like":
                news["likes"] += 1
            elif reaction_type == "dislike":
                news["dislikes"] += 1

def create_ics_event(title, description, start_date):
    """
    Создаёт строку .ics (формат календаря) для события.
    Здесь для простоты end_date = start_date + 1 час.
    """
    c = Calendar()
    e = Event()
    e.name = title
    e.begin = f"{start_date} 10:00:00"  # Начало в 10:00
    e.end = f"{start_date} 11:00:00"    # Конец в 11:00
    e.description = description
    c.events.add(e)
    return str(c)

# ============ ОСНОВНОЙ КОД СТРАНИЦЫ ============

def main():
    st.title("Новости и События")

    # Инициализируем словарь для отслеживания голосов по новостям
    # Ключ – id новости, значение – выбранная реакция ("like" или "dislike")
    if "news_reactions" not in st.session_state:
        st.session_state.news_reactions = {}

    tabs = ["Новости", "События"]
    selected_tab = st.sidebar.radio("Выберите раздел:", tabs)

    if selected_tab == "Новости":
        st.header("Последние новости")

        if "news_index" not in st.session_state:
            st.session_state.news_index = 0

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("<< Предыдущая"):
                st.session_state.news_index = max(0, st.session_state.news_index - 1)
        with col2:
            if st.button("Следующая >>"):
                st.session_state.news_index = min(len(news_data) - 1, st.session_state.news_index + 1)

        current_news = news_data[st.session_state.news_index]
        st.subheader(current_news["title"])

        # Отображение изображения: если нет URL, используем заглушку
        placeholder_path = "placeholder.png"
        if current_news["image_url"]:
            st.image(current_news["image_url"], width=300)
        else:
            if os.path.exists(placeholder_path):
                st.image(placeholder_path, width=300)
            else:
                st.warning("Файл заглушки (placeholder.png) не найден!")

        st.write(current_news["description"])
        st.write(f"Дата новости: {current_news['date']}")

        news_id = current_news["id"]

        # Проверяем, голосовал ли пользователь за эту новость
        if news_id in st.session_state.news_reactions:
            st.info(f"Вы уже проголосовали: {st.session_state.news_reactions[news_id]}")
        else:
            like_col, dislike_col = st.columns([1, 1])
            with like_col:
                if st.button("👍", key=f"like_{news_id}"):
                    update_reaction(news_id, "like")
                    st.session_state.news_reactions[news_id] = "like"
            with dislike_col:
                if st.button("👎", key=f"dislike_{news_id}"):
                    update_reaction(news_id, "dislike")
                    st.session_state.news_reactions[news_id] = "dislike"

        st.write(f"Likes: {current_news['likes']} | Dislikes: {current_news['dislikes']}")

    else:
        st.header("Ближайшие события")

        # Сортировка событий по дате (от новых к старым)
        sorted_events = sorted(events_data, key=lambda e: e["date"], reverse=True)

        for event in sorted_events:
            st.subheader(event["title"])
            st.write(event["description"])
            st.write(f"Дата события: {event['date']}")

            # При нажатии формируем ICS-файл для добавления события в календарь
            if st.button("★ Добавить в календарь", key=f"event_{event['id']}"):
                ics_data = create_ics_event(
                    title=event["title"],
                    description=event["description"],
                    start_date=event["date"]
                )
                st.download_button(
                    label="Скачать ICS-файл",
                    data=ics_data,
                    file_name=f"{event['title']}.ics",
                    mime="text/calendar"
                )
                st.success(f"Файл для события '{event['title']}' сформирован.")

if __name__ == "__main__":
    main()
