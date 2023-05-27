# Overview
SRE Toil Tracker is a Python-based GUI application designed to track and manage laborious tasks, often referred to as 'toil'. This term is typically used to describe manual work that doesn't offer enduring value but is necessary nonetheless. The application provides an easy-to-use interface for creating, updating, and deleting task records, ensuring every necessary but mundane task is well-managed.

## Key Features
Create Records: Allows you to add new task records with associated details such as task description, task duration, and any pertinent comments.
View Records: Provides a comprehensive list view of all recorded tasks sorted by Toil Duration.
Update Records: Facilitates the modification of existing records. Simply double-click on a record in the interface to make changes.
Delete Records: Lets you remove selected task records through a right-click context menu or by entering the Toil ID and clicking "Remove Toil"
Database Integration: Ensures data persistence through synchronization with a SQLite3 database. Every operation performed on the GUI is reflected in the database.
### Installation
Ensure you have Python 3.6+ installed on your system. Follow the steps below to run this application:

Clone this repository to your local machine.
Navigate to the project directory.
Run these commands:

  bash
  python toil_tracker.py
  
### How to Use
To add a task record, fill in the form at the top of the application window and click 'Add Toil'.
To modify an existing task, fill in the form once more (including the toil ID) and press 'Edit Toil'
To delete a task, right-click on it and select 'Remove' or ended the Toil ID in the form and press 'Remove Toil'
To export your toil database click File -> 'Export To CSV'

### Future Plans
The goal is to further enhance this tool by incorporating features such as multi-user support, data export options, advanced search and filter functionalities, and more.

### Experiment Features
There is an experimental Dark Mode, but it is not currently working correctly to access that press File -> 'Toggle Theme'. Most things appear fine in Dark Mode with the exception of the Tree View.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
The development of this application was aided by OpenAI's ChatGPT.

## Contributing
Contributions are always welcome! Please ensure to follow the contribution guidelines. Feel free to open an issue or submit a pull request.

## Contact
If you have any queries, feedback, or suggestions, please don't hesitate to reach out.
