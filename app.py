import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title('Загрузка и отображение данных')

# Загрузка данных пользователем
uploaded_file = st.file_uploader("Загрузите файл данных (CSV или Excel)", type=["csv", "xlsx"], key="unique_key")

if uploaded_file is not None:
    # Проверка типа файла и загрузка данных
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        data = pd.read_excel(uploaded_file)
    st.write("Загруженные данные", data.head())
else:
    # Если пользователь не загрузил файл, отображаем стандартные файлы данных
    # st.info('')

    # Загрузка и отображение данных о инфляции
    st.subheader('Данные об инфляции')
    inflation_data = pd.read_csv('inflation_data.csv')
    st.write(inflation_data.head())

    # Загрузка и отображение данных о заработной плате
    st.subheader('Данные о заработной плате')
    salary_data = pd.read_excel('zpl.xlsx', sheet_name='task4')
    st.write(salary_data.head())
 

# Заголовок приложения
st.title('Анализ заработных плат в России')
st.subheader("График изменения заработной платы в строительстве, в области информации и связи, и в финансовой сфере")

# Загрузка данных
data = pd.read_csv('task3.csv', delimiter=';')

# Установка 'Год' в качестве индекса
df = data.set_index('Год')

# Определение размера фигуры: уменьшить ширину, если метки перекрываются
fig_width = max(10, len(df.index) * 0.5)  # Эвристика: 0.5 дюйма на метку года

# Настройка ширины фигуры на основе эвристики
fig, ax = plt.subplots(figsize=(fig_width, 7))

# Определение цветов и стилей линий
colors = {
    "Строительство": "blue",
    "Деятельность в области информации и связи": "green",
    "Финансовая деятельность": "orange",
    "Всего по экономике": "black"
}
line_styles = {
    "Всего по экономике": '--'
}

# Цикл для отображения колонок с указанными цветами и стилями линий
for column in df.columns:
    ax.plot(df.index, df[column], label=column, color=colors.get(column, 'grey'), 
             linestyle=line_styles.get(column, '-'), linewidth=2 if column == 'Всего по экономике' else 1)

# Настройка горизонтальных меток на оси X для отображения каждого года
ax.set_xticks(df.index)  # Горизонтальное отображение меток

# Добавление заголовков и меток
ax.set_title('Динамика изменения зарплаты по видам экономической деятельности (2000-2023 гг.)')
ax.set_xlabel('Год')
ax.set_ylabel('Среднегодовая зарплата (руб.)')
ax.legend()
ax.grid(True)

# Отображение графика в Streamlit
st.pyplot(fig)

st.markdown("""
    ### Анализ динамики зарплат 
1. Общий рост зарплат: Наблюдается стабильный рост зарплат на протяжении всего рассматриваемого периода.

2. Самый высокий рост заработной платы в финансовой сфере связан с развитием финансовых технологий, увеличением объема финансовых услуг и ростом капитализации рынка.

3. Деятельность в области информации и связи также показывает значительный рост, особенно после 2016 года, и отражает глобальный тренд цифровизации: бурное развитие информационных технологий и их повсеместное внедрение, переход к цифровой экономике и экономике данных.

4. Строительство: Динамика роста зарплат в строительстве тесно связана с общей экономической активностью и инфраструктурными проектами, которые, как правило, обеспечены государственными инвестициями.

5. Динамика по сравнению с экономикой в целом: Зарплаты в секторах "Деятельность в области информации и связи" и "Финансовая деятельность" растут значительно быстрее, чем в среднем по экономике. Эти секторы являются более высокотехнологичными и востребованными, а также имеют большую добавленную стоимость и потенциал для инвестиций.
""")


st.markdown('# Пересчет средних зарплат с учетом уровня инфляции.')
# Функция для загрузки данных
@st.cache_data
def load_salary_data():
    # Загрузка данных из Excel
    salary = pd.read_excel('zpl.xlsx', sheet_name='task4')
    salary.set_index('Год', inplace=True)
    return salary

# Загрузка данных
salary = load_salary_data()


# Функция для загрузки и предобработки данных об инфляции
@st.cache_data
def load_inflation_data():
    # Загрузка данных
    data = pd.read_csv('inflation_data.csv')
    inflation_data = pd.DataFrame(data)
    
    # Обработка данных
    inflation_data = inflation_data[['Год', 'Всего']]
    inflation_data.rename(columns={'Всего': 'Инфляция'}, inplace=True)
    inflation_data.set_index('Год', inplace=True)
    
    # Фильтрация данных по годам
    filtered_inflation_data = inflation_data[(inflation_data.index >= 2000) & (inflation_data.index <= 2023)]
    
    # Инвертирование данных DataFrame
    reversed_inflation_data = filtered_inflation_data.iloc[::-1]
    
    return reversed_inflation_data

# Загрузка обработанных данных
reversed_inflation_data = load_inflation_data()


# Функция для расчета реальной зарплаты
def calculate_real_salary(nominal_salary, inflation_rate):
    price_index = 1 + inflation_rate / 100
    return nominal_salary / price_index

@st.cache_data
def load_and_process_data():
    # Загрузка данных о зарплатах
    salary = pd.read_excel('zpl.xlsx', sheet_name='task4')
    salary.set_index('Год', inplace=True)
    
    # Загрузка и обработка данных об инфляции
    inflation_data = pd.read_csv('inflation_data.csv')
    inflation_data = inflation_data[['Год', 'Всего']]
    inflation_data.rename(columns={'Всего': 'Инфляция'}, inplace=True)
    inflation_data.set_index('Год', inplace=True)
    
    # Расчет реальной зарплаты для каждого столбца
    real_salary = salary.copy()
    for year in real_salary.index:
        if year in inflation_data.index:
            inflation_rate = inflation_data.at[year, 'Инфляция']
            real_salary.loc[year] = real_salary.loc[year].apply(lambda x: calculate_real_salary(x, inflation_rate))

    # Добавление абсолютного и процентного изменений для каждого столбца
    for col in salary.columns:
        real_salary[f'{col}_абсолютное_изменение'] = real_salary[col].diff()
        real_salary[f'{col}_процентное_изменение'] = real_salary[col].pct_change() * 100

    return real_salary

real_salary = load_and_process_data()
# Определяем новый порядок столбцов
columns_order = ['Строительство', 'Строительство_абсолютное_изменение', 'Строительство_процентное_изменение',
                 'Информация и связь', 'Информация и связь_абсолютное_изменение', 'Информация и связь_процентное_изменение',
                 'Финансовая деятельность', 'Финансовая деятельность_абсолютное_изменение', 'Финансовая деятельность_процентное_изменение',
                 'Всего по экономике', 'Всего по экономике_абсолютное_изменение', 'Всего по экономике_процентное_изменение']

# Упорядочиваем столбцы в DataFrame
real_salary_ordered = real_salary.reindex(columns=columns_order)
# Вывод результатов
st.write("Абсолютное относительное изменение реальных заработных плат", real_salary_ordered.head())


import streamlit as st
import pandas as pd

# Функция для загрузки и предобработки данных
@st.cache_data
def load_data():
    # Загрузка данных о зарплатах
    salary = pd.read_excel('zpl.xlsx', sheet_name='task4')
    salary.set_index('Год', inplace=True)
    
    # Загрузка данных об инфляции
    inflation_data = pd.read_csv('inflation_data.csv')
    inflation_data = inflation_data[['Год', 'Всего']]
    inflation_data.rename(columns={'Всего': 'Инфляция'}, inplace=True)
    inflation_data.set_index('Год', inplace=True)
    
    return salary, inflation_data

# Обработка данных
salary, inflation_data = load_data()

# Расчет изменений для номинальной зарплаты
nominal_salary_absolute_change = salary.diff()
nominal_salary_percent_change = salary.pct_change() * 100

# Вызов функции для расчета реальной зарплаты (необходимо добавить код функции calculate_real_salary)
real_salary = salary.copy()
for year in real_salary.index:
    real_salary.loc[year] = calculate_real_salary(
        salary.loc[year],
        inflation_data.loc[year, 'Инфляция']
    )

# Расчет изменений для реальной зарплаты
real_salary_absolute_change = real_salary.diff()
real_salary_percent_change = real_salary.pct_change() * 100

# Создание DataFrame для сравнения изменений
salary_comparison = pd.DataFrame({
    'Номинальная_абсолютное_изменение': nominal_salary_absolute_change.stack(),
    'Номинальная_процентное_изменение': nominal_salary_percent_change.stack(),
    'Реальная_абсолютное_изменение': real_salary_absolute_change.stack(),
    'Реальная_процентное_изменение': real_salary_percent_change.stack(),
}).reset_index()

# Переименование столбцов для лучшей читаемости
salary_comparison.rename(columns={'level_1': 'Тип деятельности'}, inplace=True)

# Отображение данных
st.write("Абсолютное и процентное изменение номинальных и реальныз заработных плат", salary_comparison.head())

st.markdown("**Влияние инфляции на изменение зарплаты по сравнению с предыдущим годом**"
    
)
def plot_salary_changes():
    # Установка размера графика
    plt.figure(figsize=(14, 7))

    # Фильтрация данных для категории 'Всего по экономике'
    data_filtered = salary_comparison[salary_comparison['Тип деятельности'] == 'Всего по экономике']

    # Создание графика изменений номинальной и реальной зарплаты
    sns.lineplot(data=data_filtered, x='Год', y='Номинальная_процентное_изменение', label='Номинальное изменение')
    sns.lineplot(data=data_filtered, x='Год', y='Реальная_процентное_изменение', label='Реальное изменение')

    # Настройка заголовка и меток графика
    plt.title('Сравнение номинального и реального изменения зарплаты в экономике')
    plt.ylabel('Процентное изменение')
    plt.xlabel('Год')
    plt.legend()

    # Отображение графика в Streamlit
    st.pyplot(plt.gcf())  

# Вызов функции для построения и отображения графика
plot_salary_changes()

st.markdown('''
Реальное процентное изменение зарплаты больше номинального, при положительной инфляции, это может показаться нелогичным. Однако такая ситуация может возникнуть в реальности из-за следующих причин:
            
Эффект высокой базы: При снжении темпов инфляции: если в предыдущем году инфляция была высокой, а в текущем снизилась (но всё же положительна), то даже при умеренном росте номинальной зарплаты реальное изменение может быть больше номинального.
            
Нестандартные изменения в зарплатах: Возможны ситуации, когда зарплаты растут быстрее общего уровня цен из-за политических решений, повышения минимальной заработной платы или других экономических факторов.''')

import streamlit as st

st.markdown('Динамика изменения реальных зарплат с учетом инфляции.')

image_path = 'Change.png'
st.image(image_path, caption='Описание изображения')

st.markdown('''## Выводы
На графике видно, что реальные зарплаты в разных секторах экономики сильно колеблются из года в год. Это может быть связано с экономическими циклами, изменениями в спросе на определённые виды деятельности, технологическими инновациями или политическими решениями.

Сравнение с уровнем инфляции: Большую часть времени изменение зарплат превышает уровень инфляции, это говорит о повышении покупательной способности населения. Также на графике хорошо видны два периода, когда инфляция выше роста реальных зарплат, в эти периоды реальный доход населения падал.

Отраслевые различия: Разные отрасли показывают различную динамику изменения зарплат. Например, может быть, что финансовый сектор в определённые годы показывает больший рост зарплат по сравнению с другими секторами, что может отражать отраслевые тенденции, например, быстрый рост в области финтеха или повышенный спрос на финансовые услуги.
''')

# ############################################

# # Установка стиля графика
# sns.set(style="whitegrid")

# # Подготовка данных и сброс индекса
# real_salary = real_salary.reset_index() if 'Год' in real_salary.index.names else real_salary
# reversed_inflation_data = reversed_inflation_data.reset_index() if 'Год' in reversed_inflation_data.index.names else reversed_inflation_data

# # Создание фигуры и оси
# fig, ax = plt.subplots(figsize=(12, 8))
#             # Проверяем, что 'Год' это колонка, а не индекс
# if 'Год' not in real_salary.columns:
#         real_salary.reset_index(inplace=True)

# if 'Год' not in reversed_inflation_data.columns:
#         reversed_inflation_data.reset_index(inplace=True)

# st.write(real_salary.head())
# st.write(reversed_inflation_data.head())

# # Список видов деятельности и соответствующих цветов
# activities = {
# 'Строительство': 'blue',
# 'Информация и связь': 'green',
# 'Финансовая деятельность': 'orange',
# 'Всего по экономике': 'black'  # Этот тип деятельности будет отображаться жирным пунктиром
# }

# # Построение графика для каждого вида деятельности и инфляции
# for activity, color in activities.items():
#     ax.plot(real_salary['Год'], real_salary[activity],
#             label=activity, color=color, linestyle='-' if activity != 'Всего по экономике' else '--',
#             linewidth=2 if activity == 'Всего по экономике' else 1)

# if 'Инфляция' in reversed_inflation_data.columns:
#     ax.plot(reversed_inflation_data['Год'], reversed_inflation_data['Инфляция'], label='Инфляция', color='red', linestyle='-.', marker='o', markersize=8, linewidth=2)
# else:
#     st.error("Данные об инфляции отсутствуют в DataFrame.")

# # Настройка заголовка, подписей и легенды
# ax.set_title('Динамика изменения реальных зарплат по видам деятельности и уровень инфляции')
# ax.set_xlabel('Год')
# ax.set_ylabel('Изменение зарплаты (%)')
# ax.legend()

# # Показываем график
# st.pyplot(fig)

# ##############################################
# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Установка стиля графика
# sns.set(style="whitegrid")

# # Загрузка и подготовка данных
# # (Эти функции должны быть определены в вашем коде, чтобы загружать и подготавливать данные)
# # salary, inflation_data = load_and_prepare_data()

# # Преобразование инфляции из процентов в десятичные дроби для расчётов
# inflation_data['Инфляция'] = inflation_data['Инфляция'] / 100

# # Создание фигуры и оси
# fig, ax = plt.subplots(figsize=(12, 8))

# # Список видов деятельности и соответствующих цветов
# activities = {
#     'Строительство': 'blue',
#     'Информация и связь': 'green',
#     'Финансовая деятельность': 'orange',
#     'Всего по экономике': 'black'  # Этот тип деятельности будет отображаться жирным пунктиром
# }

# # Построение графика для каждого вида деятельности и инфляции
# for activity, color in activities.items():
#     ax.plot(salary.index, salary[activity],
#             label=activity, color=color, linestyle='-' if activity != 'Всего по экономике' else '--',
#             linewidth=2 if activity == 'Всего по экономике' else 1)

# # Построение графика инфляции
# ax.plot(inflation_data.index, inflation_data['Инфляция'], label='Инфляция', color='red', linestyle='-.', marker='o', markersize=8, linewidth=2)

# # Настройка заголовка, подписей и легенды
# ax.set_title('Динамика изменения реальных зарплат по видам деятельности и уровень инфляции')
# ax.set_xlabel('Год')
# ax.set_ylabel('Изменение зарплаты (%)')
# ax.legend()

# # Показываем график
# st.pyplot(fig)

