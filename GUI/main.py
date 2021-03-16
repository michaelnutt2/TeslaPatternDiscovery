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

# Error label
error_label = Label(text="Please input a valid dataset")
error_label.place(relx=0.2, rely=0.4, anchor='center')
error_label.place_forget()


# Functions
def get_eq():
    """
    Imports the test dataset: VortexDataset_Small
    """
    pass


def start():
    """
    description
    """
    # Creates the label above the output log "currently reading X.csv file"
    # When finishes running model will call import results function

    # Error check the inputs, if there are no inputs, import equations instead
    if(not screen_entry()):
        get_eq()

    # Last step
    import_results()


def import_results():
    """
    Uses CsvReader to import CSV file and then formats for viewing
    """
    eqs, paths = reader.read_json()

    # text.insert(END, 'Original Equation: '+eqs[i]+'\n\n')
    # text.insert(END, 'Path:\n')
    #
    # for item in paths[i]:
    #     text.insert(END, item+'\n')


def display_results():
    ...


def forward():
    ...


def back():
    ...

def screen_entry():
    # Read the number entries
    # Check if they fall in the proper range
    # Write the numbers between them into a CSV
    # Skip all the numbers with zeros in them

    begin = min_entry.get()
    end = max_entry.get()

    

    with open('user_in.csv', 'w+') as o_f:
        for i in range(begin, end):
            for j in range(begin, end):
                for k in range(begin, end):
                    if not has_zero_digit([i,j,k]):
                        line = str(ijk) + ',' + str(i) + ',' + str(j) + ',' + str(k) + '\n'
                        o_f.write(line)

    def has_zero_digit(nums):
        for n in nums:
            if n % 10 == 0 or n % 100 == 0:
                return True
        return False


# Text window
text = Text(window)

text.place(relx=0.5, rely=0.2, relheigh=.5, relwidth=.4)

# Buttons
# Import Equations
import_eq = Button(text="Import Equations", command=get_eq)     
import_eq.place(relx=0.2, rely=0.5, anchor='center')

# Start
run = Button(text="RUN", command=start)
run.place(relx=0.2, rely=0.9, anchor='center')

# Import Results Path
import_path = Button(text="Import Results Path", command=import_results)
import_path.place(relx=0.7, rely=0.9, anchor='center')

# Next and Back
forward_btn = Button(text="Next", command=forward)
forward_btn.place(relx=0.75, rely=0.7)
back_btn = Button(text="Back", command=back)
back_btn.place(relx=0.55, rely=0.7)

window.mainloop()
