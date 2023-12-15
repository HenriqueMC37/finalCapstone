# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.
# 3. Besides the knowledge acquired through HyperionDev, I also used StackOverflow to clear doutbs 
# and "W3schools.com" when stuck in a particular part and needed to revisit built in functions

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

#defined function to read tasks.txt and place that content into a list, then returning it
def read_task():
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    #create task_list
    task_list = []
    for t_str in task_data:
        curr_t = {}

    # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)
    return task_list

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

#defined function to read user.txt and place that data into a dictionary, then returning it
def read_user():
# Read in user_data from the user.txt file
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

# Convert data to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password
    return username_password

#defined a function to login
def login(username_password):
    logged_in = False
    while not logged_in:

        print("\nUser Login\n")
        curr_user = input("Username:  ")
        curr_pass = input("Password:  ")
        #conditional statement to check if curr_user is in username_password
        if curr_user not in username_password.keys():
            print("\nUser does not exist. Try again.\n")
            continue
        #conditional statement to check if the password typed by the user matches the password for that user
        elif username_password[curr_user] != curr_pass:
            print("\nYou got the wrong password. Please try a different one.\n")
            continue
        else:
            print(f"\nLogin Successful. Welcome back {curr_user}.\n")
            logged_in = True
    return curr_user

#defined a function to register new users
def reg_user(username_password):
    # - Request input of a new username
    new_username = input("\nNew Username: ")
    #check to see if username is already in use
    #any of the files username_password
        
    if new_username in username_password.keys():
        print("\nUsername already in use. Please input a new one.\n")
        new_username = input("New Username: ")
        return


    # - Request input of a new password
    new_password = input("\nNew Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,

        print("\nNew user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
        return
        # - Otherwise you present a relevant message.
    else:
        print("\nPasswords do not match, please try again.")

#defined a function to add a task to the task list
def add_task(task_list, username_password):
    task_username = input("Name of person assigned to task: ")
    
    
    if task_username not in username_password.keys():
        print("This user does not exist. Please enter a valid username.")
        return
        
    task_title = input("Title of Task: ")

    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
  
    # Get the current date
    curr_date = date.today()
    ''' Add the data to the file tasks.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

'''defined a function to view every task that has been assigned to any user, these do not have identifying numbers but a feature could be added 
in which only the admin could edit any task, regardless of who the task was assigned to'''    
def view_all(task_list):

    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''

    for t in task_list:
        disp_str = f"\nTask: \t\t\t {t['title']}\n"
        disp_str += "-"*42
        disp_str += f"\nAssigned to: \t\t {t['username']}\n"
        disp_str += "-"*42
        disp_str += f"\nDate Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += "-"*42
        disp_str += f"\nDue Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += "-"*42
        disp_str += f"\nTask Description: \n\t- {t['description']}\n"
        disp_str += "-"*42
        disp_str += f"\nCompleted: \t\t {'Yes' if t['completed'] else 'No'}\n"
        disp_str += "-"*42
        print(disp_str)

#defined a function to view the current user's tasks, select them according to an identifying number and then either mark them as complete or edit them
def view_mine(task_list, curr_user):
    
    user_task_list = [t for t in task_list if t['username'] == curr_user]
    if not user_task_list:
        print("\nYou have no tasks assigned to you. Enjoy it while you can")
        return
    
    #By using the built in function enumerate, we're able to assign a number to a specific task
    for i, t in enumerate(user_task_list):
        disp_str = f"\nTask {i + 1}: \t\t\t {t['title']}\n"
        disp_str += "-"*42
        disp_str += f"\nAssigned to: \t\t {t['username']}\n"
        disp_str += "-"*42
        disp_str += f"\nDate Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += "-"*42
        disp_str += f"\nDue Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += "-"*42
        disp_str += f"\nTask Description: \n\t- {t['description']}\n"
        disp_str += "-"*42
        disp_str += f"\nCompleted: \t\t {'Yes' if t['completed'] else 'No'}\n"
        disp_str += "-"*42
        print(disp_str)
            
       
    while True:
        user_choice = int(input('''\nIf you'd like to choose a specific task please type its identifying number.\nIf you'd like to go back to the main menu, type "-1": '''))

        if user_choice == -1:
            break
        elif user_choice >= 1 and user_choice <= len(user_task_list):
            chosen_task = user_task_list[user_choice - 1]
            
            '''for chosen task in task list mark task as completed - input for yes or no which will change its value from false(no) to true(yes)
            or edit task (edit due date, task title and task description)'''
            
            if chosen_task["completed"]:
                print("\nThis task has already been completed and can no longer be edited.")
                continue
            
            print("\n1. Edit task")
            print("2. Mark task as completed")
            complete_task = input("\nPlease enter your choice (1 or 2): ").lower()

            '''mark the task as complete by changing its t['completed'] value to True. I had some difficulties with this as I wanted to get this value then changed in the actual 
            text file so the task's completion status would not reset the next time the task_manager was started. I am still trying to find a way to change it meanwhile'''
            if complete_task == "2":

                chosen_task['completed'] = True
                print("\nTask successfully marked as complete, thank you.")
                        
            elif complete_task == "1":
                while True:
                    print("\n1. Reassign the task.")
                    print("2. Edit Due Date")
                    print("3. Go back to main menu")
                    edit_choice = input("\nPlease input your choice (1, 2 or 3): ").lower()
                    if edit_choice == "1":
                        username_reassign = input("\nWho would you like to reassign this task to? " )
                        if username_reassign in username_password:
                            chosen_task["username"] = username_reassign
                            print("\nTask successfully reassigned.")
                        else: 
                            print("\nUsername not found. Please enter a valid username.")

                    #edit due date of task        
                    elif edit_choice == "2":
                        while True:
                            try:
                                new_task_due_date = input("New due date of task (YYYY-MM-DD): ")
                                new_due_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                                chosen_task["due_date"] = new_due_date_time
                                print("\nDue date successfuly edited.")
                                break
                            except ValueError:
                                print("Invalid datetime format. Please use the format specified")
                            
                    #go back to the main menu    
                    elif edit_choice == "3":
                        main_menu(username=curr_user)
                    else:
                        print("That's not a valid choice. Please try again.")
        else:
            print("\nThat was not a valid choice. Please try again.")
            
# defined a function to generate reports by creating two text files called task_ovrview.txt and user_overview.txt
def generate_reports(task_list, username_password):
    
    total_tasks = len(task_list)
    total_users = len(username_password.keys())
    #sum one for each task in task_list whose t['completed'] = True
    total_completed = sum(1 for t in task_list if t['completed'])
    total_uncompleted = total_tasks - total_completed
    #same as above but for the tasks not completed and whose current date is greater than the due date. I had some issues with finding the correct use of datetime.now().date()
    total_overdue = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < datetime.now().date())
   

    #create task_overview.txt if there isn't one and write the necessary statistics into the file 
    
    with open("task_overview.txt", "w+") as file_task_overview:
        file_task_overview.write(f"Total number of tasks: {str(total_tasks)}.\n")
        file_task_overview.write(f"Total number of completed tasks: {str(total_completed)}.\n")
        file_task_overview.write(f"Total number of uncompleted tasks: {str(total_uncompleted)}.\n")
        file_task_overview.write(f"Total number of overdue tasks: {str(total_overdue)}.\n")
        
        #only write these statistics if there is at least one task, so there isn't an error caused by dividing by zero
        if total_tasks > 0:
            percentage_incomplete = round((total_uncompleted / total_tasks) * 100, 2)
            percentage_overdue = round((total_overdue / total_tasks)*100, 2)
            file_task_overview.write(f"Percentage of incomplete tasks: {percentage_incomplete}%.\n")
            file_task_overview.write(f"Percentage of overdue tasks: {str(percentage_overdue)}%.\n")

    #create user_overview.txt if there isn't one and write the necessary statistics into the file
    
    with open("user_overview.txt", "w+") as file_user_overview:
        file_user_overview.write(f"Total number of tasks: {str(total_tasks)}\n")
        file_user_overview.write(f"Total number of users: {str(total_users)}\n")
        
        
        for username in username_password:
            #create user_task_list by iterating through the task list and select the tasks that match the username through each iteration of the above for loop
            user_task_list = [t for t in task_list if t['username'] == username]
            user_total_tasks = len(user_task_list)
            user_completed_tasks = sum(1 for t in user_task_list if t['completed'])
            user_uncompleted_tasks = user_total_tasks - user_completed_tasks
            user_overdue_tasks = sum(1 for t in user_task_list if not t['completed'] and t['due_date'].date() < datetime.now().date())          
            
            file_user_overview.write(f"\nUser:\t{username}\n\n")
            file_user_overview.write(f"Total number of tasks assigned to {username}: {str(user_total_tasks)}\n")

            # only write these statistics if there is at least one task, so there isn't an error caused by dividing by zero
            if user_total_tasks > 0:
                user_percentage_tasks = round((user_total_tasks / total_tasks) * 100, 2)
                user_percentage_comp_tasks = round((user_completed_tasks / user_total_tasks) * 100, 2)
                user_percentage_uncomp_tasks = round((user_uncompleted_tasks / user_total_tasks) * 100, 2)
                user_percentage_overdue_tasks = round((user_overdue_tasks / user_total_tasks) * 100, 2)
                file_user_overview.write(f"Percentage of Tasks assigned to {username}: {str(user_percentage_tasks)}%\n")
                file_user_overview.write(f"Percentage of Completed Tasks assigned to {username}: {str(user_percentage_comp_tasks)}%\n")
                file_user_overview.write(f"Percentage of Uncompleted Tasks assigned to {username}: {str(user_percentage_uncomp_tasks)}%\n")
                file_user_overview.write(f"Percentage of Overdue Tasks assigned to {username}: {str(user_percentage_overdue_tasks)}%\n")
    
    print("\nUser and task reports generated successfully.")
    print("You can access these reports by displaying statistics in the main menu.\n")


# defined a function to display statistics by reading the files created in generate_reports()
def display_statistics(task_list, username_password):

    # if those files don't exist, run the function generate_reports() to create them
    if not os.path.exists('user_overview.txt' and 'task_overview.txt'):
        generate_reports(task_list, username_password)

    # display user_overview by ready the file
    print("-"*70)
    print("User Statistics\n")
    with open('user_overview.txt', 'r') as user_display_file:
        print(user_display_file.read())
    
    print("-"*70)
    print("Task Statistics\n")
    # display task_overview by reading the file
    with open('task_overview.txt', 'r') as task_display_file:
        print(task_display_file.read())
        
# defined a funtion for menu that does the same as the initial menu but it's easier to read
def main_menu(username):
    user_admin = username == "admin"
    while True:
        print("\nMain Menu")
        print("r - Register an user" if user_admin else "")
        print("a - Adding a task")
        print("va - View all tasks")
        print("vm - view my tasks")
        print("gr - Generate reports" if user_admin else "")
        print("ds - Display Statistics" if user_admin else "")
        print("e - Exit\n")
        menu = input("Please select one of the above: ").lower()

        if menu == "r" and user_admin:
            reg_user(username_password)
        elif menu == "r" and not user_admin:
            print("You do not have the privileges register a new user.")
            continue
        elif menu == "a":
            add_task(task_list, username_password)
        elif menu == "va":
            view_all(task_list)
        elif menu == "vm":
            view_mine(task_list, username)
        elif menu == "gr" and user_admin:
            generate_reports(task_list, username_password)
        elif menu == "ds" and user_admin:
            display_statistics(task_list, username_password)
        elif menu == "e":
            print("Thank you for using this task manager. Goodbye!")
            exit()
        else:
            print("That is not one of the available choices, please try again.")
        
if __name__ == "__main__":
    task_list = read_task()
    username_password = read_user()
    curr_user = login(username_password)
    main_menu(curr_user)



        
