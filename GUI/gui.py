"""
Class for the GUI that also handles input generation and reading the output file to display in a text box on the gui.
"""
from tkinter import filedialog

import reader
from tkinter import *
import csv
import random
import pandas

from TeslaPatternDiscovery.GUI.VortextMathEnv import VortexMathEnv


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
        self.num_ops = 0

        self.window = Tk()

        self.window.minsize(800, 800)
        self.window.title("Tesla Pattern Discovery")
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

        # display_old_path_label = Label(text="View Old Paths", font=("Arial", 20))
        # display_old_path_label.place(relx=0.7, rely=0.8, anchor='center')

        self.page_label = Label(text=self.page, font=("Arial", 20))
        self.page_label.place(relx=0.675, rely=0.7)

        self.input_file_label = Label(text="", font=("Arial", 12))
        self.input_file_label.place(relx=0.1, rely=0.55)

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

        import_path = Button(text="Import Results Path", command=self.choose_file)
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
        if self.page < self.num_paths - 1:
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
        self.text.insert(END, 'Equation: ' + self.eqs[self.page] + '\n')
        self.text.insert(END, 'Total Number of Operations Run: ' + str(self.num_ops) + '\n\n')
        self.text.insert(END, 'Path:\n')

        self.page_label.config(text=self.page + 1)

        for item in self.paths[self.page]:
            self.text.insert(END, item + '\n')

    def get_eq(self):
        self.eq_file_path = filedialog.askopenfilename()
        self.input_file_label.config(text="Using Input File")
        self.eq_file_used = True

    def choose_file(self):
        self.results_path = filedialog.askopenfilename()
        self.import_results()

    def gen_values(self, output, min_value, max_value):
        """
        Runs through values from min to max to generate list of x*y*z=a values
        these values are later exported as csv. Screens the inputs to exclude all numbers with zeros in the digits.

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
                    if not self.has_zero_digit([i, j, k]):
                        val = i * j * k
                        output.append([val, i, j, k])

    def has_zero_digit(self, nums):
        for n in nums:
            if n % 10 == 0 or n % 100 == 0:
                return True
        return False

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

        self.input_file_label.config(text="")

        if results_path == "":
            results_path = "output.json"

        self.results_path = results_path

        if not self.eq_file_used:
            min_value = int(self.min_entry.get())
            max_value = int(self.max_entry.get())

            if min_value == "" or max_value == "":
                print("No value entered")
                return 'No value entered'
            if min_value < 100 or max_value > 1000:
                print("Invalid range")
                return 'Please enter a value with 3 digits'

            output = []

            self.gen_values(output, min_value, max_value)
            self.write_input(output)

        self.eq_file_used = False
        self.model(self.eq_file_path, self.results_path)
        self.import_results()

    def import_results(self):
        """
        Reads the output.json file, or whatever the user specified file is
        """
        self.eqs, self.paths = reader.read_json(self.results_path)
        self.num_paths = len(self.paths)

        self.display_results()

    def model(self, input_file, output_file):
        ds = reader.read_csv(input_file)
        qtable = reader.read_csv('q_table.csv')
        env = VortexMathEnv([ds.loc[0, 1], ds.loc[0, 2], ds.loc[0, 3]], ds.loc[0, 0], q_table=qtable)

        env.action_space.sample()

        episodes = 1
        epsilon = 0.1

        for episode in range(1, episodes + 1):
            state = env.reset()
            done = False
            score = 0

            while not done:
                if random.random() > epsilon:
                    action = random.choice(env.q_table.iloc[0][env.possible_ops].nlargest(1, keep='all').index)
                    n_state, reward, done, info = env.static_step(action)
                    score += reward
                else:
                    action = env.possible_ops[env.action_space.sample()]
                    n_state, reward, done, info = env.static_step(action)
                    score += reward

        self.num_ops = len(env.memory)
        op_list = self.compress(env.memory)
        out_list = self.convert_to_operations(op_list)

        env.memory = []

        val_a = str(ds.loc[0,1])
        val_b = str(ds.loc[0,2])
        val_c = str(ds.loc[0,3])
        ans = str(ds.loc[0,0])
        eq = val_a + ' x ' + val_b + ' x ' + val_c + ' = ' + ans

        out = {'equations': [eq], 'paths': [out_list]}
        reader.write_json(out, self.results_path)

    def compress(self, mem):
        """
        Compresses model output to combine all sequential entries into one set that
        has how many entries for that number as the [1] value
        :param mem: List generated from the model run of operations performed
        :return:
        """
        prev = -1
        num = 0
        new_list = []
        for item in mem:
            if item == prev:
                num += 1
            elif prev == -1:
                prev = item
            else:
                num += 1
                new_list.append((prev, num))
                num = 0
                prev = item

        return new_list

    def convert_to_operations(self, mem):
        """
        Converts the operations from raw numbers to string representations of
        the operations being run.
        :param mem:
        :return:
        """
        with open('newops.csv') as f:
            reader = csv.reader(f)
            operations = list(reader)

        out_list = []

        for item in mem:
            op = operations[item[0]]
            if op[2] == '0':
                out_list.append('+' + op[1] + ' (' + str(item[1]) + ' times)')
            elif op[2] == '1':
                out_list.append('-' + op[1] + ' (' + str(item[1]) + ' times)')
            elif op[2] == '2':
                out_list.append('x' + op[1] + ' (' + str(item[1]) + ' times)')
            elif op[2] == '3':
                out_list.append('/' + op[1] + ' (' + str(item[1]) + ' times)')

        return out_list


if __name__ == '__main__':
    gui = GUI()
