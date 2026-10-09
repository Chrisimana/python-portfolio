from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import json
import os
from datetime import datetime

# Basic student data management class
class StudentManager:
    def __init__(self):
        self.data_file = "students_data.json"
        self.load_data()
    
    # Memuat data dari file JSON
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    self.students = json.load(file)
            except:
                self.students = []
        else:
            self.students = []
    
    # Menyimpan data ke file JSON
    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.students, file, indent=4)
    
    # Menambah data mahasiswa baru
    def add_student(self, name, nim, birth_date):
        student = {
            'id': len(self.students) + 1,
            'name': name,
            'nim': nim,
            'birth_date': birth_date,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.students.append(student)
        self.save_data()
        return student
    
    # Mendapatkan semua data mahasiswa
    def get_all_students(self):
        return self.students

class ModernStudentForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.student_manager = StudentManager()
        self.init_ui()
        
    # Initialize UI
    def init_ui(self):
        self.setWindowTitle("Student Management System")
        self.setGeometry(300, 300, 900, 700)
        self.setMinimumSize(800, 600)
        
        # Set style
        self.set_modern_style()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left side - Form
        form_container = self.create_form_container()
        main_layout.addWidget(form_container, 1)
        
        # Right side - History
        history_container = self.create_history_container()
        main_layout.addWidget(history_container, 1)
        
        # Load existing data
        self.load_history()
    
    # Set modern style
    def set_modern_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #d1d5db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #374151;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4f46e5;
            }
            QLabel {
                color: #374151;
                font-weight: 500;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                border: 2px solid #d1d5db;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #f9fafb;
                selection-background-color: #4f46e5;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #4f46e5;
                background-color: white;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
            QPushButton.secondary {
                background-color: #6b7280;
            }
            QPushButton.secondary:hover {
                background-color: #4b5563;
            }
            QListWidget {
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
            }
            QListWidget::item:selected {
                background-color: #e0e7ff;
                color: #3730a3;
            }
            QCalendarWidget {
                border: 2px solid #d1d5db;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                color: #4f46e5;
                font-weight: bold;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #d1d5db;
            }
        """)
    
    # Buat wadah formulir
    def create_form_container(self):
        container = QGroupBox("Student Registration Form")
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Student Information")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1f2937; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Name field
        name_layout = QHBoxLayout()
        lbl_nama = QLabel("Full Name:")
        lbl_nama.setFixedWidth(120)
        self.ledit_nama = QLineEdit()
        self.ledit_nama.setPlaceholderText("Enter your full name...")
        name_layout.addWidget(lbl_nama)
        name_layout.addWidget(self.ledit_nama)
        layout.addLayout(name_layout)
        
        # NIM field
        nim_layout = QHBoxLayout()
        lbl_nim = QLabel("Student ID:")
        lbl_nim.setFixedWidth(120)
        self.ledit_nim = QLineEdit()
        self.ledit_nim.setPlaceholderText("Enter your student ID...")
        nim_layout.addWidget(lbl_nim)
        nim_layout.addWidget(self.ledit_nim)
        layout.addLayout(nim_layout)
        
        # Program Study
        study_layout = QHBoxLayout()
        lbl_study = QLabel("Program Study:")
        lbl_study.setFixedWidth(120)
        self.combo_study = QComboBox()
        self.combo_study.addItems([
            "Computer Science", 
            "Electrical Engineering", 
            "Mechanical Engineering",
            "Civil Engineering",
            "Business Administration",
            "Psychology"
        ])
        study_layout.addWidget(lbl_study)
        study_layout.addWidget(self.combo_study)
        layout.addLayout(study_layout)
        
        # Birth Date
        birth_layout = QVBoxLayout()
        lbl_tgl_lahir = QLabel("Date of Birth:")
        self.calender_lahir = QCalendarWidget()
        self.calender_lahir.setGridVisible(True)
        self.calender_lahir.setMaximumDate(QDate.currentDate())
        birth_layout.addWidget(lbl_tgl_lahir)
        birth_layout.addWidget(self.calender_lahir)
        layout.addLayout(birth_layout)
        
        # Gender
        gender_layout = QHBoxLayout()
        lbl_gender = QLabel("Gender:")
        lbl_gender.setFixedWidth(120)
        self.gender_group = QButtonGroup()
        self.radio_male = QRadioButton("Male")
        self.radio_female = QRadioButton("Female")
        self.gender_group.addButton(self.radio_male)
        self.gender_group.addButton(self.radio_female)
        self.radio_male.setChecked(True)
        
        gender_layout.addWidget(lbl_gender)
        gender_layout.addWidget(self.radio_male)
        gender_layout.addWidget(self.radio_female)
        gender_layout.addStretch()
        layout.addLayout(gender_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_simpan = QPushButton("Save Data")
        self.btn_simpan.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.btn_clear = QPushButton("Clear Form")
        self.btn_clear.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.btn_clear.setProperty("class", "secondary")
        
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_simpan)
        layout.addLayout(button_layout)
        
        layout.addStretch()
        container.setLayout(layout)
        
        # Connect signals
        self.btn_simpan.clicked.connect(self.save_student)
        self.btn_clear.clicked.connect(self.clear_form)
        
        return container
    
    # Buat riwayat/tampilan
    def create_history_container(self):
        container = QGroupBox("Student Records")
        layout = QVBoxLayout()
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name or student ID...")
        self.btn_search = QPushButton("Search")
        self.btn_search.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.btn_search)
        layout.addLayout(search_layout)
        
        # Statistics
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel("Total Records: 0")
        self.stats_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Student list
        self.student_list = QListWidget()
        self.student_list.setAlternatingRowColors(True)
        layout.addWidget(self.student_list)
        
        # Action buttons for list
        action_layout = QHBoxLayout()
        self.btn_view = QPushButton("View Details")
        self.btn_delete = QPushButton("Delete")
        self.btn_export = QPushButton("Export Data")
        self.btn_view.setProperty("class", "secondary")
        self.btn_delete.setProperty("class", "secondary")
        self.btn_export.setProperty("class", "secondary")
        
        action_layout.addWidget(self.btn_view)
        action_layout.addWidget(self.btn_delete)
        action_layout.addStretch()
        action_layout.addWidget(self.btn_export)
        layout.addLayout(action_layout)
        
        container.setLayout(layout)
        
        # Connect signals
        self.btn_search.clicked.connect(self.search_students)
        self.search_edit.textChanged.connect(self.search_students)
        self.btn_view.clicked.connect(self.view_student_details)
        self.btn_delete.clicked.connect(self.delete_student)
        self.btn_export.clicked.connect(self.export_data)
        self.student_list.itemDoubleClicked.connect(self.view_student_details)
        
        return container
    
    # Simpan data mahasiswa
    def save_student(self):
        name = self.ledit_nama.text().strip()
        nim = self.ledit_nim.text().strip()
        
        if not name or not nim:
            self.show_message("Error", "Please fill in all required fields!", QMessageBox.Warning)
            return
        
        # Get selected date
        selected_date = self.calender_lahir.selectedDate()
        birth_date = f"{selected_date.day():02d}/{selected_date.month():02d}/{selected_date.year()}"
        
        # Get gender
        gender = "Male" if self.radio_male.isChecked() else "Female"
        
        # Get program study
        program_study = self.combo_study.currentText()
        
        # Save to database
        student = self.student_manager.add_student(name, nim, birth_date)
        
        # Show success message
        self.show_success_message(name, nim, birth_date, gender, program_study)
        
        # Clear form and refresh history
        self.clear_form()
        self.load_history()
    
    # Bersihkan formulir
    def clear_form(self):
        self.ledit_nama.clear()
        self.ledit_nim.clear()
        self.combo_study.setCurrentIndex(0)
        self.calender_lahir.setSelectedDate(QDate.currentDate())
        self.radio_male.setChecked(True)
    
    # Muat riwayat mahasiswa
    def load_history(self):
        self.student_list.clear()
        students = self.student_manager.get_all_students()
        
        for student in students:
            item_text = f"{student['name']} - {student['nim']} - {student['birth_date']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, student)
            self.student_list.addItem(item)
        
        self.stats_label.setText(f"Total Records: {len(students)}")
    
    # Cari mahasiswa
    def search_students(self):
        search_text = self.search_edit.text().lower()
        students = self.student_manager.get_all_students()
        
        self.student_list.clear()
        for student in students:
            if (search_text in student['name'].lower() or 
                search_text in student['nim'].lower()):
                item_text = f"{student['name']} - {student['nim']} - {student['birth_date']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, student)
                self.student_list.addItem(item)
    
    # Lihat detail mahasiswa
    def view_student_details(self):
        current_item = self.student_list.currentItem()
        if not current_item:
            self.show_message("Info", "Please select a student to view details.", QMessageBox.Information)
            return
        
        student = current_item.data(Qt.UserRole)
        
        # Create detailed view dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Student Details")
        dialog.setModal(True)
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Student details
        details_text = f"""
        <h3>Student Details</h3>
        <table style='width:100%; border-collapse: collapse;'>
        <tr><td style='padding:8px; font-weight:bold;'>Name:</td><td style='padding:8px;'>{student['name']}</td></tr>
        <tr><td style='padding:8px; font-weight:bold;'>Student ID:</td><td style='padding:8px;'>{student['nim']}</td></tr>
        <tr><td style='padding:8px; font-weight:bold;'>Date of Birth:</td><td style='padding:8px;'>{student['birth_date']}</td></tr>
        <tr><td style='padding:8px; font-weight:bold;'>Registered:</td><td style='padding:8px;'>{student['created_at']}</td></tr>
        </table>
        """
        
        details_label = QLabel(details_text)
        details_label.setWordWrap(True)
        layout.addWidget(details_label)
        
        # Close button
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    # Hapus mahasiswa
    def delete_student(self):
        current_item = self.student_list.currentItem()
        if not current_item:
            self.show_message("Info", "Please select a student to delete.", QMessageBox.Information)
            return
        
        student = current_item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete {student['name']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from data
            self.student_manager.students = [s for s in self.student_manager.students if s['id'] != student['id']]
            self.student_manager.save_data()
            self.load_history()
            self.show_message("Success", "Student record deleted successfully!", QMessageBox.Information)
    
    # Ekspor data mahasiswa
    def export_data(self):
        if not self.student_manager.students:
            self.show_message("Info", "No data to export.", QMessageBox.Information)
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Export Data", 
            f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    json.dump(self.student_manager.students, file, indent=4)
                self.show_message("Success", f"Data exported successfully to {filename}", QMessageBox.Information)
            except Exception as e:
                self.show_message("Error", f"Failed to export data: {str(e)}", QMessageBox.Critical)
    
    # Tampilkan pesan sukses dengan detail mahasiswa
    def show_success_message(self, name, nim, birth_date, gender, program_study):
        message = f"""
        <h3>Registration Successful!</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Student ID:</b> {nim}</p>
        <p><b>Date of Birth:</b> {birth_date}</p>
        <p><b>Gender:</b> {gender}</p>
        <p><b>Program Study:</b> {program_study}</p>
        <p style='color: #059669; font-weight: bold;'>✓ Data has been saved successfully!</p>
        """
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Success")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
    
    # Tampilkan pesan umum
    def show_message(self, title, message, icon):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Student Management System")
    app.setApplicationVersion("2.0")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ModernStudentForm()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()