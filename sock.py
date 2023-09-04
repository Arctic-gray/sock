import socket #Модуль для работы с сокетами
from datetime import datetime #Используется для расчета времени работы рограммы
import csv #Для работы с форматом .csv

start = datetime.now()

#Функция для сканирования портов
def scan_port(ip, port):
    #Создание нового сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#AF - AddressFamily, SOCK_STREAM - socket type - дефолтные значения
    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip, port))#Подключиться к <ip> по <port>
        print('Port:', port, 'is open.')#Для вывода сообщения на экран
        return port #Возвращаем <port>, для последующей записи в файл
        connect.close()#Закрываем соединение
    except:
        pass #Чтобы программа не "вылетала" при достижении таймаута в settimeout()


file_name = input('Введите имя файла (например, text.csv): ')

final = [] #Пустой список, в который будут записаны ip-адреса и открытые порты 

#open(file_name) - открытие файла для работы
#В отличие от open(), где нужно закрыть файл методом close(),
#оператор with закрывает файл для вас, не сообщая об этом.
with open(file_name) as in_file:
    #Используется, когда файл используется в качестве итератора, обычно в цикле,
    # метод next () вызывается повторно, пока не достигнет EOF.
    #Обычно используется с другими методами, например, для чтения
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
                #print('Port:', i, 'is close.')

        #Через функцию map() преобразуем все элементы в open_ports к типу str
        #и добавляем в final ip и открытые порты
        final.append([ip,','.join(map(str, open_ports))])

#Создаем файл connections.csv и открываем его на запись
with open('connections.csv', 'w') as out_file:
    writer = csv.writer(out_file, delimiter=';', lineterminator='\r')# \r - перевод каретки в начало текущей строки
    writer.writerow(['ip-адрес', 'порты'])#первая строка в файле - одписи столбцов
    for i in final:
        writer.writerow(i)
    print('Данные были сохранены в connections.csv.')

ends = datetime.now()
print('Time: {}'.format(ends-start))#Выводим время, за которое выполнялась рограмма

input('Нажмите любую клавишу для выхода...')
