import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a Pandas DataFrame to store student data
student_data = pd.DataFrame(columns=['Name', 'Maths Score', 'English Score'])

# Check if a CSV file exists, and if so, load it
try:
    student_data = pd.read_csv('C:\\ct_internship_kl\\stu.csv')
except FileNotFoundError:
    pass

# Function to add a new student record
def add_student():
    name = name_entry.get()
    math_score = math_score_entry.get()
    english_score = english_score_entry.get()

    if not name or not math_score or not english_score:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        math_score = int(math_score)
        english_score = int(english_score)
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter valid numeric scores.")
        return

    if math_score > 100 or english_score > 100:
        messagebox.showwarning("Input Error", "Scores must be less than or equal to 100.")
        return

    student_data.loc[len(student_data)] = [name, math_score, english_score]
    update_display()
    clear_entries()
    update_chart()  # Update the chart

# Function to clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    math_score_entry.delete(0, tk.END)
    english_score_entry.delete(0, tk.END)

# Function to update the display with student data
def update_display():
    for i in tree.get_children():
        tree.delete(i)
    for index, row in student_data.iterrows():
        tree.insert("", tk.END, values=(row['Name'], row['Maths Score'], row['English Score']))

# Function to save student data to a CSV file
def save_to_csv():
    student_data.to_csv('C:\\ct_internship_kl\\stu.csv', index=False)
    messagebox.showinfo("Save Successful", "Student data saved to student_data.csv")

# Function to generate a bar chart
def generate_chart():
    plt.figure(figsize=(8, 6))
    
    bar_width = 0.35
    index = range(len(student_data))
    
    plt.bar(index, student_data['Maths Score'], width=bar_width, label='Maths Score')
    plt.bar([i + bar_width for i in index], student_data['English Score'], width=bar_width, label='English Score')
    
    plt.xlabel('Students')
    plt.ylabel('Scores')
    plt.title('Student Scores')
    plt.legend()
    plt.xticks([i + bar_width / 2 for i in index], student_data['Name'], rotation=45)
    
    # Embed the chart in the tkinter window
    global canvas
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to update the chart
def update_chart():
    # Clear the previous chart
    for widget in chart_frame.winfo_children():
        widget.destroy()
    generate_chart()  # Generate the updated chart

# Create the main tkinter window
root = tk.Tk()
root.title("Student Performance Tracker")

# Create labels and entry fields
name_label = tk.Label(root, text="Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

math_score_label = tk.Label(root, text="Math Score:")
math_score_label.pack()
math_score_entry = tk.Entry(root)
math_score_entry.pack()

english_score_label = tk.Label(root, text="English Score:")
english_score_label.pack()
english_score_entry = tk.Entry(root)
english_score_entry.pack()

# Create buttons
add_button = tk.Button(root, text="Add Student", command=add_student)
add_button.pack()

save_button = tk.Button(root, text="Save to CSV", command=save_to_csv)
save_button.pack()

# Create a Treeview widget for displaying student data
columns = ('Name', 'Maths Score', 'English Score')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('Name', text='Name')
tree.heading('Maths Score', text='Maths Score')
tree.heading('English Score', text='English Score')
tree.pack()

# Create a frame for the chart
chart_frame = tk.Frame(root)
chart_frame.pack()

# Generate and display the initial chart
generate_chart()

# Update the display with any pre-existing data
update_display()

# Start the tkinter main loop
root.mainloop()
