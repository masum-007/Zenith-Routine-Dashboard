Zenith Routine Dashboard

A modern, professional desktop routine planner built with Python and PyQt6. This application helps you organize your day, track your progress, and analyze your productivity with a beautiful, theme-aware interface.

[User Interface](https://imgur.com/a/PjVpjFq)

✨ Features

Elegant & Modern UI: A clean, "Zenith" design that is a pleasure to use.

Light & Dark Modes: An animated toggle to switch between a beautiful dark mode and a crisp light mode, with your preference saved.

Weekly Routine Templates: Set a default routine and create specific overrides for any day of the week (e.g., "Friday").

Daily Progress Tracking: A "live" dashboard that shows your tasks for the current day.

"Current Task" Highlighting: A glowing border automatically highlights the task you should be doing right now.

Task Notes & Categories: Add detailed notes and assign color-coded categories (e.g., "Study," "Work," "Health") to every task.

Professional Analytics: An analytics dashboard with three key reports:

Weekly Completion: A bar chart of your completion percentage for the last 7 days.

Time Allocation: A pie chart showing how your time is divided among your categories.

Progress Heatmap: A 35-day calendar heatmap to visualize your consistency.

Smart & User-Friendly:

"Smart Time Suggestion" in the editor.

12-hour (AM/PM) time format.

A custom, fully-styled date selector.

🚀 Installation & Setup

Follow these steps to run the project on your local machine.

1. Clone the Repository:

git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git)
cd YOUR-REPOSITORY-NAME


2. Create and Activate a Virtual Environment:
This project uses a virtual environment (.venv) to manage dependencies.

# On Windows (PowerShell):

# Create the environment
python -m venv .venv
# Activate the environment
.\.venv\Scripts\Activate.ps1


# On Windows (Command Prompt):

# Create the environment
python -m venv .venv
# Activate the environment
.\.venv\Scripts\activate.bat


3. Install Dependencies:
With your virtual environment activated, install the required libraries from requirements.txt:

pip install -r requirements.txt


4. Run the Application:

python main.py


The application will start, and it will automatically create a data/ folder in your project directory to store your personal tasks and settings.

🛠 Tech Stack

Python 3

PyQt6: The core UI framework.

PyQt6-Charts: Used to create the beautiful charts on the Analytics Dashboard.


This project was developed by Masum Al Mahamud.
