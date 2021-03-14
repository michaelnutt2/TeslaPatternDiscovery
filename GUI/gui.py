import reader
from tkinter import *
import csv


class GUI:
    def __init__(self):
        """
        Init all values, setting self for all values used later
        """
        self.eqs = None
        self.paths = None
        self.num_paths = 0
        self.page = 0
        self.results_path = "output.json"
        self.eq_file_used = False
        self.eq_file_path = "input.csv"

        self.window = Tk()

        self.window.minsize(800, 800)
        self.window.title("Project 2")
        self.window.config(padx=20, pady=20)

        # Labels and Entries
        eq_label = Label(text="Enter equations range", font=("Arial", 20))
        eq_label.place(relx=0.2, rely=0.1, anchor='center')

        self.min_entry = Entry(width=10)
        self.min_entry.place(relx=0.1, rely=0.2, anchor='center')

        self.max_entry = Entry(width=10)
        self.max_entry.place(relx=0.3, rely=0.2, anchor='center')

        to_label = Label(text="to", font=("Arial", 10))
        to_label.place(relx=0.2, rely=0.2, anchor='center')

        results_label = Label(text="Results Paths File Name", font=("Arial", 20))
        results_label.place(relx=0.2, rely=0.7, anchor='center')

        self.csv_entry = Entry(width=25)
        self.csv_entry.place(relx=0.2, rely=0.8, anchor='center')

        # Text window
        self.text = Text(self.window)

        self.text.place(relx=0.5, rely=0.2, relheigh=.5, relwidth=.4)

        # Buttons
        import_eq = Button(text="Import Equations", command=self.get_eq)
        import_eq.place(relx=0.2, rely=0.5, anchor='center')

        run = Button(text="RUN", command=self.start)
        run.place(relx=0.2, rely=0.9, anchor='center')

        import_path = Button(text="Import Results Path", command=self.import_results)
        import_path.place(relx=0.7, rely=0.9, anchor='center')

        forward_btn = Button(text="Next", command=self.forward)
        forward_btn.place(relx=0.75, rely=0.7)
        back_btn = Button(text="Back", command=self.backward)
        back_btn.place(relx=0.55, rely=0.7)

        self.window.mainloop()

    def forward(self):
        """
        Navigates forward a page in results, does nothing if max page reached
        """
        if self.page < self.num_paths-1:
            self.page = self.page + 1

        self.display_results()

    def backward(self):
        """
        Navigates back a page in results, does nothing if at page 0
        """
        if self.page > 0:
            self.page = self.page - 1

        self.display_results()

    def display_results(self):
        """
        Clears the text box, then fills based on what the page value is
        """
        self.text.delete(1.0, END)
        self.text.insert(END, 'Equation: '+self.eqs[self.page]+'\n\n')
        self.text.insert(END, 'Path:\n')

        for item in self.paths[self.page]:
            self.text.insert(END, item+'\n')

    def get_eq(self):
        ...

    @staticmethod
    def gen_values(output, min_value, max_value):
        """
        Runs through values from min to max to generate list of x*y*z=a values
        these values are later exported as csv

        :param output: list used to store output values
        :param min_value: minimum value to start from when generating values
        :param max_value: max value to generate values to
        """
        a = min_value
        b = min_value
        c = min_value

        for i in range(a, max_value):
            for j in range(b, max_value):
                for k in range(c, max_value):
                    val = i * j * k
                    output.append([val, i, j, k])

    def write_input(self, output):
        """
        Writes output list as csv for use in model
        :param output: list of values in answer, x, y, z format
        """
        with open(self.eq_file_path, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerows(output)

    def start(self):
        """
        Starts the model running, will first clear the text box
        then checks for user entered result path, user entered min/max values
        or user generated file.

        TODO is call the model and output actual output
        Once model is run will fill text box by calling the import results
        :return:
        """
        self.text.delete(1.0, END)
        self.page = 0
        results_path = self.csv_entry.get()

        if results_path == "":
            results_path = "output.json"

        self.results_path = results_path

        if not self.eq_file_used:
            min_value = self.min_entry.get()
            max_value = self.max_entry.get()

            if min_value == "" or max_value == "":
                return 'No value entered'

            output = []

            self.gen_values(output, int(min_value), int(max_value))
            self.write_input(output)

        self.import_results()

    def import_results(self):
        """
        Reads the output.json file, or whatever the user specified file is
        """
        self.eqs, self.paths = reader.read_json(self.results_path)
        self.num_paths = len(self.paths)

        self.display_results()


if __name__ == '__main__':
    gui = GUI()
