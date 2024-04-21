import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Function to fetch questions and options from MySQL database
def fetch_questions():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello@123!",
            database="project"
        )
        cursor = connection.cursor()

        # Fetch questions and options from the database table
        cursor.execute("SELECT * FROM vw_getquestionoption")
        questions = cursor.fetchall()

        connection.close()
        return questions
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to fetch questions: {error}")
        return []

# Function to handle the "Take Test" button click
def take_test():
    # Function to handle the "Submit" button click in the test window
    def submit():
        # Get name, age, and phone number from entry fields
        name = name_entry.get()
        age = age_entry.get()
        phoneno = phoneno_entry.get()

        # Validate name, age, and phone number
        if not name or not age.isdigit() or not phoneno.isdigit():
            messagebox.showerror("Error", "Please enter valid name, age, and phone number.")
            return

        # Get selected options for each question
        selected_options = []
        for i, var in enumerate(option_vars):
            selected_value = var.get()
            if selected_value == 'None':
                messagebox.showinfo("Input Error", f"Please select all options")
                return
            selected_options.append((f"Option {i + 1}", selected_value))

        # Implement submission logic here
        messagebox.showinfo("Test Submitted", f"The selected options are: {selected_options}")

        # Loop to generate insert query
        for i, var in enumerate(option_vars):
            selected_value = var.get()
            person_name = str(name)
            questionoptionid = int(var.get().split('(')[1].split(')')[0])
            questionid = int(i + 1)
            personage = int(age)
            phone_no = int(phoneno)
            insert_variables_into_table(person_name, questionoptionid, questionid, personage, phone_no)

    # Fetch questions from the database
    questions = fetch_questions()

    if not questions:
        return

    # Create test window
    test_window = tk.Toplevel(root)
    test_window.title("Take Test")

    # Create canvas for scrolling
    canvas = tk.Canvas(test_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbar
    scrollbar = tk.Scrollbar(test_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create frame to contain questions and options
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    # Create labels and entry fields for name, age, and phone number
    tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame, text="Age:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    age_entry = tk.Entry(frame)
    age_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(frame, text="Phone Number:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    phoneno_entry = tk.Entry(frame)
    phoneno_entry.grid(row=2, column=1, padx=5, pady=5)

    option_vars = []  # List to hold the IntVars for each question

    # Create question labels and option checkboxes
    for i, (question, *options) in enumerate(questions):
        tk.Label(frame, text=question).grid(row=i * 6 + 3, column=0, padx=5, pady=5, sticky="w")
        option_vars.append(tk.StringVar())  # Create a StringVar for each question

        for j, option in enumerate(options):
            option_vars[i].set(None)
            tk.Radiobutton(frame, text=option, variable=option_vars[i], value=option).grid(row=i * 6 + 4 + j, column=1,
                                                                                             padx=5, pady=2, sticky="w")

    # Create submit button
    tk.Button(frame, text="Submit", command=submit).grid(row=i * 6 + 9, columnspan=2, padx=5, pady=10)

    # Update canvas scroll region
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to insert records into the database
def insert_variables_into_table(person_name, questionoptionid, questionid, personage, phone_no):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='project',
                                             user='root',
                                             password='Hello@123!')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO personqa (person_name, questionoptionid, questionid, age, phone_no) 
                                VALUES (%s, %s, %s, %s, %s) """

        record = (person_name, questionoptionid, questionid, personage, phone_no)
        cursor.execute(mySql_insert_query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to fetch records based on selected criteria
def fetch_records(criteria):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello@123!",
            database="project"
        )
        cursor = connection.cursor()

        # Fetch records based on selected criteria
        cursor.execute(f"SELECT * FROM vw_getperson")
        records = cursor.fetchall()

        connection.close()
        return records
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to fetch records: {error}")
        return []

def display_result():
    selected_criteria = criteria_dropdown.get()

    # Extract the selected name and phone number from the selected criteria
    selected_name, selected_phone = selected_criteria.split(' | ')
    selected_name = selected_name[1:]  # Remove leading/trailing whitespace
    selected_phone = selected_phone[:-1]

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello@123!",
            database="project"
        )
        cursor = connection.cursor()

        # Execute the modified query with the selected name and phone number
        query = f"""SELECT a.person_name, a.age, c.personal_type, SUM(b.optionmarks) AS Totalmarks,  
                    CASE 
                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) > 0 THEN 'Extrovert' 
                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) <= 0 THEN 'Introvert' 
                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) > 0 THEN 'Thinking' 
                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) <= 0 THEN 'Feeling' 
                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) > 0 THEN 'Sensing' 
                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) <= 0 THEN 'Intuitive' 
                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) > 0 THEN 'Judging' 
                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) <= 0 THEN 'Perceiving' 
                    END AS PersonalityTrait 
                    FROM personqa AS a 
                    LEFT JOIN questionoptions AS b ON a.questionoptionid = b.questionoptionid 
                    LEFT JOIN personality_questions AS c ON a.questionid = c.questionid 
                    WHERE a.person_name = '{selected_name}' AND phone_no = {selected_phone}
                    GROUP BY a.person_name, a.age, c.personal_type"""

        cursor.execute(query)
        result = cursor.fetchall()

        # Create a new window to display the result in a table
        result_window = tk.Toplevel(root)
        result_window.title("Result")

        # Create a Treeview widget
        tree = ttk.Treeview(result_window)

        # Define columns
        columns = ["Name", "Age", "Personal Type", "Total Marks", "Personality Trait"]
        tree["columns"] = columns

        # Format columns
        for col in columns:
            tree.heading(col, text=col)

        # Insert data into the Treeview
        for row in result:
            tree.insert("", "end", values=row)

        # Pack the Treeview widget
        tree.pack(expand=True, fill="both")

        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to fetch result: {error}")


# Function to handle the "View Results" button click
def view_results():
    # Fetch records from the database
    records = fetch_records('')

    # Create "View Results" window
    results_window = tk.Toplevel(root)
    results_window.title("View Results")

    # Create dropdown menu to select criteria
    global criteria_var, criteria_dropdown 
    criteria_var = tk.StringVar()
    criteria_label = tk.Label(results_window, text="Select Person|Phone Number:")
    criteria_label.pack(pady=5)
    criteria_dropdown = ttk.Combobox(results_window, textvariable=criteria_var)
    criteria_dropdown['values'] = records
    criteria_dropdown.pack(pady=5)

    # Create "Display Result" button
    display_button = tk.Button(results_window, text="Display Result", command=display_result)
    display_button.pack(pady=10)
        
def run_matching_query():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello@123!",
            database="project"
        )
        cursor = connection.cursor()

        # Run the matching query to fetch all personality traits
        cursor.execute("""SELECT DISTINCT PersonalityTrait FROM (
                            SELECT 
                                a.person_name, 
                                a.phone_no, 
                                c.personal_type, 
                                SUM(b.optionmarks) AS Totalmarks, 
                                CASE 
                                    WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) > 0 THEN 'Extrovert' 
                                    WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) <= 0 THEN 'Introvert' 
                                    WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) > 0 THEN 'Thinking' 
                                    WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) <= 0 THEN 'Feeling' 
                                    WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) > 0 THEN 'Sensing' 
                                    WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) <= 0 THEN 'Intutive' 
                                    WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) > 0 THEN 'Judging' 
                                    WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) <= 0 THEN 'Perceiving' 
                                END AS PersonalityTrait 
                            FROM 
                                personqa AS a 
                            LEFT JOIN 
                                questionoptions AS b ON a.questionoptionid = b.questionoptionid 
                            LEFT JOIN 
                                personality_questions AS c ON a.questionid = c.questionid 
                            GROUP BY 
                                a.person_name, a.phone_no, c.personal_type
                        ) AS subquery""")
        personality_traits = cursor.fetchall()

        # Display the results in a new window
        matching_window = tk.Toplevel(root)
        matching_window.title("Matching Results")

        # Dropdown to select personality traits
        trait_var = tk.StringVar()
        trait_label = tk.Label(matching_window, text="Select The Personality type of the people you want to see:")
        trait_label.pack(pady=5)
        trait_dropdown = ttk.Combobox(matching_window, textvariable=trait_var)
        trait_dropdown['values'] = personality_traits
        trait_dropdown.pack(pady=10)

        # Function to display people with selected personality trait
        def display_people():
            selected_trait = trait_dropdown.get()

            try:
                # Re-establish the cursor connection
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Hello@123!",
                    database="project"
                )
                cursor = connection.cursor()

                # Fetch people with the selected personality trait
                cursor.execute(f"""SELECT person_name, phone_no FROM (
                                    SELECT 
                                        a.person_name, 
                                        a.phone_no, 
                                        c.personal_type, 
                                        SUM(b.optionmarks) AS Totalmarks, 
                                        CASE 
                                            WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) > 0 THEN 'Extrovert' 
                                            WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) <= 0 THEN 'Introvert' 
                                            WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) > 0 THEN 'Thinking' 
                                            WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) <= 0 THEN 'Feeling' 
                                            WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) > 0 THEN 'Sensing' 
                                            WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) <= 0 THEN 'Intutive' 
                                            WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) > 0 THEN 'Judging' 
                                            WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) <= 0 THEN 'Perceiving' 
                                        END AS PersonalityTrait 
                                    FROM 
                                        personqa AS a 
                                    LEFT JOIN 
                                        questionoptions AS b ON a.questionoptionid = b.questionoptionid 
                                    LEFT JOIN 
                                        personality_questions AS c ON a.questionid = c.questionid 
                                    GROUP BY 
                                        a.person_name, a.phone_no, c.personal_type
                                ) AS subquery 
                                WHERE 
                                    PersonalityTrait = '{selected_trait}'""")
                matching_results = cursor.fetchall()

                # Display the results in a messagebox
                messagebox.showinfo("Matching Results", f"People with {selected_trait} personality: {matching_results}")

            except mysql.connector.Error as error:
                messagebox.showerror("Database Error", f"Failed to fetch matching results: {error}")
            finally:
                if connection and connection.is_connected():
                    cursor.close()
                    connection.close()

        # Button to display people with selected personality trait
        display_button = tk.Button(matching_window, text="Display People", command=display_people)
        display_button.pack(pady=10)

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to fetch personality traits: {error}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def open_matching_window():
    run_matching_query()

# Main window
root = tk.Tk()
root.title("Test Application")

# Create buttons
tk.Button(root, text="Take Test", command=take_test).pack(pady=10)
tk.Button(root, text="View Results", command=view_results).pack(pady=10)

# Button to open the "Matching Window"
tk.Button(root, text="Matching Window", command=open_matching_window).pack(pady=10)

root.mainloop()