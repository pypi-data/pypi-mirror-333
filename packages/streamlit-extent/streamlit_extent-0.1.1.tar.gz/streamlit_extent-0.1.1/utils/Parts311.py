from flask import Flask, jsonify, request, make_response, send_file
import pyodbc

app = Flask(__name__)


conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=84.54.228.191,49172;"
    "DATABASE=Pushkarcki;"
    "UID=Pushkarcki;"
    "PWD=3kVJPI3h;"
)
connect=pyodbc.connect(conn_str)
cursor=connect.cursor()

data_news=[
    {
      "id": 1,
      "title": "Новая технология в области медицины",
      "date": "2025-02-12",
      "description": "Ученые разработали инновационную технологию для лечения редких заболеваний, которая может изменить подход к медицинской практике.",
      "image": None,
      "likes": 125,
      "dislikes": 8
    },
    {
      "id": 2,
      "title": "Экологические инициативы в крупных городах",
      "date": "2025-02-11",
      "description": "В нескольких крупных городах мира стартуют экологические проекты, направленные на улучшение качества воздуха и снижение углеродных выбросов.",
      "image": None,
      "likes": 97,
      "dislikes": 5
    },
    {
      "id": 3,
      "title": "Прорыв в области искусственного интеллекта",
      "date": "2025-02-10",
      "description": "Новая система искусственного интеллекта, способная самостоятельно обучаться, обещает произвести революцию в различных отраслях.",
      "image": None,
      "likes": 210,
      "dislikes": 12
    },
    {
      "id": 4,
      "title": "Запуск нового космического спутника",
      "date": "2025-02-09",
      "description": "Космическое агентство успешно вывело на орбиту новый спутник для исследований в области климатических изменений.",
      "image": None,
      "likes": 156,
      "dislikes": 7
    },
    {
      "id": 5,
      "title": "Международная конференция по кибербезопасности",
      "date": "2025-02-08",
      "description": "В Москве прошла международная конференция, посвященная вопросам безопасности в интернете и защите данных.",
      "image": None,
      "likes": 89,
      "dislikes": 4
    }
  ]

@app.route("/swagger/<int:id>/<string:type>",methods=["POST"])
def post_news(id,type):

  if type=="likes": 
    data_news[id-1]["likes"]+=1
    # print(data_news[id]["likes"])
    return f"{data_news[id]["likes"]}"
  
  elif type=="dislikes":
    data_news[id-1]["dislikes"]+=1
    # print(data_news[id]["dislikes"])
    return f"{data_news[id]["dislikes"]}"
  else:
     return "Некорректный метод"

@app.route("/swagger",methods=["GET"])
def get_news():

  return jsonify(data_news)
    
   
        

@app.route("/event")
def event_info():
    info=[
  {
    "id": 1,
    "title": "Запуск нового проекта по устойчивому развитию",
    "date": "2025-02-12",
    "author": "Иван Петров",
    "short_text": "Сегодня стартовал проект по устойчивому развитию, направленный на улучшение экологии и сохранение природных ресурсов в регионе."
  },
  {
    "id": 2,
    "title": "Вебинар по цифровым технологиям в образовании",
    "date": "2025-02-11",
    "author": "Александра Смирнова",
    "short_text": "Пройдет вебинар, на котором эксперты обсудят внедрение цифровых технологий в школьное и вузовское образование."
  },
  {
    "id": 3,
    "title": "Международная конференция по искусственному интеллекту",
    "date": "2025-02-10",
    "author": "Дмитрий Кузнецов",
    "short_text": "Конференция соберет ведущих специалистов в области искусственного интеллекта для обсуждения перспектив и вызовов этой технологии."
  },
  {
    "id": 4,
    "title": "Фестиваль стартапов и инноваций",
    "date": "2025-02-09",
    "author": "Мария Лебедева",
    "short_text": "Мероприятие для начинающих предпринимателей и стартаперов, на котором будут представлены новейшие идеи и разработки."
  },
  {
    "id": 5,
    "title": "Мастер-класс по креативному мышлению",
    "date": "2025-02-08",
    "author": "Сергей Васильев",
    "short_text": "Мастер-класс, на котором участники научатся использовать нестандартные подходы для решения проблем и создания инновационных проектов."
  }
]

    return jsonify(info)

@app.route("/employees")
def employees_info():
    query="Select DISTINCT Employees.Id,FullName,Email,WorkPhone,P.NamePosition,Ad.DateBirth from Employees join Positions as P on P.Id=Employees.IdPosition join AddInfo as Ad on Ad.IdEmployee=Employees.Id"
    cursor.execute(query)
    info=cursor.fetchall()
    result=[]
    for row in info:
        date_info=str(row[5])
        date,month=date_info[5:7].strip(),date_info[8:11]
        result.append({
                "Id":row[0],
                "name":row[1],
                "email":row[2],
                "phone":row[3],
                "position":row[4],
                "date":f"День {date} Месяц {month}"
        })
    return jsonify(result)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
