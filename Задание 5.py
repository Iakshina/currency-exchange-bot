import tkinter as tk
from mimetypes import init
from tkinter import ttk

import git
import requests


CURRENCY_NAMES = {
    "EUR": "Евро",
    "USD": "Американский доллар",
    "RUB": "Российский рубль",
    "GBP": "Фунт стерлингов",
    "JPY": "Японская йена",
    "CNY": "Китайский юань"
}


class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы обмена валют")
        self.root.geometry("350x500")

        # Валюта 1
        self.label_base1 = tk.Label(root, text="Базовая валюта 1", font=("Arial", 10, "bold"))
        self.label_base1.pack(pady=(20, 5))

        self.combo_base1 = ttk.Combobox(root, values=list(CURRENCY_NAMES.keys()), state="readonly")
        self.combo_base1.current(0)  # EUR по умолчанию
        self.combo_base1.pack()

        self.name_base1 = tk.Label(root, text=CURRENCY_NAMES["EUR"])
        self.name_base1.pack(pady=(0, 15))
        self.combo_base1.bind("<<ComboboxSelected>>", self.update_names)

        # Валюта 2
        self.label_base2 = tk.Label(root, text="Вторая базовая валюта", font=("Arial", 10, "bold"))
        self.label_base2.pack(pady=(10, 5))

        self.combo_base2 = ttk.Combobox(root, values=list(CURRENCY_NAMES.keys()), state="readonly")
        self.combo_base2.current(1)  # USD по умолчанию
        self.combo_base2.pack()

        self.name_base2 = tk.Label(root, text=CURRENCY_NAMES["USD"])
        self.name_base2.pack(pady=(0, 15))
        self.combo_base2.bind("<<ComboboxSelected>>", self.update_names)

        # Целевая валюта
        self.label_target = tk.Label(root, text="Целевая валюта", font=("Arial", 10, "bold"))
        self.label_target.pack(pady=(10, 5))

        self.combo_target = ttk.Combobox(root, values=list(CURRENCY_NAMES.keys()), state="readonly")
        self.combo_target.current(2)  # RUB по умолчанию
        self.combo_target.pack()

        self.name_target = tk.Label(root, text=CURRENCY_NAMES["RUB"])
        self.name_target.pack(pady=(0, 20))
        self.combo_target.bind("<<ComboboxSelected>>", self.update_names)


        self.btn_get = tk.Button(root, text="Получить курс обмена", command=self.exchange,
                                 bg="#f0f0f0", padx=10, pady=5)
        self.btn_get.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", justify="left")
        self.result_label.pack(pady=20)

    def update_names(self, event=None):
        self.name_base1.config(text=CURRENCY_NAMES.get(self.combo_base1.get(), ""))
        self.name_base2.config(text=CURRENCY_NAMES.get(self.combo_base2.get(), ""))
        self.name_target.config(text=CURRENCY_NAMES.get(self.combo_target.get(), ""))

    def exchange(self):
        base1 = self.combo_base1.get()
        base2 = self.combo_base2.get()
        target = self.combo_target.get()


        url = "https://open.er-api.com/v6/latest/USD"

        try:
            response = requests.get(url)
            data = response.json()

            if data["result"] == "success":
                rates = data["rates"]

                def get_rate(from_curr, to_curr):
                    if from_curr == to_curr:
                        return 1.0

                    rate_from = rates.get(from_curr, 1)
                    rate_to = rates.get(to_curr, 1)
                    return rate_to / rate_from

                res1 = get_rate(base1, target)
                res2 = get_rate(base2, target)

                text = (f"1 {base1} = {res1:.2f} {target}\n"
                        f"1 {base2} = {res2:.2f} {target}")

                self.result_label.config(text=text, fg="green")
            else:
                self.result_label.config(text="Ошибка API", fg="red")

        except Exception as e:
            self.result_label.config(text=f"Ошибка соединения:\n{e}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()