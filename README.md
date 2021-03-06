# Artificial Roughness Configurator 
Конфигуратор искусственной шероховатости

## Описание
Приложение-конфигуратор искусственной шероховатости для теплообменных аппаратов типа "труба в трубе" на базе статьи [1]:
* предсказания обученной нейронной сети для широкого диапазона входных параметров записаны в базу данных SQLite `assets/db/arc.db` (для удобства те же данные доступны в формате .csv: `assets/csv/data.csv`)
* для поиска в базе данных создано приложение с GUI интерфейсом `app.py` с помощью Streamlit API [2]

## Использование
Для запуска необходимо активировать виртуальную среду и Streamlit:
```
# на Linux/MacOS
source venv/scripts/activate
# на Windows
.\venv\scripts\activate

streamlit run app.py
```
После чего откроется приложение:

![alt text](https://github.com/nickuzmenkov/arc/blob/main/assets/img/app_1.png?raw=true)

В полях слева необходимо ввести штатное число Рейнольдса и прочие ограничения, налагаемые на теплообменный аппарат. При нажатии на кнопку "ОК" в базе данных будет найдена запись, соответствующая наиболее эффективной конфигурации шероховатости для данного случая:

![alt text](https://github.com/nickuzmenkov/arc/blob/main/assets/img/app_2.png?raw=true)

В случае, если введенным требованиям нельзя удовлетворить (например, минимальный рост теплоотдачи - 2 раза, максимальный рост сопротивления - 1.1 раза), высветится сообщение об ошибке.

## Ссылки
1. [N V Kuzmenkov et al 2021 J. Phys.: Conf. Ser. 1891 012063](https://iopscience.iop.org/article/10.1088/1742-6596/1891/1/012063)
2. [Streamlit Official Documentation](https://docs.streamlit.io/en/stable/index.html)
