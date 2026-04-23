from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
import json
import os

def load_db():
    if not os.path.exists('smartphones.json'):
        return None
    try:
        with open('smartphones.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def find_phone():
    data = load_db()
    if not data:
        showerror("ошибка", "нет файла бд")
        return

    # забираем значения из полей
    s_budget = cb_budget.get()
    s_purpose = cb_purpose.get()
    s_brand = cb_brand.get().lower()
    nfc_req = var_nfc.get()

    # ищем категорию
    category = next((c for c in data['categories'] if c['name'] == s_budget), None)
    if not category:
        showwarning("внимание", "выберите бюджет из списка")
        return

    phone = category['phones'].get(s_purpose)
    if not phone:
        showwarning("внимание", "выберите цель из списка")
        return

    # логика фильтра
    brand_list = [b.lower() for b in phone['brands']]
    brand_ok = s_brand == "любой" or s_brand == "" or s_brand in brand_list
    nfc_ok = not nfc_req or phone['nfc']

    # вывод
    txt_result.config(state=NORMAL)
    txt_result.delete('1.0', END)
    
    if brand_ok and nfc_ok:
        res = f"РЕКОМЕНДАЦИЯ: {phone['name']}\n\nПОЧЕМУ: {phone['reason']}"
    else:
        res = f"ПОД ФИЛЬТРЫ НЕТ СОВПАДЕНИЙ.\n\nЛУЧШИЙ В ЭТОМ БЮДЖЕТЕ: {phone['name']}"
    
    txt_result.insert(END, res)
    txt_result.config(state=DISABLED)

# инициализация окна
root = Tk()
root.title("Smartphone Consultant")
root.geometry("400x550")
root.configure(bg="#ffffff")

# стиль для интерфейса
style = Style()
style.theme_use('clam') 

main_frame = Frame(root, padding=20)
main_frame.pack(fill=BOTH, expand=True)

# настройки полей 
# бюджет
Label(main_frame, text="бюджет (кликни для выбора):").pack(anchor=W, pady=(10,0))
budget_list = ["бюджетный (до 20к)", "оптимальный (20к - 50к)", "высокий (50к - 90к)", "премиальный (от 90к)"]
cb_budget = Combobox(main_frame, values=budget_list)
cb_budget.pack(fill=X, pady=5)

# цель
Label(main_frame, text="цель (кликни для выбора):").pack(anchor=W, pady=(10,0))
purpose_list = ["игры", "работа", "фото", "общее"]
cb_purpose = Combobox(main_frame, values=purpose_list)
cb_purpose.pack(fill=X, pady=5)

# бренд
Label(main_frame, text="бренд (можно вписать или выбрать):").pack(anchor=W, pady=(10,0))
brand_list = ["любой", "Apple", "Samsung", "Xiaomi", "Poco", "Realme", "Google", "OnePlus"]
cb_brand = Combobox(main_frame, values=brand_list)
cb_brand.pack(fill=X, pady=5)

# nfc
var_nfc = BooleanVar()
Checkbutton(main_frame, text="нужен nfc", variable=var_nfc).pack(anchor=W, pady=10)

# кнопка
btn = Button(main_frame, text="ПОДОБРАТЬ", command=find_phone)
btn.pack(fill=X, pady=15)

# поле вывода
txt_result = Text(main_frame, height=8, font=("Arial", 10), state=DISABLED, wrap=WORD, bg="#f4f4f4", relief=FLAT)
txt_result.pack(fill=BOTH, expand=True)

root.mainloop()