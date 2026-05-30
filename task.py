from dataclasses import dataclass, field

# Визначення класу Teacher
@dataclass
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: set
    assigned_subjects: set = field(default_factory=set)


def create_schedule(subjects, teachers):
    # Зберігатиме обрані підмножини
    final_schedule = []
    # Непокриті предмети
    uncovered_subjects = subjects.copy()

    while uncovered_subjects:
        best_teacher = None
        best_coverage = set()

        for teacher in teachers:
            # Знаходимо предмети, які цей вчитель може викладати зі списку непризначених
            can_cover = teacher.can_teach_subjects.intersection(uncovered_subjects)
            
            if not can_cover:
                continue
                
            # Критерії вибору:
            if (best_teacher is None or 
                len(can_cover) > len(best_coverage) or 
                (len(can_cover) == len(best_coverage) and teacher.age < best_teacher.age)):
                
                best_teacher = teacher
                best_coverage = can_cover

        # Якщо ми пройшли всіх вчителів і нікого не знайшли для решти предметів
        if best_teacher is None:
            return None  # Неможливо покрити всі предмети

        # Призначаємо предмети вчителю
        best_teacher.assigned_subjects = best_coverage
        final_schedule.append(best_teacher)
        
        # Викреслюємо призначені предмети зі списку непокритих
        uncovered_subjects -= best_coverage

    return final_schedule


if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
    # Створення списку викладачів
    teachers = [
    Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {"Математика", "Фізика"}),
    Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
    Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {"Інформатика", "Математика"}),
    Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}),
    Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {"Фізика", "Інформатика"}),
    Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"})
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
