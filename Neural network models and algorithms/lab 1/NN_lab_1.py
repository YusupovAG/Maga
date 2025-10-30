
def table_from_file(name):
    with open(name, 'r') as file:
        headers = file.readline().split('\t')
        table = {}
        for i in range(len(headers)):
            table[headers[i]] = []
        for line in file:
            list_from_line = line.split('\t')
            for i in range(len(headers)):
                if i == 2 or i == 3:
                    table[headers[i]].append(float(list_from_line[i]))
                else:
                    table[headers[i]].append(int(list_from_line[i]))
    return table

table = table_from_file('Абоненты.txt')

# 1 
print(f"Минимальный возраст абонента: {min(table['Возраст'])}")
print(f"Максимальный возраст абонента: {max(table['Возраст'])}")

# 2
call_count_20 = len([call_count for call_count in table['Звонков днем за месяц'] if call_count == 20])
print(f"Cколько абонентов совершило ровно 20 звонков днем за месяц: {call_count_20}")

# 3
age_from_30_to_50 = len([age for age in table['Возраст'] if 30 <= age <= 50])
print(f" Вы отфильтровали исходный набор данных по полю Возраст и вывели данные абонентов от 30 до 50 лет включительно. Ответьте на вопрос, сколько записей прошло через фильтр?: {age_from_30_to_50}")

# 4
table['Всего звонков за месяц'] = [day_calls + evening_calls + night_calls for day_calls, evening_calls, night_calls in zip(table['Звонков днем за месяц'], table['Звонков вечером за месяц'], table['Звонков ночью за месяц'])]
sub_10_index = table['Код'].index(10)
sub_number_10_calls_count = table['Всего звонков за месяц'][sub_10_index]
print(f'Ответьте на вопрос, сколько всего звонков за месяц совершил абонент с кодом 10?: {sub_number_10_calls_count}')
