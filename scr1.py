# Импортируем необходимые модули
from tkinter import *  # библиотекa для разработки графического интерфейса
import geocoder  # библиотека для геокодирования
from tkcalendar import Calendar, DateEntry  # модуль для создания календаря и списка
from tkinter import Label, Tk, ttk  # для создания кнопок
from PIL import Image, ImageTk  # библиотека для исспользования изображений
import requests  # библиотека для работы с запросами
from tkinter import font  # для установки шрифтов

# import smtplib # для отправки почты
from datetime import timedelta  # для установки нитервала времени
from datetime import datetime  # для установки даты

# from datetime import *
import os  # для работы с файловой системой ПК
import runpy  # для запуска модулей из файловой системы.

# Текст информации о приложении
sring_my = """\n\n\n\nHello!\n\nI am called to rescue you from the hellish chaos of life. Where you can define your path, divide it into stages, understand the possibilities of time and your pace. And what is very important, you can see all the work done and admire yourself.\n\nI'll always keep you posted."""
# Вводим словарь действий и привязываем к ним иконки
type_to_image = {
    "programming": Image.open("pc.png"),
    "health": Image.open("m.png"),
    "erudition": Image.open("cr.png"),
    "work": Image.open("money.png"),
    "cleanliness": Image.open("c.png"),
}
# Создаем пустой словарь для раскраски запланированных дней в планере
dict_greener = {}


# Инициируем необходимые классы
# Инициируем класс виджета с инструментами


class Tooltip:
    def __init__(
        self, widget, text
    ):  # Конструктор класса Tooltip, который принимает виджет (widget) и текст (text) для отображения
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(
        self, event=None
    ):  # позволяет создавать виджет с указанным текстом (text) при наведении курсора (<Enter>),
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(
            self.tooltip,
            text=self.text,
            background="white",
            relief="solid",
            borderwidth=0,
        )
        label.pack()

    def hide(self, event=None):  # для закрывания виджета при уходе курсора (<Leave>).
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# Инициируем класс окна
class ScrollableFrame(ttk.Frame):
    def __init__(
        self, container, *args, **kwargs
    ):  # Конструктор класса, который наследуется от ttk.Frame.
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(
            self, bg="white"
        )  # Создает холст (Canvas) для отображения содержимого с белым фоном.
        self.canvas.pack(fill=BOTH, expand=True)
        scrollbar = Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            bg="green",
            bd=0,
            troughcolor="white",
        )  # Создает вертикальный ползунок для прокрутки, связанный с холстом.
        self.scrollable_frame = Frame(
            self.canvas, bg="white"
        )  # Создает внутренний фрейм, который будет содержать прокручиваемое содержимое.

        # Привязка событий
        self.scrollable_frame.bind("<Configure>", self.OnFrameConfigure)

        # Настройка виджетов
        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", self.FrameWidth)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        root.bind_all("<MouseWheel>", self._on_mousewheel)

    def FrameWidth(
        self, event
    ):  # обновляет ширину внутреннего фрейма в соответствии с изменением ширины холста.
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def OnFrameConfigure(self, event):  # обновляет область прокрутки холста
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(
        self, event
    ):  # прокрутки содержимого вертикально при использовании колеса мыши.
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Работа с календарем удаление
def updateLabel(a):
    list_menus = {}
    if (
        os.stat("settings.txt").st_size > 5
    ):  # Проверяется размер файла "settings.txt". Если размер больше 5 байт, вызывается функция get_schedule().
        get_schedule()  # Запускаем функцию планера
    labelblue.config(text="Selected Date: " + tkc.get_date(), font=85)
    for (
        i
    ) in (
        frame3.winfo_children()
    ):  # удаляет содержимое виджета frame3                                   #тут др фрейм
        i.destroy()
    curr_date = tkc.get_date()  # Получает  дату и сохраняет ее в переменную curr_date.
    dict_for_variables = {}

    scrollbar = ScrollableFrame(
        frame3
    )  # Создается экземпляр класса ScrollableFrame и упаковывается в frame3
    scrollbar.pack(fill=BOTH, expand=True)

    if (
        curr_date in dict_
    ):  # Проверяем выбранный в календаре день на наличие его в справочнике с сохраненными задачами
        for i in range(
            len(dict_[curr_date])
        ):  # Проходим циклом по всему справочнику - отбираем задачи на этот день
            dict_for_variables[curr_date] = dict_for_variables.get(curr_date, []) + [
                IntVar()
            ]  # Получаем список переменных в отдельный список
            dict_for_variables[curr_date][i].set(
                dict_[curr_date][i][-1]
            )  # Копируем построчно
            list_menus[curr_date] = list_menus.get(curr_date, []) + [
                [IntVar(), IntVar()]
            ]  # Формируем список для меню
        for i in range(len(dict_[curr_date])):  # Восстановление окна с задачами
            current_task = dict_[curr_date][i][0]  # Формируем списолк задач на дату
            # Помещаем задачи в фрейм для визуализации
            curr_frame = Frame(
                scrollbar.scrollable_frame,
                background="white",
                borderwidth=0,
                highlightthickness=0,
                bd=0,
            )
            curr_frame.pack(side="top", fill=X)

            def callBackFunc():  # обновление всех галочек по текущей дате
                print("функция работает исправно")
                n = 0
                print("dict_for_variables", dict_for_variables)
                for i in range(len(dict_[curr_date])):
                    dict_[curr_date][n][-1] = dict_for_variables[curr_date][n].get()
                    n += 1

            def greener():  # Функция раскрашивания календаря (на будущее)
                # Задаем справочник палитры цветов
                rgb = [
                    (144, 223, 144),
                    (118, 216, 118),
                    (94, 209, 94),
                    (73, 203, 73),
                    (56, 195, 56),
                    (51, 177, 51),
                    (46, 159, 46),
                    (41, 143, 41),
                    (37, 129, 37),
                    (33, 116, 33),
                    (30, 104, 30),
                ]
                # Справочник дат с соответствующими цветами закрашивания
                dict_greener[curr_date] = dict_greener.get(curr_date, []) + rgb
                step_color = len(dict_[curr_date]) // len(rgb)
                _from_rgb(rgb)
                current_color = _from_rgb(
                    rgb[sum([i[-1] for i in dict_[curr_date]]) // step_color]
                )
                # Закрашиваем календарь
                green_event = tkc.calevent_create(
                    date=curr_date, text="greener", tags="tag"
                )
                tkc.tag_config("tag", background=current_color, foreground="white")

            # Создается флажок (Checkbutton), который представляет собой отдельную задачу.
            current_task = Checkbutton(
                curr_frame,
                text=current_task,
                font=45,
                bg="white",
                variable=dict_for_variables[curr_date][i],
                onvalue=1,
                offvalue=0,
                highlightthickness=0,
                bd=0,
                command=greener,
            )  # command= callBackFunc aaaaaaaaaaaaaaaaaaaaa Checkbutton.command

            def delete():  # Функция для удаления задачи
                for i in range(len(list_menus[curr_date])):
                    if list_menus[curr_date][i][0].get() == 1:
                        del dict_[curr_date][i]
                        scrollbar.scrollable_frame.winfo_children()[i].destroy()

            # Создаем кнопки меню
            menubutton = Menubutton(curr_frame, text="...", bg="white")
            menubutton.menu = Menu(menubutton)
            menubutton["menu"] = menubutton.menu  # Кнопка Меню
            deletebtn = menubutton.menu.add_checkbutton(
                label="Delete", variable=list_menus[curr_date][i][0], command=delete
            )  # Кнопка Удалить

            def description(
                event,
            ):  # отображение  описания задачи при наведении курсора на соответствующий виджет
                numb = 0
                for curr_frame in scrollbar.scrollable_frame.winfo_children():
                    for widget in curr_frame.winfo_children():
                        if event.widget == widget:
                            result_numb = numb
                    numb += 1

                Tooltip(event.widget, dict_[curr_date][result_numb][-2])

            # Настройка метки текущих задач
            current_task.bind("<Enter>", description)
            current_task["command"] = callBackFunc
            current_task.pack(side="left", padx=7)

            # добавлям изображение к задачам
            img = type_to_image[dict_[curr_date][i][1]]  # Image.open('mass.png')
            resized_image = img.resize((30, 30))  #
            photo = ImageTk.PhotoImage(resized_image)  #
            lab = Label(curr_frame, image=photo)  #
            lab.image = photo
            lab.pack(side="right")
            menubutton.pack(side="right")


# Запуск приветственного окна с информацией пользователю о приложении
def hello():
    global tkc
    hello = Toplevel(root)
    root["bg"] = "white"
    hello.title("Hellper_2.0")
    hello.geometry("1000x480")
    frame1 = Frame(hello, bg="white", width=200, height=200)
    frame1.pack(fill=BOTH, expand=True, side="left")
    frame2 = Frame(hello, bg="white", width=200, height=200)
    frame2.pack(fill=BOTH, expand=True, side="left")
    global icon1
    Label(frame1, image=icon1, bg="white").pack(fill=BOTH, expand=True, padx=12)
    global my_font
    noteditor = Text(
        frame2,
        wrap="word",
        bg="white",
        font=my_font,
        highlightthickness=0,
        borderwidth=0,
        height=14,
    )
    noteditor.pack(fill=BOTH, expand=1, padx=35)
    global sring_my
    noteditor.insert(7.0, sring_my)
    noteditor.config(state=DISABLED)

    def open_settings():  # Задаем настройки для окна планера
        global tkc
        hello.withdraw()
        settings_window()

    frame3 = Frame(frame2, bg="green", width=200, height=100)
    frame3.pack(fill=BOTH, expand=True, side="bottom")
    global my_font2
    # Задаем кнопку "Настройки"
    btn = Button(
        frame3,
        bg="white",
        text="start settings",
        font=my_font2,
        foreground="red",
        justify=RIGHT,
        command=open_settings,
        highlightthickness=0,
        borderwidth=0,
    )
    btn.configure(width=200, height=100)
    btn.pack(anchor="se")


# Загружаем сохраненный календарь пользователя + основные параметры
def get_schedule(
    *A,
):  # работа над заполнением рабочих дней функция проставляет даты рабочих дней при загрузке
    with open("settings.txt") as fe:  # загружаем из файла
        print('os.stat("settings.txt").st_size ', os.stat("settings.txt").st_size)
        if (
            os.stat("settings.txt").st_size > 5
        ):  # Если в файле есть хоть 1 стрка настроек (5 элементов) то открываем файл
            text = fe.read()
            print("text = ", text)
            settings_list = eval(text)
        else:
            settings_list = (
                []
            )  # Если файл пустой, то создаем пустой справочник для сохранения настроек
    tkc.calevent_remove()  # удаляет все события календаря. можно указать список необходимых к удаленю
    print("settings_list ==", settings_list)
    # Берем из справочника дату (4 элемент в списке)
    date = datetime(*map(int, settings_list[3].split("-")))
    # Выбранный элемент
    selected = settings_list[2]
    #
    date_last = date + timedelta(days=int(selected.split("/")[-1]) + 1)
    step = int(selected.split("/")[-1])
    # Заполняем календарь из справочника
    for i in range(130):
        for j in range(int(selected.split("/")[0])):
            work_event = tkc.calevent_create(date=date_last, text="WorkDay", tags="tag")
            tkc.tag_config("tag", background="azure2", foreground="dodgerblue4")
            date_last = date_last + timedelta(days=1)
        date_last = date_last + timedelta(days=step)
    tkc.update()


# settings window
def settings_window():
    global tkc
    settings.deiconify()
    frame1 = Frame(settings, bg="white")
    frame1.pack()
    title = Label(
        frame1,
        text="Settings",
        font=my_font2,
        bg="white",
        highlightthickness=0,
        bd=0,
        pady=15,
    ).pack()
    frame_email = Frame(settings, bg="white", width=200, height=100)
    frame_email.pack(fill=BOTH, expand=True)
    title = Label(
        frame_email,
        text="Enter your mail: ",
        font=my_font,
        bg="white",
        highlightthickness=0,
        bd=0,
        pady=15,
    ).pack(side=LEFT, fill=X)
    entry1 = Entry(frame_email, width=30)
    entry1.pack(side=LEFT, fill=X)
    frame_name = Frame(settings, bg="white", width=200, height=100)
    frame_name.pack(fill=BOTH, expand=True)
    title = Label(
        frame_name,
        text="Enter your name: ",
        font=my_font,
        bg="white",
        highlightthickness=0,
        bd=0,
        pady=15,
    ).pack(side=LEFT, fill=X)
    entry2 = Entry(frame_name, width=30)
    entry2.pack(side=LEFT, fill=X)
    frame_work = Frame(settings, bg="white", width=200, height=100)
    frame_work.pack(fill=BOTH, expand=True)
    title = Label(
        frame_work,
        text="Сhoose your work schedule: ",
        font=my_font,
        bg="white",
        highlightthickness=0,
        bd=0,
        pady=15,
    ).pack(side=LEFT, fill=X)
    counter = 0

    def select(selected):  # cоздаем поле для заполнения рабочего времени.
        nonlocal counter
        counter += 1
        if counter > 1:
            frame_worktime.destroy()
        frame_worktime = Frame(settings, bg="white", width=200, height=100)
        frame_worktime.pack(side=LEFT, fill=X)
        title = Label(
            frame_worktime,
            text="Set your worktime (08:00 20:00): ",
            font=my_font,
            bg="white",
            highlightthickness=0,
            bd=0,
            pady=15,
        ).pack(side=LEFT, fill=X)
        entry_start = Entry(frame_worktime)
        entry_start.pack(side=LEFT, fill=X)
        entry_end = Entry(frame_worktime)
        entry_end.pack(side=LEFT, fill=X)
        title = Label(
            frame_worktime,
            text="Last workday: ",
            font=my_font,
            bg="white",
            highlightthickness=0,
            bd=0,
            pady=15,
        ).pack(side=LEFT, fill=X)
        datentry = DateEntry(frame_worktime)
        datentry.pack(side=LEFT, fill=X)

        def saving_and_destroy():
            settings_list = [
                entry1.get(),
                entry2.get(),
                btn.get(),
                str(datentry.get_date()),
                entry_start.get(),
                entry_end.get(),
            ]
            with open(
                "settings.txt", mode="w"
            ) as f:  # Записываем список задач в "settings.txt"
                f.write(str(settings_list))
            get_schedule()
            settings.withdraw()
            updateLabel("a")
            root.deiconify()

        btnn = Button(
            frame_worktime, text="OK", padx=30, command=saving_and_destroy
        ).pack(side=RIGHT, fill=BOTH)

    btn = StringVar()

    def f():
        selected = btn.get()
        select(selected)

    list_ = ["5/2", "1/3", "2/2"]
    for schedule in list_:
        schedule = Radiobutton(
            frame_work,
            text=schedule,
            value=schedule,
            variable=btn,
            command=f,
            bg="white",
        )
        schedule.pack(side=LEFT, fill=X)


def func():  # Определяет геолокацию и погоду
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    g = geocoder.ip("me")
    city = g.latlng
    # Параметры запроса
    params = {
        "latitude": city[0],  # широта
        "longitude": city[1],  # долгота
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",  # минимальная и максимальная температура, сумма осадков
        "timezone": "Europe/Moscow",
    }  # временная зона для Краснодара
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    user_name["text"] = (
        str(g.city) + " : " + str(data["daily"]["temperature_2m_max"][1])
    )


number = 0
position = 0
dict_ = {}


# Функция добавления задачи в календарь
def func1():
    stroka = tkc.get_date()
    newWindow = Toplevel(root)
    newWindow.title("Add your task/goal")
    newWindow.geometry("700x300")
    class_tasks = ["Goal", "Task"]  # Список для типа задачи
    combobox = ttk.Combobox(
        newWindow, values=class_tasks
    )  # Типы задача или цель получаем из списка созданного ранее
    combobox.pack()
    combobox.insert(0, "Task")

    def goal_or_task(a, b=False):  # Функция работы с целью или задачей

        if combobox.get() == "Task":
            for i in newWindow.winfo_children()[1:]:  # тут др фрейм
                i.destroy()

            def fetch():
                if tasky.get():
                    task_name, task_type = tasky.get(), combobox1.get()
                    global number
                    dict_[stroka] = dict_.get(stroka, []) + [
                        [task_name, task_type, editor.get(1.0, END), False]
                    ]
                    number += 1
                    updateLabel("a")
                    record_()
                    newWindow.destroy()
                newWindow.destroy()

            newWindow.update()
            frameall = Frame(newWindow, background="white")
            frameall.pack(fill=BOTH, expand=True)
            framegv = Frame(frameall, background="white")
            framegv.pack(side=LEFT, fill=BOTH, expand=True)
            frame11 = Frame(framegv, background="white")
            frame11.pack(fill=BOTH, expand=True)
            taskname = Label(frame11, text="Set the task", bg="white")
            taskname.pack(side=LEFT, fill=BOTH)
            tasky = Entry(frame11, width=35)
            tasky.pack(side=LEFT)
            frame22 = Frame(framegv, background="white")
            frame22.pack(fill=BOTH, expand=True)
            frame33 = Frame(frameall, background="white")
            frame33.pack(side=RIGHT, fill=BOTH, expand=True)
            task_description = Label(frame33, text="Task_description", bg="white")
            task_description.pack(side=TOP, fill=X)
            editor = Text(
                frame33, width=25, height=5, bg="darkgreen", fg="white", wrap=WORD
            )
            editor.pack(fill=BOTH, expand=1)
            types_of_tasks = Label(frame22, text="Set the type", bg="white")
            types_of_tasks.pack(side=LEFT, fill=BOTH)
            tasks_types = ["programming", "health", "erudition", "work", "cleanliness"]
            combobox1 = ttk.Combobox(frame22, values=tasks_types, background="white")
            combobox1.pack(side=LEFT)
            Button(newWindow, text="add task", command=fetch).pack(anchor="se")
            newWindow.protocol(
                "WM_DELETE_WINDOW", updateLabel("a")
            )  # close window trigger
        elif combobox.get() == "Goal":
            newWindow.update()

    goal_or_task("a", b=True)
    combobox.bind("<<ComboboxSelected>>", goal_or_task)


# Сохранение календаря
def record():
    with open("your_story.txt", "w") as f:
        data = str(dict_)
        f.write(data)
        root.destroy()


def record_():
    with open("your_story.txt", "w") as f:
        data = str(dict_)
        f.write(data)


def read_dict():
    print('os.stat("settings.txt").st_size ', os.stat("settings.txt").st_size)
    isempty = os.stat("your_story.txt").st_size
    print("isempty", isempty)
    if isempty != 0:
        with open("your_story.txt") as f:
            global dict_
            dict_ = eval(f.readlines()[0])


if __name__ == "__main__":

    read_dict()
    root = Tk()
    root.title("Hellper_2.0")
    root["bg"] = "#fafafa"
    icon = PhotoImage(file="aaa.png")
    icon1 = PhotoImage(file="bb.png")
    root.iconphoto(True, icon)
    root.wm_attributes("-alpha", 1)
    root.geometry("980x400")
    # create settings window:
    settings = Toplevel(root)
    root["bg"] = "white"
    settings.title("Hellper_2.0")
    settings.geometry("1000x480")
    root.protocol("WM_DELETE_WINDOW", record)

    root.wm_withdraw()  # скрываем окно до окончания настройки

    settings.wm_withdraw()  # скрываем окно до окончания настройки
    my_font2 = font.Font(family="Arial", size=17, weight="bold")
    my_font = font.Font(family="Arial", size=17, weight="normal")
    if os.stat("settings.txt").st_size < 5:
        hello()
    else:
        root.deiconify()
    frame = Frame(root, bg="white", width=200, height=200)
    frame.pack(fill=BOTH, expand=True, side=RIGHT)

    current_font = font.Font(weight="bold", size=13)
    dt_now = str(datetime.now()).split()[0].split("-")
    tkc = Calendar(
        frame,
        selectmode="day",
        year=int(dt_now[0]),
        month=int(dt_now[1]),
        date=int(dt_now[2]),
        foreground="darkorange1",
        font=current_font,
        background="white",
        bordercolor="azure2",
        headersbackground="white",
        weekendbackground="white",
        othermonthbackground="floralwhite",
        weekendforeground="black",
        othermonthwebackground="floralwhite",
        showweeknumbers=False,
        day=int(dt_now[2]),
        disabledselectbackground="yellow",
        disabledselectforeground="blue",
        disableddaybackground="pink",
        selectbackground="green",
    )
    tkc.pack(fill="both", expand=True, padx=17, pady=4)
    tkc.bind("<<CalendarSelected>>", updateLabel)  # нажатие на дату

    frame1 = Frame(root, bg="white", width=200, height=200)
    frame1.pack(fill=BOTH, expand=True, side=RIGHT)
    frame4 = Frame(frame1, bg="white")
    frame4.pack(side="top", fill=X)
    frame3 = Frame(frame1, bg="white")
    frame3.pack(side=TOP, fill=BOTH, expand=True)
    btn1 = Button(frame4, text="ADD", bg="white", command=func1)
    btn1.pack(side=LEFT)
    labelblue = Label(frame4, text="Selected Date: ", font=40, bg="white")
    labelblue.pack(side=LEFT)
    labelblue.config(text="Selected Date: " + tkc.get_date(), font=85)

    # Для погоды по геолокации
    image = Image.open("picture.png")
    resized_image = image.resize((28, 28))
    photo = ImageTk.PhotoImage(resized_image)

    # фрейм с погодой
    frame2 = Frame(frame, bg="white", width=100, height=100)
    frame2.pack(side="top", fill=X, pady=13)

    # кнопка с фото
    btn = Button(frame2, text="Создать задачу", bg="white", image=photo, command=func)
    btn.configure(width=28, height=28)
    btn.pack(side=LEFT, padx=17, pady=1)

    user_name = Label(
        frame2, text="wheather", font=25, bg="white", highlightthickness=0, bd=0
    )
    user_name.pack(side=LEFT)
    my_font2 = font.Font(family="Arial", size=10, weight="bold")

    # функция отправки почты
    # модуль с моделью генерации текста письма вынесен в отдельный файл
    def send_mail():
        runpy.run_module(mod_name="email_and_ml")  # запускаем  модель

    btn_for_email = Button(
        frame2,
        text="Send mail",
        bg="white",
        highlightthickness=2,
        bd=1,
        font=my_font2,
        command=send_mail,
    )
    btn_for_email.config(
        highlightbackground="blue violet", highlightcolor="blue violet"
    )
    btn_for_email.pack(side=RIGHT, padx=19)
    btn.invoke()  # кнопка  нажатие
    print("cick")

    updateLabel("a")

    root.mainloop()

else:

    def summa(a, b):
        print("undirect run")
        return a + b
