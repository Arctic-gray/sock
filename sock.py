import socket #Модуль для работы с сокетами
from datetime import datetime #Используется для расчета времени работы рограммы
import csv #Используется для работы с форматом .csv

start = datetime.now()

#Функция для сканирования портов
def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Создание нового сокета
    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip, port)) #Подключиться к <ip> по <port>
        print('Port:', port, 'is open.') #Для вывода сообщения на экран
        return port #Возвращаем <port>, для последующей записи в файл
        connect.close() #Закрываем соединение
    except:
        pass #Чтобы программа не "вылетала" при достижении таймаута в settimeout()


file_name = input('Введите имя файла (например, text.csv): ')

final = [] #Пустой список, в который будут записаны ip-адреса и открытые порты 

#Открытие файла для работы
with open(file_name) as in_file:
    next(in_file)
    reader = csv.reader(in_file, delimiter=';') #Перебор по строкам в файле; указываем, что разделитель ';'

    for row in reader:
        ip = row[0] #Объект с индексом 0 - ip адрес
        print('For %s:' %ip)
            
        ports = [int(i) for i in row[1].split(',')] #По индексу 1 хранятся порты, разделяем их по ',' и формируем в список ports

        open_ports = [] #Пустой список, в который будут записаны открытые порты
        
        #Сканирование портов
        for i in ports:
            p = scan_port(ip, i)
            if p:
                open_ports.append(p)
                
            #Для вывода сообщения о закрытых портах
            #else:
                #print('Port:', i, 'is closed.')

        #Через функцию map() преобразуем все элементы в open_ports к типу str и добавляем в final ip и открытые порты
        final.append([ip,','.join(map(str, open_ports))])

#Создаем файл connections.csv и открываем его на запись
with open('connections.csv', 'w') as out_file:
    writer = csv.writer(out_file, delimiter=';', lineterminator='\r')
    writer.writerow(['ip-адрес', 'порты'])#первая строка в файле - подписи столбцов
    for i in final:
        writer.writerow(i) #построчно записываем данные из final в connections.csv
    print('Данные были сохранены в connections.csv.')

ends = datetime.now()
print('Time: {}'.format(ends-start))#Выводим время, за которое выполнялась программа

input('Нажмите любую клавишу для выхода...')
