from streamlit_autorefresh import st_autorefresh
from io import BytesIO
from utils import info_news,info_employee,info_event,search
import streamlit as st
import requests
import qrcode
import json


# Настройка страницы для адаптивного отображения (wide layout)
st.set_page_config(page_title="Портал компании", layout="wide")

# Базовый URL для нашего Flask API
BASE_URL = "http://127.0.0.1:5000"






def main():
    # st.logo(путь файла)
    query=st.text_input("Поиск",placeholder="Введите запрос для поиска")


    # блок с сотрудниками
    st.title("Сотрудники")

    response=requests.get(BASE_URL+"/employees")
    employees=response.json()

    col1,col2,col3,col4,col5=st.columns(5)
    if query:
         search(col1,employees,query,info_employee)
    else:
        info_employee(col1,employees[0])
        info_employee(col2,employees[1])
        info_employee(col3,employees[2])
        info_employee(col4,employees[3])
        info_employee(col5,employees[4])

    # Блок с новостями
    st.title("Новости")

    response=requests.get(BASE_URL+"/swagger")
    news=response.json()
    col1,col2,col3,col4,col5=st.columns(5)

    if query:
         search(col1,news,query,info_news)
        # for i in range(len(news)):  # Перебираем все новости
        #     for key, value in news[i].items():  # Перебираем ключи и значения каждой новости
        #         if query.lower() in str(value).lower():  # Регистронезависимый поиск
        #             st.write(f"Совпадение найдено в поле '{key}': {value}")
        #             info_news(col1, news[i])  # Выводим новость
    else:  

        info_news(col1,news[0])
        info_news(col2,news[1])
        info_news(col3,news[2])
        info_news(col4,news[3])
        info_news(col5,news[4])


    # блок с событиями
    st.title("События")

    response=requests.get(BASE_URL+"/event")
    event=response.json()

    col1,col2,col3,col4,col5=st.columns(5)
    if query:
         search(col1,event,query,info_event)
    else: 
        info_event(col1,event[0])
        info_event(col2,event[1])
        info_event(col3,event[2])
        info_event(col4,event[3])
        info_event(col5,event[4])



if __name__ == "__main__":
    main()
 