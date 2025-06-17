import tkinter as tk
import random
import json

colora = "#fffbff"
colorb = "#fe5d9f"
colorc = "#28262b"
colord = "#28262b"
colox = "#84ff3d"

class TkinterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guess the Word Game")
        self.geometry("720x480")
        self.resizable(True, True)
        self.config(background=colorb)

        try:
            icon = tk.PhotoImage(file='images\\WU_logo.png')
            self.iconphoto(True, icon)
        except:
            pass

        try:
            with open("categories.json", "r") as f:
                self.categories = json.load(f)
        except Exception as e:
            self.categories = {}
            print("Could not load categories.json:", e)

        self.selected_button_index = None
        self.category_buttons = []
        self.play_again_button = None

        self.create_widgets()

    def create_widgets(self):
        self.container = tk.Frame(self, bg=colorb)
        self.container.pack(expand=True, anchor="center")

        self.label = tk.Label(self.container, text="Welcome to the Guess the Word Game!",
                              font=("Goudy old style", 20), bg=colorb, fg=colora)
        self.label.pack(pady=0.3)

        self.start_button = tk.Button(self.container, text="Start Game", command=self.start_game,
                                      bg=colorc, fg=colora, font=("century gothic", 14))
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(self.container, text="Quit", command=self.quit,
                                     bg=colorc, fg=colora, font=("century gothic", 14))
        self.quit_button.pack(pady=10)

    def start_game(self):
        self.container.pack_forget()
        self.label.pack_forget()
        self.start_button.pack_forget()
        self.quit_button.pack_forget()

        self.main_area = tk.Frame(self, bg=colorb)
        self.main_area.pack(expand=True, anchor="center")

        self.label = tk.Label(self.main_area, text="Choose a Category:",
                              font=("Goudy old style", 20), bg=colorb, fg=colora)
        self.label.pack(pady=20)

        self.grid_frame = tk.Frame(self.main_area, bg=colorb)
        self.grid_frame.pack(anchor="center")

        self.category_buttons.clear()
        columns = 4

        for idx, category in enumerate(self.categories):
            row = idx // columns
            col = idx % columns
            btn = tk.Button(
                self.grid_frame,
                text=category.capitalize(),
                font=("Arial", 12, "bold"),
                bg=colord,
                fg=colora,
                relief="ridge",
                bd=2,
                padx=12,
                pady=6,
                command=lambda i=idx: self.select_category(i)
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            self.category_buttons.append(btn)

        self.next_button = tk.Button(self.main_area, text="Next", state="disabled",
                                     font=("Arial", 14), bg="#bbb", fg="white",
                                     command=self.confirm_selection)
        self.next_button.pack(pady=10)

    def select_category(self, index):
        if self.selected_button_index is not None:
            prev_btn = self.category_buttons[self.selected_button_index]
            prev_btn.config(bg=colord, fg=colora)

        self.selected_button_index = index
        selected_btn = self.category_buttons[index]
        selected_btn.config(bg=colorb, fg="black")
        self.next_button.config(state="normal", bg="black")

    def confirm_selection(self):
        self.grid_frame.pack_forget()
        if self.selected_button_index is not None:
            selected_category = list(self.categories.keys())[self.selected_button_index]
            self.next_button.pack_forget()
            for btn in self.category_buttons:
                btn.grid_forget()
            self.start_word_game(selected_category)
        else:
            print("No category selected!")

    def start_word_game(self, category):
        self.word = random.choice(self.categories[category])
        self.wordlen = len(self.word)
        self.attempt = 1
        self.points = 0

        self.label.config(text=f"Guess the word from: {category.capitalize()}")

        self.word_frame = tk.Frame(self, bg=colorb)
        self.word_frame.pack(pady=20, anchor="center")

        self.hint_text = "— " * self.wordlen
        self.hint_label = tk.Label(self.main_area, text=self.hint_text,
                                   font=("Arial", 18), bg=colorb, fg=colora)
        self.hint_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.main_area, font=("Arial", 14))
        self.guess_entry.pack(pady=10, anchor="center")

        self.guess_button = tk.Button(self.main_area, text="Guess",
                                      command=self.check_guess,
                                      bg=colorc, fg=colora, font=("Arial", 12))
        self.guess_button.pack(pady=10, anchor="center")

    def check_guess(self):
        guess = self.guess_entry.get().strip().lower()
        if guess == self.word:
            if self.attempt == 1:
                self.points = 5
                msg = "Correct on first try!"
            elif self.attempt == 2:
                self.points = 2
                msg = "Correct on second try!"
            else:
                self.points = 1
                msg = "Correct on last try!"

            self.label.config(text=f"{msg} Word: {self.word} | Points: {self.points}")
            self.word_frame.destroy()
            self.show_play_again()
            return

        self.attempt += 1

        if self.attempt == 2:
            self.hint_text = self.word[0] + "— " * (self.wordlen - 1)
        elif self.attempt == 3:
            self.hint_text = ""
            for idx, char in enumerate(self.word):
                if char in "aeiou" or idx == self.wordlen - 1:
                    self.hint_text += char
                else:
                    self.hint_text += "— "
        else:
            self.label.config(text=f"No more tries. Word was: {self.word}")
            self.word_frame.destroy()
            self.show_play_again()
            return

        self.hint_label.config(text=self.hint_text)
        self.guess_entry.delete(0, tk.END)

    def show_play_again(self):
        if self.guess_entry:
            self.guess_entry.destroy()
        if self.guess_button:
            self.guess_button.destroy()
        if self.hint_label:
            self.hint_label.destroy()

        self.play_again_button = tk.Button(self.main_area, text="Play Again",
                                           font=("Arial", 14),
                                           bg=colorc, fg=colora,
                                           command=self.restart_game)
        self.play_again_button.pack(pady=20)

    def restart_game(self):
        self.play_again_button.destroy()
        self.main_area.destroy()
        self.selected_button_index = None
        self.create_widgets()


root = TkinterApp()
root.mainloop()
