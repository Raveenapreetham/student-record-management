import json
import os

# Student Class 
class Student:
    def __init__(self, student_id, name, age, department, marks):
        self.id = student_id
        self.name = name
        self.age = age
        self.department = department
        self.marks = marks  # dictionary {subject: score}

    def average_marks(self):
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def to_dict(self):
        """Convert object to dictionary for saving in JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "marks": self.marks
        }

    @staticmethod
    def from_dict(data):
        """Create Student object from dictionary (while loading)"""
        return Student(
            data["id"],
            data["name"],
            data["age"],
            data["department"],
            data["marks"]
        )


# Student Management System
class StudentManagement:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_students()

    # Load student records from JSON file
    def load_students(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
        else:
            self.students = []

    # Save student records to JSON file
    def save_students(self):
        with open(self.filename, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    # Add new student
    def add_student(self, student):
        if any(s.id == student.id for s in self.students):
            print(f"❌ Student with ID {student.id} already exists.")
            return
        self.students.append(student)
        self.save_students()
        print(f"✅ Student {student.name} added successfully.")

    # Update marks by student ID
    def update_marks(self, student_id, subject, score):
        for s in self.students:
            if s.id == student_id:
                s.marks[subject] = score
                self.save_students()
                print(f"✅ Marks updated for student {s.name}.")
                return
        print("❌ Student ID not found.")

    # Delete student by ID
    def delete_student(self, student_id):
        for s in self.students:
            if s.id == student_id:
                self.students.remove(s)
                self.save_students()
                print(f"✅ Student {s.name} deleted successfully.")
                return
        print("❌ Student ID not found.")

    # Find student with highest average marks
    def highest_average_student(self):
        if not self.students:
            print("No students available.")
            return
        top_student = max(self.students, key=lambda s: s.average_marks())
        print(f"🏆 Top Student: {top_student.name} (ID: {top_student.id}), "
              f"Average Marks: {top_student.average_marks():.2f}")

    # Print all students sorted by department then name
    def print_students(self):
        if not self.students:
            print("No students available.")
            return
        sorted_students = sorted(self.students, key=lambda s: (s.department, s.name))
        print("\n📋 Student Records:")
        for s in sorted_students:
            print(f"ID: {s.id}, Name: {s.name}, Age: {s.age}, Dept: {s.department}, Marks: {s.marks}")
          
# Main Program (Menu)

def main():
    system = StudentManagement()

    while True:
        print("\n===== Student Record Management System =====")
        print("1. Add Student")
        print("2. Update Student Marks")
        print("3. Delete Student")
        print("4. Show Top Student by Average")
        print("5. Show All Students")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = input("Enter ID: ")
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            dept = input("Enter Department: ")
            marks = {}
            while True:
                 try:
                    age = int(input("Enter Age: "))
                    if age <= 0:
                        print("❌ Age must be a positive number. Try again.")
                        continue
                    break
                except ValueError:
                   print("❌ Invalid input. Please enter a valid number.")

                sub = input("Enter Subject (or 'done' to finish): ")
                if sub.lower() == "done":
                    break
                score = int(input(f"Enter marks for {sub}: "))
                marks[sub] = score
            student = Student(student_id, name, age, dept, marks)
            system.add_student(student)

        elif choice == "2":
            student_id = input("Enter Student ID: ")
            subject = input("Enter Subject: ")
            score = int(input("Enter New Marks: "))
            system.update_marks(student_id, subject, score)

        elif choice == "3":
            student_id = input("Enter Student ID: ")
            system.delete_student(student_id)

        elif choice == "4":
            system.highest_average_student()

        elif choice == "5":
            system.print_students()

        elif choice == "6":
            print("Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
