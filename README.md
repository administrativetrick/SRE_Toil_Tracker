[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT
# Overview
SRE Toil Tracker is a Python-based GUI application designed to track and manage laborious tasks, often referred to as 'toil'. This term is typically used to describe manual work that doesn't offer enduring value but is necessary nonetheless. The application provides an easy-to-use interface for creating, updating, and deleting task records, ensuring every necessary but mundane task is well-managed. This is not a replacement for Sprint Ceremonies, but rather an easy way for Engineers to track toil until they have time to create user stories and acceptance criteria for specific toil items. A step up from tracking time a tasks takes in a Spreadsheet.

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

### Dependencies
* The pyperclip module is a dependency for this application.

## Changelog

## V 1.0.5
* There is a known issue, when toil_duration_unit is set to 'Days" then the calcluations for days do not come out right. Removing the option for days in Combobox until this feature works.
* To achieve the same result you can use the hours Duration Unit with a Toil Duration of 8. This will simulate an 8 hour workday and still be calculated correctly.

## V 1.0.4
* Added a stopwatch to the bottom of the application to allow users to track time taken from start to finish of tasks straight form the application.
* Stopwatch timer is in seconds to allow users to track time easier.
* Made Windows slightly longer from 600 to 650 to allow the stopwatch to show appropriately.
* Stopwatch will also clear if the Stopwatch label is double-clicked.

## V 1.0.3
* Experimental Feature added, this feature adds a field showing Money saved by the Eliminated toil. This assumes a default salary of $80,000
  * This feature is an approximate and is not exact. It assumes a 5-day 8 hour per day work week with no holidays.
* New feature also shows potential money saved based off toil identified that has not yet been eliminated
* Money saved field is updated every 1 second
* Added additional module to show how much in non-eliminated toil is available, this can be used in future releases
* Preferences Field added to allow for the future configuration of Average Engineers Salary (Not yet functioning, need to add global variable or some other mechanism to share this configuration)

## V 1.0.2
* Added a time conversion utility that is accesible from the top Menu Bar
* Added a column for Eliminated, this allows to you track past Toil and identify if that toil has been elimiated or not
* Removed the first column in the treeview
* Adjusted the root window to be slightly wider to accomodate eliminated column
* Changed the default selection in the Time Conversion Tool to minutes

## V 1.0.1
* Added a search feature

## V 1.0
* User-Friendly Interface: The application is built with tkinter, a Python GUI library, resulting in a simple and intuitive interface that's easy to use for tracking and managing tasks.
* Task Addition: You can easily add new toil tasks, providing details such as task name, category, start and end times, and any relevant notes.
* Task Modification: Any toil task in the application can be modified. Simply double-click on a task in the table and the input fields will be auto-filled with the task details, which you can then modify as needed.
* Task Deletion: Single or multiple tasks can be removed easily from the task list. The right-click context menu allows for quick removal of selected tasks.
* Data Persistence: The application utilizes SQLite3 for data persistence. This means that any task added, modified, or deleted in the application is immediately reflected in the database. You don't need to worry about losing your tasks when the application is closed.
* Multitask Deletion: The application supports the deletion of multiple tasks at once. This feature enhances usability and saves time for users managing large amounts of toil.
* Clean and Organized Display: Tasks are neatly displayed in a tabular format, making it easy to view and manage all your toil in one place.
* Notification Messages: The application provides helpful feedback messages upon completion of various operations such as task deletion or modification. This ensures users are kept informed about their actions.
* CSV Export: A feature exists to export your tasks to a CSV file for later use.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
The development of this application was aided by OpenAI's ChatGPT.

## Contributing
Contributions are always welcome! Please ensure to follow the contribution guidelines. Feel free to open an issue or submit a pull request.

## Contact
If you have any queries, feedback, or suggestions, please don't hesitate to reach out.
