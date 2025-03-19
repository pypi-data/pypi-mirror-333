import streamlit as st
import qrcode
from io import BytesIO

def info_employee(col,data):
    
    name = data.get("name", "Имя не указано")
    email = data.get("email", "Email не указан")
    phone = data.get("phone", "Телефон не указан")
    position = data.get("position", "Должность не указана")
    date = data.get("date", "Дата не указана")
    
    with col:
        with st.expander(name,expanded=True):
            st.write(email)
            st.write(phone)
            st.write(position)
            st.write(date)
            if st.button("Показать qr-code",key=f"qr_button_{data.get("Id")}"):
                vcard=f"""BEGIN:VCARD
                    VERSION:3.0
                    N:{name}
                    FN:{name}
                    ORG:Дороги России
                    TITLE:{position}
                    TEL;WORK;VOICE:{phone}
                    TEL;CELL:{phone}
                    EMAIL;WORK;INTERNET:{email}
                    END:VCARD
                    """
                
                image=qrcode.make(vcard,box_size=10,border=4)
                buffered=BytesIO()
                image.save(buffered,format="PNG")
                st.image(buffered.getvalue(),caption="QR-Code сотрудника",use_container_width=True)
                
def info_news(col,data):

    id=data.get("id")
    title=data.get("title")
    date=data.get("date")
    description=data.get("description")
    image=data.get("image")


    with col:
        with st.expander(title,expanded=True):
            st.write(date)
            st.write(description)
            st.image(image,caption="Photo",use_container_width=True)
            

def info_event(col,data):

    id=data.get("id")
    title=data.get("title")
    date=data.get("date")
    author=data.get("author")
    text=data.get("short_text")

    ics_content=f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{title}
DTSTART:{date}
DTEND:Дата начала
DTSTAMP:Дата создания события
UID:{id}
DESCRIPTION:{text}
LOCATION:место события
ORGANIZER:{author}
STATUS:CONFIRMED
PRIORITY:0
END:VEVENT
END:VCALENDAR"""

    with col:
        with st.expander(title,expanded=True):
            st.write(date)
            st.write(author)
            st.write(text)
            st.download_button(
                                label="Добавить в календарь",
                                data=ics_content,
                                file_name=f"event_{id}.ics",
                                mime="text/calendar",
                                key=f"download_btn_{id}"
                                )
                
def search(col,data,query,func):
    found=False
    for i in range(len(data)):
            for key, value in data[i].items(): 
                if query.lower() in str(value).lower(): 
                    func(col, data[i]) 
                    found=True
                    break

    if not found:
         st.info("Новость не найдена")