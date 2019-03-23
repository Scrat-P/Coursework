# Сетевой графический ASCII-арт редактор

#### Команда:

+ Баранович Павел
+ Юревич Андрей

#
#### Описание проекта:

Проект представляет собой клиент-серверное приложение. 

На клиентской части пользователь может воспользоваться оконным интерфейсом для рисования и редактирования различных растровых изображений. Интерфейс поддерживает рисование прямых, изогнутых и ломаных линий (с регулировкой толщины и цвета линий), различных геометрических фигур (окружность, эллипс, квадрат, прямоугольник, пятиконечная звезда и некоторые другие виды многоугольников), выделения определённой области с последующими операциями над ней (увеличения в размерах, зеркального отражения и вращения вокруг центра), копирование и вставка фрагментов изображения, масштабирование, заливка замкнутых фигур цветом, сохранение и загрузка уже готовых изображений. 

На серверной - пользователь видит в онлайн режиме изменения производимые на клиентской части. Эти изменения отображаются в виде цветного ASCII-арта (отображаемого в консоли), в который переводится изображение клиента. Пользователь может сохранить данный ASCII-арт себе на компьютер в виде изображения в формате BMP. 

Для ускорения передачи данных и обеспечения синхронизации обмен данными будет производится через самописный простейший протокол TCP, который реализуется на основе UDP протокола, устанавливает соединение с сервером, посредством локальной сети (IP адрес и порт заранее заданы), разбивает информацию на пакеты заданной длины, осуществляет повторный запрос данных в случае их потери, собирает пакеты в порядке их отправки и устраняет дублирование при получении двух копий одного и того же пакета.

#
#### Project description:

The project is a client-server application. 

On the client side, user can use the window interface to draw and edit various bitmaps. The interface supports drawing straight, curved and broken lines (with adjustable line thickness and color), various geometric shapes (circle, ellipse, square, rectangle, five-pointed star and some other types of polygons), selection of a certain area with subsequent operations on it (increase in size, mirror reflection and rotation around the center), copy and paste image fragments, scaling, fill closed shapes with color, save and load ready-made images. 

On the server, user sees online changes made on the client side. These changes are displayed as a color ASCII-art (displayed in the console), which translates the image of the client. The user can save the ASCII art to your computer as an image in BMP format. 

To speed up data transfer and ensure synchronization, data exchange will be carried out through the self-written simple TCP Protocol, which is implemented on the basis of UDP Protocol, establishes a connection to the server through a local network (IP address and port are pre-defined), splits the information into packets of a given length, re-queries the data in case of loss, collects the packets in the order they are sent and eliminates duplication when receiving two copies of the same packet.
