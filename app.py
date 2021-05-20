import streamlit as st
import pandas as pd
import sqlite3


def select(r, min_nu, max_xi, min_pf):
    connect = sqlite3.connect('assets/db/arc.db')
    query = f'''
        SELECT *
        FROM data
        WHERE reynolds = {r} AND
            nusselt >= {min_nu} AND
            friction <= {max_xi} AND
            performance <= {1 / min_pf};'''
    df = pd.read_sql_query(query, connect).set_index('id')
    connect.close()
    return df


def search(df):
    if len(df) > 0:
        return df.index[df['performance'] == df['performance'].min()]
    else:
        return None


st.header('Конфигуратор искусственной шероховатости')
st.write('Введите условия и ограничения в полях слева для получения эффективных параметров искусственной шероховатости теплообменного аппарата с помощью обученной нейронной сети')

st.sidebar.header('Условия')

r = st.sidebar.slider(
    'Число Рейнольдса',
    10000., 60000., 10000., 2000., format='%i')

st.sidebar.header('Ограничения')

if st.sidebar.checkbox('Ограничить рост теплоотдачи'):
    min_nu = st.sidebar.slider(
        'Минимальный рост теплоотдачи',
        1., 2.2, 1., .1)
else:
    min_nu = 1.

if st.sidebar.checkbox('Ограничить рост сопротивления'):
    max_cf = st.sidebar.slider(
        'Максимальный рост гидравлического сопротивления',
        1., 10., 10., .5)
else:
    max_cf = 10.

if st.sidebar.checkbox('Ограничить габариты'):
    min_pf = st.sidebar.slider(
        'Минимальное снижение габаритов',
        1., 2., 1., .1)
else:
    min_pf = 1.

if st.sidebar.button('OK'):
    df = select(r, min_nu, max_cf, min_pf)
    index = search(df)

    if index is not None:

        form_dict = {
            0: '**прямоугольного профиля**',
            1: '**треугольного профиля, скошенных по потоку**',
            2: '**треугольного профиля, скошенных против потока**'}

        row = df.loc[index]
        st.header(
            f'Возможно снижение габаритов в {1. / float(row["performance"]):.2f} раз(а)')
        st.write(
            f'При росте теплоотдачи в {float(row["nusselt"]):.2f} раз(а) и сопротивления в {float(row["friction"]):.2f} раз(а).')
        st.write(
            f'При использовании искусственной шероховатости в виде выступов {form_dict[int(row["type"])]} с параметрами: h/d={float(row["height"]):.2f}, p/d={float(row["pitch"]):.2f}.')
    else:
        st.header('Ошибка')
        st.write('Поиск с данными ограничениями вернул пустое множество. Попробуйте ослабить или убрать некоторые ограничения и повторите поиск.')
