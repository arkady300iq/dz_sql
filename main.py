import sqlite3

db = sqlite3.connect('university.db')

db.execute('''CREATE TABLE IF NOT EXISTS students(
           student_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(50),
           age INTEGER,
           major VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS courses(
           course_id INTEGER PRIMARY KEY AUTOINCREMENT,
           course_name VARCHAR(50),
           instructor VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS student_course(
           student_id INTEGER REFERENCES students (student_id),
           course_id INTEGER REFERENCES students (course_id),
           PRIMARY KEY (student_id, course_id));''')


def add_user(db, name, age, major):
    db.execute(f'''INSERT INTO students(name, age, major)
               VALUES  (?, ?, ?)''', (name, age, major))
    db.commit()
    

def add_course(db, course_name, instructor):
    db.execute(f'''INSERT INTO courses(course_name, instructor)
               VALUES  (?, ?)''', (course_name, instructor))
    db.commit()

def add_to_student_course(db, student_id, course_id):
    db.execute(f'''INSERT INTO student_course(student_id, course_id)
               VALUES  (?, ?)''', (student_id, course_id))
    db.commit()

def edit_student(db, student_id, name, age, major):
    db.execute("UPDATE students SET name = ?, age = ?, major = ? WHERE student_id = ?", (name,age,major,student_id))
    db.commit()

def get_students(db):
    students = db.execute('''SELECT * FROM students''')
    dict_std = {}
    for student in students:
        dict_std[student[0]] = {'name': student[1], "age": student[2], "major": student[3]}
    db.commit()

    return dict_std

def get_courses(db):
    courses = db.execute('''SELECT * FROM courses''')
    dict_cour = {}
    for course in courses:
        dict_cour[course[0]] = {'course_name': course[1], "instructor": course[2]}
    db.commit()

    return dict_cour


def get_student_courses(db, course_id):
    courses_ids = db.execute(f'''SELECT student_id FROM student_course WHERE course_id == {course_id}''')
    students = [db.execute(f'''SELECT * FROM students WHERE student_id == {int(i[0])}''') for i in courses_ids]
    return students


while True:
    print("\n1. Додати нового студента")
    print("2. Додати новий курс")
    print("3. Показати список студентів")
    print("4. Показати список курсів")
    print("5. Зареєструвати студента на курс")
    print("6. Показати студентів на конкретному курсі")
    print("7. Оновити інформацію студента")
    print("8. Вийти")

    choice = input("Оберіть опцію (1-7): ")
    
    match choice:
        case "1":
            name = input("Введіть ім'я студента:")
            age = int(input("Введіть вік студента:"))
            major = input("Введіть дисципліну студента:")
            add_user(db, name, age, major)
            print(f"Студент {name} успішно доданий")
        case "2":
            name = input("Введіть ім'я курсу:")
            instructor = input("Введіть вчителя курсу:")
            add_course(db, name, instructor)
            print(f"Курс {name} успішно створений")
        case "3":
            print("Ось список студентів:", get_students(db))
        case "4":
            print("Ось список курсів:", get_courses(db))
        case "5":
            student_id = int(input("Введіть id студента "))
            course_id = int(input("Введіть id курсу "))
            add_to_student_course(db, student_id, course_id)
            print("Студента успішно додано до курсу!")
        case "6":
            course_id = int(input("Введіть id курсу:"))
            print([i.fetchall() for i in get_student_courses(db, course_id)])
        case "7":
            student_id = int(input("Student id to edit:"))
            name = input('Name:')
            age = int(input("Age:"))
            major = input("Major:")
            edit_student(db, student_id, name, age, major)
        case "8":
            break
        case _:
            print("Некоректний вибір. Будь ласка, введіть число від 1 до 7.")
