import streamlit as st
import requests

base_url="http://192.168.0.15:5000"

def reaction(id,type):

    if id is not None:
        requests.post(base_url+f"/swagger/{id}/{type}",json={})
        # return response.json()

def main():
    
    st.set_page_config(page_icon="",page_title="что то для моблы")

    menu = st.sidebar.radio("Выберите раздел", ["Новости", "События"])

    if menu == "Новости":
        st.title("Новости")
        
        # Инициализируем словарь для отслеживания голосов (ключ — news_id)
        if "news_reactions" not in st.session_state:
            st.session_state.news_reactions = {}

        response = requests.get(f"{base_url}/swagger")
        data = response.json()

        if "index" not in st.session_state:
            st.session_state.index = 0

        index = st.session_state.index

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("<< Предыдущая"):
                index = (index - 1) % len(data)
                st.session_state.index = index
        with col2:
            if st.button("Следующая >>"):
                index = (index + 1) % len(data)
                st.session_state.index = index

        st.header(data[index]["title"])

        if data[index]["image"]:
            st.image(data[index]["image"])
        else:
            st.image("image/photo.jpg")

        st.text(data[index]["description"])
        st.write(data[index]["date"])

        news_id = data[index]["id"]
        current_reaction = st.session_state.news_reactions.get(news_id)

        if current_reaction:
            st.info(f"Ваш текущий голос: {current_reaction}")
        else:
            st.info("Вы еще не голосовали.")

        # Всегда показываем обе кнопки, чтобы позволить изменить голос
        col_like, col_dislike = st.columns([1, 1])

        with col_like:
            if st.button("👍 Likes", key="btn_like"):
                # Если голос не совпадает, то изменяем его
                if current_reaction != "likes":
                    reaction(news_id, "likes")
                    st.session_state.news_reactions[news_id] = "likes"
                    st.rerun()
        with col_dislike:
            if st.button("👎 Dislikes", key="btn_dislike"):
                if current_reaction != "dislikes":
                    reaction(news_id, "dislikes")
                    st.session_state.news_reactions[news_id] = "dislikes"
                    st.rerun()

        st.write(f"likes: {data[index]['likes']} | Dislikes: {data[index]['dislikes']}")

    else:
        st.header("Ближайшие события")

        response=requests.get(base_url+"/event")
        events_data= response.json()


        sorted_events = sorted(events_data, key=lambda e: e["date"], reverse=True)

        for event in sorted_events:
            st.header(event["title"])
            st.write(event["short_text"])
            col1,col2=st.columns([1,1])
            with col1:
                st.write(event["date"])
            with col2:
                st.write(event["author"])

if __name__=="__main__":
    main()