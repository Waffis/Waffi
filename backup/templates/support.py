import sqlite3
import os
import db 
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox


#db.create_db()
def confirm():
    
    problem= problem_textfeld.get("1.0","end").strip()
    solution= solution_textfeld.get("1.0","end").strip()
    img=image_feld.get("1.0","end").strip()
    if problem and solution:
        problems= db.search_problem()
        for p in problems:
            if problem == p:
                messagebox.showwarning("WARNING", "there is the same problem!")
                return
            
        db.insert_db(problem,solution,img)
        messagebox.showwarning("WARNING", "Done!")
        problem_textfeld.delete("1.0",ctk.END)
        solution_textfeld.delete("1.0",ctk.END)
        image_feld.delete("1.0",ctk.END)
        
    else:
        messagebox.showwarning("WARNING", "Please write the Problem and the Solution")

def on_closing():
        app.destroy()
def show_problems():
    app.withdraw()
    window_select.deiconify()
    window_select.protocol("WM_DELETE_WINDOW", on_closing)

    # استرجاع المشاكل من قاعدة البيانات
    problems = db.borwes_db()

    # تنظيف النافذة قبل إعادة تحميل المشاكل
    for widget in window_select.winfo_children():
        widget.destroy()
        

    # عنوان النافذة
    title_label = ctk.CTkLabel(window_select, text="All Problems", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # إنشاء إطار للتمرير إذا كانت المشاكل كثيرة
    scrollable_frame = ctk.CTkFrame(window_select)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # عرض كل مشكلة مع أزرار الحذف والتعديل
    for problem, solution, img, id in problems:
        frame_item = ctk.CTkFrame(scrollable_frame)
        frame_item.pack(pady=5, padx=5, fill="x")

        # عرض النص باستخدام grid
        label = ctk.CTkLabel(frame_item, text=f"📌 {id}:  {problem}\n", anchor="w", justify="left")
        label.grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=2)

        # تخصيص الأعمدة باستخدام grid_columnconfigure لضبط عرض الأعمدة
        frame_item.grid_columnconfigure(0, weight=1, uniform="equal")
        frame_item.grid_columnconfigure(1, weight=0, uniform="equal")
        frame_item.grid_columnconfigure(2, weight=0, uniform="equal")

        # زر تعديل
        edit_button = ctk.CTkButton(frame_item, text="✏️ Edit", width=80, command=lambda p=problem, s=solution, i=img,id=id: open_edit_window(p, s, i,id))
        edit_button.grid(row=0, column=1, padx=5, pady=5)

        # زر حذف
        delete_button = ctk.CTkButton(frame_item, text="🗑️ Delete", width=80, fg_color="red",
                                      command=lambda p=problem: delete_problem_and_refresh(p))
        delete_button.grid(row=0, column=2, padx=5, pady=5)

    # زر العودة
    back_button = ctk.CTkButton(window_select, text="Back", width=200, height=40, font=("Arial", 14, "bold"),
                                command=lambda: [window_select.withdraw(), app.deiconify()])
    back_button.pack(pady=10)


# دالة لحذف المشكلة وإعادة تحميل الصفحة
def delete_problem_and_refresh(problem):
    db.delete_problem(problem)
    show_problems()  # إعادة تحميل الصفحة بعد الحذف

def open_edit_window(problem, solution, img):
    edit_window = ctk.CTkToplevel(app)
    edit_window.geometry("500x400+5+5")
    edit_window.title("Edit Problem")

    ctk.CTkLabel(edit_window, text="Edit Problem", font=("Arial", 16, "bold")).pack(pady=5)

    # حقل المشكلة
    problem_entry = ctk.CTkTextbox(edit_window, width=400, height=50,font=("Arial", 13, "bold"))
    problem_entry.pack(pady=5)
    problem_entry.insert(ctk.END, problem)

    # حقل الحل
    solution_entry = ctk.CTkTextbox(edit_window, width=400, height=100,font=("Arial", 13, "bold"))
    solution_entry.pack(pady=5)
    solution_entry.insert(ctk.END, solution)

    # حقل الصورة
    image_entry = ctk.CTkTextbox(edit_window, width=400, height=40)
    image_entry.pack(pady=5)
    image_entry.insert(ctk.END, img)
    def browse_new_image():
        filepath = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),("Word Files", "*.docx;*.doc")])
        if filepath:
            image_entry.delete("1.0", ctk.END)  # مسح المسار القديم
            image_entry.insert(ctk.END, filepath)  # إدخال المسار الجديدd
            
    browse_button = ctk.CTkButton(edit_window, text="Browse", width=80, command=browse_new_image)
    browse_button.pack(pady=5)        

    # زر حفظ التعديلات
    def save_changes():
        new_problem = problem_entry.get("1.0", "end").strip()
        new_solution = solution_entry.get("1.0", "end").strip()
        new_img = image_entry.get("1.0", "end").strip()

        if new_problem and new_solution:
            db.update_problem(problem, new_problem, new_solution, new_img)
            edit_window.destroy()
            show_problems()
        else:
            ctk.CTkMessagebox(title="Error", message="Problem and Solution cannot be empty", icon="warning")

    save_button = ctk.CTkButton(edit_window, text="Save", width=150, command=save_changes)
    save_button.pack(pady=10)
  


#!GUI

# إعداد نافذة التطبيق
ctk.set_appearance_mode("Dark")  # تعيين الوضع الداكن
ctk.set_default_color_theme("blue")  # تعيين لون الأزرار

app = ctk.CTk()
app.geometry("600x650")
app.title("Support Admin")

# إطار يحتوي على جميع العناصر
frame = ctk.CTkFrame(app, width=600, height=650)
frame.pack(pady=10)

window_select = ctk.CTkToplevel(app)  # إنشاء نافذة فرعية
window_select.geometry("600x600")
window_select.withdraw()

# "Add New Problem"
problem_label = ctk.CTkLabel(frame, text="Add New Problem", font=("Arial", 16, "bold"))
problem_label.pack(pady=5)

# problem_textfeld
problem_textfeld = ctk.CTkTextbox(frame, width=500, height=100)
problem_textfeld.pack(pady=5)

# عنوان "Add New Solution"
solution_label = ctk.CTkLabel(frame, text="Add New Solution", font=("Arial", 16, "bold"))
solution_label.pack(pady=5)

# حقل النص لإدخال الحل
solution_textfeld = ctk.CTkTextbox(frame, width=500, height=100)
solution_textfeld.pack(pady=5)

# img
def browse_image():
    filepath = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),("Word Files", "*.docx;*.doc")])
    if filepath:
        image_feld.delete("1.0", ctk.END)  # مسح النص السابق
        image_feld.insert(ctk.END, filepath)  # إدخال المسار الجديد

# img-button
button_browse = ctk.CTkButton(frame, text="Browse Image", width=250, height=40, font=("Arial", 14, "bold"), command=browse_image)
button_browse.pack(pady=10)
# img-feld
image_feld = ctk.CTkTextbox(frame, width=500, height=40)
image_feld.pack(pady=5)

# button "Add"
button_confirm = ctk.CTkButton(frame, text='Add', width=250, height=40, font=("Arial", 14, "bold"), hover_color='green', command=confirm)
button_confirm.pack(pady=10)
# زر "Show" في الأعلى لاستعراض المشكلات
button_show = ctk.CTkButton(frame, text='Show Problems', width=250, height=40, font=("Arial", 14, "bold"), hover_color='red', command=show_problems)
button_show.pack(pady=20)
# تشغيل واجهة المستخدم
app.mainloop()