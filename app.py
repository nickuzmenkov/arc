import streamlit as st
import pandas as pd


@st.cache
def load_df():
    return pd.read_csv('./data.csv')


def search(df, r, min_nu=None, max_xi=None, min_pf=None):
    # direct comparison returns False even for equal numbers
    df = df[round(df['Reynolds'] - r) == 0]

    if min_nu is not None:
        df = df[df['Nusselt'] >= min_nu]

    if max_xi is not None:
        df = df[df['Cf'] <= max_xi]

    if min_pf is not None:
        df = df[1. / df['Performance'] >= min_pf]

    if len(df) > 0:
        return df.index[df['Performance'] == df['Performance'].min()]
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
    min_nu = None

if st.sidebar.checkbox('Ограничить рост сопротивления'):
    max_cf = st.sidebar.slider(
        'Максимальный рост гидравлического сопротивления',
        1., 10., 10., .5)
else:
    max_cf = None

if st.sidebar.checkbox('Ограничить габариты'):
    min_pf = st.sidebar.slider(
        'Минимальное снижение габаритов',
        1., 2., 1., .1)
else:
    min_pf = None

if st.sidebar.button('OK'):
    df = load_df()

    index = search(df, r, min_nu, max_cf, min_pf)

    if index is not None:

        form_dict = {
            0: '**прямоугольного профиля**',
            1: '**треугольного профиля, скошенных по потоку**',
            2: '**треугольного профиля, скошенных против потока**'}

        row = df.loc[index].values.tolist()[0]
        st.header(
            f'Возможно снижение габаритов в {1. / row[-1]:.2f} раз(а)')
        st.write(
            f'При росте теплоотдачи в {row[4]:.2f} раз(а) и сопротивления в {row[5]:.2f} раз(а).')
        st.write(
            f'При использовании искусственной шероховатости в виде выступов {form_dict[row[0]]} с параметрами: h/d={row[1]:.2f}, p/d={row[2]:.2f}.')
    else:
        st.header('Ошибка')
        st.write('Поиск с данными ограничениями вернул пустое множество. Попробуйте ослабить или убрать некоторые ограничения и повторите поиск.')
