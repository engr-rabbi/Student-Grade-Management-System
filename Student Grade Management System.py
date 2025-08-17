#!/usr/bin/env python3
# This shebang line specifies that the script should be run using Python 3.
# Why: Ensures compatibility and portability across Unix-like systems.

"""
Student Grade Management System (CLI Version)
A comprehensive system to manage student records with CSV persistence
"""
# This docstring provides a high-level overview of the program's purpose.
# Why: Helps developers and users understand the script's functionality.

import csv
# Importing the csv module to handle CSV file operations.
# Why: CSV is used for persistent storage of student data, allowing data to be saved and loaded.

import os
# Importing the os module to check file existence and handle file operations.
# Why: Needed to verify if the CSV file exists when loading data.

from typing import Dict, List, Optional, Tuple
# Importing type hints for better code readability and type checking.
# Why: Enhances code maintainability and helps catch type-related errors during development.

class StudentGradeManager:
    # Defining the main class to manage student records.
    # Why: Encapsulates all functionality related to student data management in a single class.

    def __init__(self, csv_file: str = "students.csv"):
        # Constructor method to initialize the StudentGradeManager.
        # Why: Sets up the initial state, including the CSV file name and an empty student dictionary.
        self.csv_file = csv_file
        # Storing the CSV file name (default: "students.csv").
        # Why: Allows flexibility to specify a different file if needed.
        self.students: Dict[str, Dict] = {}
        # Initializing an empty dictionary to store student data with ID as the key.
        # Why: A dictionary provides fast lookup by student ID and organizes data efficiently.
        self.load_data()
        # Calling load_data to populate the students dictionary from the CSV file.
        # Why: Ensures data is loaded from persistent storage when the program starts.
    
    def validate_marks(self, marks: float) -> bool:
        # Method to validate that marks are between 0 and 100.
        # Why: Ensures marks are within a valid range to maintain data integrity.
        return 0 <= marks <= 100
        # Returns True if marks are valid, False otherwise.
        # Why: Simple boolean check for validation logic.
    
    def calculate_gpa(self, marks: Dict[str, float]) -> float:
        # Method to calculate GPA on a 5.0 scale based on marks.
        # Why: GPA is a key metric for student performance, standardized to a 5.0 scale.
        if not marks:
            # Checking if the marks dictionary is empty.
            # Why: Prevents division by zero and handles edge cases.
            return 0.0
        total_marks = sum(marks.values())
        # Summing all marks in the dictionary.
        # Why: To calculate the average, we need the total marks.
        average_marks = total_marks / len(marks)
        # Calculating the average by dividing total marks by the number of subjects.
        # Why: Average marks are used to compute GPA.
        return round(average_marks / 20, 2)  # Convert to 5.0 scale
        # Dividing by 20 to convert percentage to a 5.0 scale and rounding to 2 decimal places.
        # Why: Standardizes GPA to a 5.0 scale and ensures readable output.
    
    def get_grade_letter(self, gpa: float) -> str:
        # Method to convert GPA to a letter grade (A, B, C, D, F).
        # Why: Letter grades provide a human-readable representation of performance.
        if gpa >= 4.5:
            return 'A'
        elif gpa >= 3.5:
            return 'B'
        elif gpa >= 2.5:
            return 'C'
        elif gpa >= 1.5:
            return 'D'
        else:
            return 'F'
        # Using conditional logic to map GPA ranges to letter grades.
        # Why: Standard grading scale to categorize student performance.
    
    def add_student(self):
        # Method to add a new student to the system.
        # Why: Core functionality to create new student records.
        print("\n--- Add New Student ---")
        # Displaying a header for user clarity.
        # Why: Improves user experience in the CLI interface.
        
        while True:
            # Loop to ensure valid student ID input.
            # Why: Prevents duplicate or empty IDs.
            student_id = input("Enter Student ID: ").strip()
            # Getting student ID from user input and removing whitespace.
            # Why: Ensures clean input data.
            if not student_id:
                print("Student ID cannot be empty!")
                continue
            # Checking for empty ID.
            # Why: Ensures every student has a unique identifier.
            if student_id in self.students:
                print(f"Student with ID {student_id} already exists!")
                continue
            # Checking for duplicate ID.
            # Why: Prevents overwriting existing student data.
            break
        
        name = input("Enter Student Name: ").strip()
        # Getting student name from user input.
        # Why: Name is a required field for student records.
        if not name:
            print("Name cannot be empty!")
            return
        # Checking for empty name.
        # Why: Ensures valid data entry before proceeding.
        
        marks = {}
        # Initializing an empty dictionary for subject marks.
        # Why: To store subject-mark pairs for the student.
        print("Enter marks for subjects (press Enter with empty subject name to finish):")
        # Prompting user to enter subject marks.
        # Why: Guides the user through the process.
        
        while True:
            # Loop to collect subject marks until user is done.
            # Why: Allows adding multiple subjects flexibly.
            subject = input("Subject name: ").strip()
            if not subject:
                break
            # Breaking the loop if no subject is entered.
            # Why: Signals the end of subject input.
            
            try:
                mark = float(input(f"Marks for {subject} (0-100): "))
                # Getting marks as a float.
                # Why: Marks are numerical and need to be validated.
                if not self.validate_marks(mark):
                    print("Marks must be between 0 and 100!")
                    continue
                # Validating marks using validate_marks method.
                # Why: Ensures marks are within the valid range.
                marks[subject] = mark
                # Adding subject and mark to the marks dictionary.
                # Why: Stores the subject-mark pair for the student.
            except ValueError:
                print("Please enter a valid number!")
                continue
            # Handling invalid numerical input.
            # Why: Prevents crashes from non-numeric input.
        
        if not marks:
            print("At least one subject mark is required!")
            return
        # Checking if at least one subject mark was entered.
        # Why: Ensures the student record has meaningful data.
        
        gpa = self.calculate_gpa(marks)
        # Calculating GPA for the student.
        # Why: GPA is a required field for the student record.
        self.students[student_id] = {
            "name": name,
            "marks": marks,
            "gpa": gpa
        }
        # Adding the student data to the students dictionary.
        # Why: Stores all student information in memory.
        
        print(f"\n✅ Student {name} (ID: {student_id}) added successfully!")
        print(f"GPA: {gpa} ({self.get_grade_letter(gpa)})")
        # Displaying success message with GPA and letter grade.
        # Why: Provides user feedback on successful operation.
    
    def view_all_students(self):
        # Method to display all students and their details.
        # Why: Allows users to see an overview of all student records.
        if not self.students:
            print("\n❌ No students found!")
            return
        # Checking if there are any students.
        # Why: Prevents displaying an empty table.
        
        print("\n--- All Students ---")
        print(f"{'ID':<10} {'Name':<20} {'GPA':<6} {'Grade':<5}")
        print("-" * 45)
        # Printing a formatted table header.
        # Why: Organizes output for readability.
        
        for student_id, data in self.students.items():
            # Looping through all students.
            # Why: To display each student's details.
            gpa = data['gpa']
            grade = self.get_grade_letter(gpa)
            print(f"{student_id:<10} {data['name']:<20} {gpa:<6} {grade:<5}")
            # Printing student details in a formatted row.
            # Why: Ensures consistent and readable output.
    
    def search_student(self):
        # Method to search for a student by ID.
        # Why: Allows users to view details of a specific student.
        print("\n--- Search Student ---")
        student_id = input("Enter Student ID to search: ").strip()
        # Getting student ID from user input.
        # Why: To identify the student to search for.
        
        if student_id not in self.students:
            print(f"❌ Student with ID {student_id} not found!")
            return
        # Checking if the student exists.
        # Why: Prevents errors when searching for non-existent students.
        
        student = self.students[student_id]
        print(f"\n📋 Student Details:")
        print(f"ID: {student_id}")
        print(f"Name: {student['name']}")
        print(f"GPA: {student['gpa']} ({self.get_grade_letter(student['gpa'])})")
        print(f"Subjects and Marks:")
        for subject, mark in student['marks'].items():
            print(f"  • {subject}: {mark}")
        # Displaying detailed student information.
        # Why: Provides comprehensive feedback to the user.
    
    def update_student(self):
        # Method to update a student’s marks.
        # Why: Allows modification of existing student records.
        print("\n--- Update Student ---")
        student_id = input("Enter Student ID to update: ").strip()
        # Getting student ID from user input.
        # Why: To identify the student to update.
        
        if student_id not in self.students:
            print(f"❌ Student with ID {student_id} not found!")
            return
        # Checking if the student exists.
        # Why: Prevents errors for non-existent students.
        
        student = self.students[student_id]
        print(f"\nUpdating marks for {student['name']} (ID: {student_id})")
        print("Current subjects:", list(student['marks'].keys()))
        # Displaying the student’s name and current subjects.
        # Why: Provides context for the update operation.
        
        print("\nOptions:")
        print("1. Update existing subject marks")
        print("2. Add new subject")
        print("3. Remove subject")
        # Presenting update options to the user.
        # Why: Allows flexibility in how to modify the student’s record.
        
        try:
            choice = int(input("Choose option (1-3): "))
            # Getting the user’s choice.
            # Why: Determines which update operation to perform.
        except ValueError:
            print("Invalid choice!")
            return
            # Handling invalid input.
            # Why: Prevents crashes from non-numeric input.
        
        if choice == 1:
            # Option to update existing subject marks.
            # Why: Allows modifying marks for an existing subject.
            subject = input("Enter subject name to update: ").strip()
            if subject not in student['marks']:
                print(f"Subject {subject} not found!")
                return
            # Checking if the subject exists.
            # Why: Prevents updating non-existent subjects.
            
            try:
                new_mark = float(input(f"Enter new marks for {subject}: "))
                if not self.validate_marks(new_mark):
                    print("Marks must be between 0 and 100!")
                    return
                # Getting and validating new marks.
                # Why: Ensures valid input data.
                
                old_mark = student['marks'][subject]
                student['marks'][subject] = new_mark
                student['gpa'] = self.calculate_gpa(student['marks'])
                # Updating the mark and recalculating GPA.
                # Why: Reflects the change in the student’s record.
                
                print(f"✅ Updated {subject}: {old_mark} → {new_mark}")
                print(f"New GPA: {student['gpa']} ({self.get_grade_letter(student['gpa'])})")
                # Displaying the update result.
                # Why: Provides user feedback.
                
            except ValueError:
                print("Please enter a valid number!")
                # Handling invalid numerical input.
                # Why: Prevents crashes from non-numeric input.
                
        elif choice == 2:
            # Option to add a new subject.
            # Why: Allows expanding the student’s subject list.
            subject = input("Enter new subject name: ").strip()
            if subject in student['marks']:
                print(f"Subject {subject} already exists!")
                return
            # Checking if the subject already exists.
            # Why: Prevents duplicate subjects.
            
            try:
                mark = float(input(f"Enter marks for {subject}: "))
                if not self.validate_marks(mark):
                    print("Marks must be between 0 and 100!")
                    return
                # Getting and validating marks.
                # Why: Ensures valid input data.
                
                student['marks'][subject] = mark
                student['gpa'] = self.calculate_gpa(student['marks'])
                # Adding the subject and recalculating GPA.
                # Why: Updates the student’s record.
                
                print(f"✅ Added {subject}: {mark}")
                print(f"New GPA: {student['gpa']} ({self.get_grade_letter(student['gpa'])})")
                # Displaying the result.
                # Why: Provides user feedback.
                
            except ValueError:
                print("Please enter a valid number!")
                # Handling invalid numerical input.
                # Why: Prevents crashes.
                
        elif choice == 3:
            # Option to remove a subject.
            # Why: Allows removing outdated or incorrect subjects.
            if len(student['marks']) <= 1:
                print("Cannot remove the last subject!")
                return
            # Checking if there’s only one subject left.
            # Why: Ensures at least one subject remains for a valid record.
            
            subject = input("Enter subject name to remove: ").strip()
            if subject not in student['marks']:
                print(f"Subject {subject} not found!")
                return
            # Checking if the subject exists.
            # Why: Prevents removing non-existent subjects.
            
            removed_mark = student['marks'].pop(subject)
            student['gpa'] = self.calculate_gpa(student['marks'])
            # Removing the subject and recalculating GPA.
            # Why: Updates the student’s record.
            
            print(f"✅ Removed {subject} (was: {removed_mark})")
            print(f"New GPA: {student['gpa']} ({self.get_grade_letter(student['gpa'])})")
            # Displaying the result.
            # Why: Provides user feedback.
        
        else:
            print("Invalid choice!")
            # Handling invalid option input.
            # Why: Ensures only valid options are processed.
    
    def delete_student(self):
        # Method to delete a student record.
        # Why: Allows removing student records when no longer needed.
        print("\n--- Delete Student ---")
        student_id = input("Enter Student ID to delete: ").strip()
        # Getting student ID from user input.
        # Why: To identify the student to delete.
        
        if student_id not in self.students:
            print(f"❌ Student with ID {student_id} not found!")
            return
        # Checking if the student exists.
        # Why: Prevents errors for non-existent students.
        
        student_name = self.students[student_id]['name']
        confirm = input(f"Are you sure you want to delete {student_name} (ID: {student_id})? (y/N): ")
        # Asking for confirmation before deletion.
        # Why: Prevents accidental deletion of data.
        
        if confirm.lower() == 'y':
            del self.students[student_id]
            print(f"✅ Student {student_name} deleted successfully!")
            # Deleting the student and confirming success.
            # Why: Updates the data and informs the user.
        else:
            print("Delete operation cancelled.")
            # Cancelling the operation if not confirmed.
            # Why: Respects user’s decision to abort.
    
    def save_data(self):
        # Method to save student data to a CSV file.
        # Why: Ensures data persistence across program runs.
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                # Opening the CSV file in write mode.
                # Why: To write student data to persistent storage.
                writer = csv.writer(file)
                # Creating a CSV writer object.
                # Why: Simplifies writing data in CSV format.
                
                # Write header
                writer.writerow(['ID', 'Name', 'Subjects', 'Marks', 'GPA'])
                # Writing the CSV header.
                # Why: Defines the structure of the CSV file.
                
                # Write student data
                for student_id, data in self.students.items():
                    subjects = '|'.join(data['marks'].keys())
                    marks = '|'.join(str(mark) for mark in data['marks'].values())
                    # Joining subjects and marks with '|' for CSV storage.
                    # Why: Allows storing multiple subjects/marks in a single CSV field.
                    writer.writerow([
                        student_id,
                        data['name'],
                        subjects,
                        marks,
                        data['gpa']
                    ])
                    # Writing a row for each student.
                    # Why: Saves all student data in CSV format.
                
            print(f"✅ Data saved to {self.csv_file} successfully!")
            # Confirming successful save.
            # Why: Informs the user that data is persisted.
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            # Handling file write errors.
            # Why: Prevents crashes and informs the user of issues.
    
    def load_data(self):
        # Method to load student data from a CSV file.
        # Why: Restores data from previous sessions.
        if not os.path.exists(self.csv_file):
            print(f"📁 {self.csv_file} not found. Starting with empty database.")
            return
        # Checking if the CSV file exists.
        # Why: Prevents errors when the file is missing.
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                # Opening the CSV file in read mode.
                # Why: To read stored student data.
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header
                # Skipping the CSV header.
                # Why: The header is not data and should be ignored.
                
                if not header:
                    return
                # Checking if the file is empty.
                # Why: Prevents errors with empty files.
                
                for row in reader:
                    # Looping through each row in the CSV.
                    # Why: To process each student’s data.
                    if len(row) >= 5:
                        # Ensuring the row has enough fields.
                        # Why: Prevents errors from malformed CSV rows.
                        student_id, name, subjects_str, marks_str, gpa_str = row[:5]
                        # Extracting fields from the row.
                        # Why: Maps CSV data to student attributes.
                        
                        # Parse subjects and marks
                        subjects = subjects_str.split('|') if subjects_str else []
                        marks_list = marks_str.split('|') if marks_str else []
                        # Splitting subjects and marks strings into lists.
                        # Why: Reconstructs the subject-mark pairs.
                        
                        marks = {}
                        for subject, mark_str in zip(subjects, marks_list):
                            try:
                                marks[subject] = float(mark_str)
                            except ValueError:
                                continue
                            # Converting marks to floats and building the marks dictionary.
                            # Why: Restores the subject-mark pairs, ignoring invalid data.
                        
                        try:
                            gpa = float(gpa_str)
                        except ValueError:
                            gpa = self.calculate_gpa(marks)
                            # Loading GPA or recalculating if invalid.
                            # Why: Ensures valid GPA data.
                        
                        self.students[student_id] = {
                            "name": name,
                            "marks": marks,
                            "gpa": gpa
                        }
                        # Adding the student to the students dictionary.
                        # Why: Restores the student record in memory.
                
            print(f"📂 Loaded {len(self.students)} students from {self.csv_file}")
            # Confirming successful load.
            # Why: Informs the user of the number of records loaded.
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            # Handling file read errors.
            # Why: Prevents crashes and informs the user.
    
    def export_summary(self):
        # Method to export summary statistics of the class.
        # Why: Provides an overview of class performance.
        if not self.students:
            print("\n❌ No students found!")
            return
        # Checking if there are any students.
        # Why: Prevents processing empty data.
        
        gpas = [student['gpa'] for student in self.students.values()]
        # Collecting all GPAs in a list.
        # Why: Needed for calculating statistics.
        avg_gpa = sum(gpas) / len(gpas)
        max_gpa = max(gpas)
        min_gpa = min(gpas)
        # Calculating average, highest, and lowest GPA.
        # Why: Summarizes class performance metrics.
        
        print("\n--- Class Summary ---")
        print(f"Total Students: {len(self.students)}")
        print(f"Average GPA: {avg_gpa:.2f} ({self.get_grade_letter(avg_gpa)})")
        print(f"Highest GPA: {max_gpa:.2f} ({self.get_grade_letter(max_gpa)})")
        print(f"Lowest GPA: {min_gpa:.2f} ({self.get_grade_letter(min_gpa)})")
        # Displaying summary statistics.
        # Why: Provides a concise overview for the user.
        
        # Grade distribution
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for gpa in gpas:
            grade_counts[self.get_grade_letter(gpa)] += 1
        # Counting the number of students per grade.
        # Why: Shows the distribution of grades in the class.
        
        print("\nGrade Distribution:")
        for grade, count in grade_counts.items():
            percentage = (count / len(self.students)) * 100
            print(f"  {grade}: {count} students ({percentage:.1f}%)")
        # Displaying the grade distribution.
        # Why: Provides insight into overall class performance.
    
    def display_menu(self):
        # Method to display the main menu.
        # Why: Provides a user-friendly interface for navigation.
        print("\n" + "="*50)
        print("📚 STUDENT GRADE MANAGEMENT SYSTEM")
        print("="*50)
        print("1. 📝 Add Student")
        print("2. 👥 View All Students")
        print("3. 🔍 Search Student by ID")
        print("4. ✏️  Update Student")
        print("5. 🗑️  Delete Student")
        print("6. 💾 Save Data to CSV")
        print("7. 📊 Export Class Summary")
        print("8. 🚪 Exit")
        print("="*50)
        # Printing a formatted menu with options.
        # Why: Guides the user through available actions.
    
    def run(self):
        # Main program loop to run the application.
        # Why: Controls the program flow and user interaction.
        print("🎓 Welcome to Student Grade Management System!")
        # Displaying a welcome message.
        # Why: Enhances user experience.
        
        while True:
            # Infinite loop for continuous user interaction.
            # Why: Keeps the program running until the user chooses to exit.
            self.display_menu()
            # Displaying the menu.
            # Why: Shows available options at each iteration.
            
            try:
                choice = int(input("Enter your choice (1-8): "))
                # Getting the user’s menu choice.
                # Why: Determines which action to perform.
            except ValueError:
                print("❌ Please enter a valid number!")
                continue
                # Handling invalid input.
                # Why: Prevents crashes from non-numeric input.
            
            if choice == 1:
                self.add_student()
                # Calling add_student method.
                # Why: Executes the add student functionality.
            elif choice == 2:
                self.view_all_students()
                # Calling view_all_students method.
                # Why: Displays all student records.
            elif choice == 3:
                self.search_student()
                # Calling search_student method.
                # Why: Searches for a specific student.
            elif choice == 4:
                self.update_student()
                # Calling update_student method.
                # Why: Updates a student’s record.
            elif choice == 5:
                self.delete_student()
                # Calling delete_student method.
                # Why: Deletes a student’s record.
            elif choice == 6:
                self.save_data()
                # Calling save_data method.
                # Why: Saves data to CSV.
            elif choice == 7:
                self.export_summary()
                # Calling export_summary method.
                # Why: Displays class statistics.
            elif choice == 8:
                # Auto-save before exit
                self.save_data()
                print("\n👋 Thank you for using Student Grade Management System!")
                print("💾 Data has been automatically saved.")
                break
                # Saving data and exiting the program.
                # Why: Ensures data is saved before termination.
            else:
                print("❌ Invalid choice! Please select 1-8.")
                # Handling invalid menu choices.
                # Why: Guides the user to valid options.
            
            input("\nPress Enter to continue...")
            # Pausing for user to review output before continuing.
            # Why: Improves user experience by allowing time to read results.

def main():
    # Main function to run the application.
    # Why: Entry point for the program.
    manager = StudentGradeManager()
    # Creating an instance of StudentGradeManager.
    # Why: Initializes the system.
    try:
        manager.run()
        # Running the main program loop.
        # Why: Starts the application.
    except KeyboardInterrupt:
        print("\n\n🛑 Program interrupted by user.")
        manager.save_data()
        print("💾 Data has been saved. Goodbye!")
        # Handling Ctrl+C interruption.
        # Why: Ensures data is saved before abrupt termination.
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        manager.save_data()
        print("💾 Data has been saved.")
        # Handling unexpected errors.
        # Why: Prevents data loss and informs the user.

if __name__ == "__main__":
    main()
    # Checking if the script is run directly and calling main.
    # Why: Standard Python practice to ensure main runs only when intended.