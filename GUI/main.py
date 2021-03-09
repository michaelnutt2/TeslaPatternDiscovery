from tkinter import *
import reader

window = Tk()
window.minsize(800, 800)
window.title("Project 2")
window.config(padx=20, pady=20)

# Labels and Entries
eq_label = Label(text="Enter equations range", font=("Arial", 20))
eq_label.place(relx=0.2, rely=0.1, anchor='center')

min_entry = Entry(width=10)
min_entry.place(relx=0.1, rely=0.2, anchor='center')

max_entry = Entry(width=10)
max_entry.place(relx=0.3, rely=0.2, anchor='center')

to_label = Label(text="to", font=("Arial", 10))
to_label.place(relx=0.2, rely=0.2, anchor='center')

results_label = Label(text="Results Paths File Name", font=("Arial", 20))
results_label.place(relx=0.2, rely=0.7, anchor='center')

csv_entry = Entry(width=25)
csv_entry.place(relx=0.2, rely=0.8, anchor='center')


# Functions
def get_eq():
    """
    description
    """
    pass


def start():
    """
    description
    """
    # Creates the label above the output log "currently reading X.csv file"
    # When finishes running model will call import results function


def import_results():
    """
    Uses CsvReader to import CSV file and then formats for viewing
    """
    text = Text(window)

    text.place(relx=0.5, rely=0.2, relheigh=.5, relwidth=.4)
    output_dict = reader.read_json()

    text.insert(END, 'Original Equation: '+output_dict['original']+'\n\n')
    text.insert(END, 'Path:\n')

    for item in output_dict['Path1']:
        text.insert(END, item+'\n')


# Buttons
import_eq = Button(text="Import Equations", command=get_eq)
import_eq.place(relx=0.2, rely=0.5, anchor='center')

run = Button(text="RUN", command=start)
run.place(relx=0.2, rely=0.9, anchor='center')

import_path = Button(text="Import Results Path", command=import_results)
import_path.place(relx=0.7, rely=0.9, anchor='center')

window.mainloop()
