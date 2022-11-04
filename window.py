import tkinter
import main
import dotenv


class MyWindow:
    def __init__(self, win, title):
        self.window = win
        self.title = title
        boxes = [
            "reddit_client_id",
            "reddit_client_secret",
            "reddit_user_agent",
            "reddit_username",
            "reddit_password",
            "subreddit",
            "flair",
            "limit",
            "time_filter"
        ]
        hidden_boxes = [
            "reddit_client_id",
            "reddit_client_secret",
            "reddit_user_agent",
            "reddit_password",
        ]
        self.label_entry_dict = {}
        config = dotenv.dotenv_values(".env")
        index = 0
        for index, name in enumerate(boxes):
            tkinter.Label(win, text=f'{name}: ').place(x=10, y=10 + 25 * index)
            entry_box = tkinter.Entry(win, show="*" if name in hidden_boxes else "")
            entry_box.insert(0, config.get(name))
            entry_box.place(x=150, y=10 + 25 * index)
            self.label_entry_dict[name] = entry_box
        tkinter.Button(window, text='Save', fg='black', bg='white',
                       command=self.save, height=1, width=7).place(x=250, y=10 + 25 * (index + 1))
        tkinter.Button(window, text='Run', fg='black', bg='white',
                       command=self.run, height=1, width=7).place(x=150, y=10 + 25 * (index + 1))

    def save(self):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        for key, value in self.label_entry_dict.items():
            response = value.get()
            dotenv.set_key(dotenv_file, key, response)

    def run(self):
        self.save()
        main.main()

    def start(self, geometry):
        self.window.geometry(geometry)
        self.window.mainloop()


if __name__ == '__main__':
    window = tkinter.Tk()
    my_win = MyWindow(window, 'Hello Python')
    my_win.start("400x300+10+10")
