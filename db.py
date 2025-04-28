import sqlite3
import nltk
import random
from PIL import Image

def create_db():
    con = sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
    cursor = con.cursor()
    sql ='''CREATE TABLE IF NOT EXISTS problems(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                    problem TEXT UNIQUE,
                    solution TEXT,
                        image_path TEXT
        
        )'''
    cursor.execute(sql )

    con.commit()
    con.close()
    print("DB wurde erstellt")
    
def insert_db(problem,solution,image):
    con = sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
    cursor = con.cursor()
    insert="INSERT INTO problems (problem, solution,image_path) VALUES (?,?,?)"
    insert1= cursor.execute(insert, (problem,solution,image))
    if insert1:
        print("inserted")
    con.commit()
    con.close()

def borwes_db():
    con = sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
    cursor = con.cursor()
    cursor.execute("SELECT problem, solution, image_path,id FROM problems")
    results = cursor.fetchall()
    con.close()
    return results  # ترجع جميع المشاكل والحلول

def delete_problem(problem):
    con = sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
    cursor = con.cursor()
    cursor.execute("DELETE FROM problems WHERE problem = ?", (problem,))
    con.commit()
    con.close()
def update_problem(old_problem, new_problem, new_solution, new_image):
    con = sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
    cursor = con.cursor()
    cursor.execute("""
        UPDATE problems 
        SET problem = ?, solution = ?, image_path = ?
        WHERE problem = ?
    """, (new_problem, new_solution, new_image, old_problem))
    con.commit()
    con.close()


def search_problem():
        con = sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
        cursor = con.cursor()
        cursor.execute(
            'SELECT problem FROM problems'
        )
        rows = cursor.fetchall()
        con.close()
    
        return [row[0] for row in rows] if rows else []
        
def search_soulution(problem):
    con=sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
    cursor=con.cursor()
    cursor.execute('SELECT solution, image_path FROM problems WHERE problem=?', (problem,))
    row = cursor.fetchone()  # جلب أول نتيجة فقط
    con.close()
    
    if row:
        return row  # (solution, image_path)
    else:
        return ("❌ keine Lösung gefunden", None)  # إرجاع قيم افتراضية لتجنب الخطأ
    
# وظيفة للبحث عن مشكلة وإظهار الحل والصورة
# #def show_problem(problem):
#     con = sqlite3.connect(r"c:/Users/w.saad/OneDrive - tmITService/Desktop/PYTHON/Support/problem")
#     cursor = con.cursor()

#     cursor.execute("SELECT solution, image_path FROM problems WHERE problem = ?", (problem,))
#     result = cursor.fetchone()

#     if result:
#         solution, image_path = result
#         print(f"🔹 المشكلة: {problem}\n✅ الحل: {solution}")

#         # عرض الصورة إذا كانت موجودة
#         if image_path:
#             img = Image.open(image_path)
#             img.show()  # فتح الصورة تلقائيًا
#         else:
#             print("❌ لا توجد صورة لهذه المشكلة.")
#     else:
#         print("❌ المشكلة غير موجودة في قاعدة البيانات!")

#     con.close()
# #show_problem("tes2t")
