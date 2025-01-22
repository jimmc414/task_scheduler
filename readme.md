```markdown
# Task Scheduler

A **CLI-based task scheduling system** designed to manage and visualize scheduled tasks for multiple clients. This tool displays tasks due **today** and in the coming **business days** (by default, the next 3).

The goal of the Task Scheduler is to provide a clear, daily-oriented view of all tasks in your pipeline, highlighting which tasks need immediate attention and which tasks are coming up soon.

---

## Features

- **CLI interface** with color-coded display
- Shows tasks scheduled for **today** and the **next 3 business days**
- **Dynamic task loading** from configuration (INI) files
- **Hierarchical organization**:
  - Client → Task → Metadata
- **Multiple scheduling options** (daily, weekly, monthly)
- **Metadata support** for tasks (e.g., `priority`, `estimated_duration`, etc.)
- **Visual presentation** using Python’s [Rich](https://github.com/Textualize/rich) library


![image](https://github.com/user-attachments/assets/972f3f1a-5db9-4367-95c5-1798f86436ac)

---

## Installation

1. **Clone** the repository:
   ```bash
   git clone <repository-url>
   cd task_scheduler
   ```

2. **Install dependencies**:
   ```bash
   pip install rich
   ```

---

## Configuration

Tasks are stored in an **INI** file (by default `tasks.ini`), where each task is defined as a section. The section name must follow the format:
```
[Client.<CompanyName>.<TaskName>]
```
Inside each section, you provide a set of key-value pairs that describe the task. 

### Required Keys

- **schedule**  
  Defines **when** the task is scheduled:
  - `everyday`  
    Runs daily.
  - `every <weekday>`  
    Runs on a specific weekday (e.g., `every monday`).
  - `days:<day1>,<day2>`  
    Runs on specified dates of the month (e.g., `days:5,20`).

- **priority**  
  A priority label (e.g., `low`, `medium`, `high`, `critical`).

- **estimated_duration**  
  Estimated time to complete the task (e.g., `30m`, `1h`, `4h`).

- **description**  
  A brief explanation of the task.

### Example `tasks.ini`
**Task.ini Example**
![image](https://github.com/user-attachments/assets/3c7dd027-a5be-43d3-b9eb-bfcd58624eab)

```ini
[Client.Acme.daily_backup]
schedule = everyday
priority = high
estimated_duration = 30m
description = Perform daily backup of client systems

[Client.Acme.monthly_report]
schedule = days:1,15
priority = medium
estimated_duration = 2h
description = Generate and send monthly progress report

[Client.GlobalTech.weekly_maintenance]
schedule = every monday
priority = high
estimated_duration = 1h
description = Perform weekly system maintenance

[Client.GlobalTech.security_scan]
schedule = days:5,20
priority = critical
estimated_duration = 4h
description = Comprehensive security scan of all systems
```

---

## Importing Tasks

To **import** tasks into this scheduler, place or merge your tasks into the `tasks.ini` file (or any INI file you choose). Make sure your tasks follow the **INI structure** above.

### Using a Custom File

You can specify a different INI file by providing the path at initialization:
```python
scheduler = TaskScheduler("path/to/your_custom_tasks.ini")
scheduler.run()
```

### Dynamic Imports

If you have another source (e.g., a database, CSV, or JSON file), convert its contents to **INI format** programmatically. For example:

```python
import configparser

config = configparser.ConfigParser()

# Dynamically create or update tasks from another data source
config['Client.NewClient.new_task'] = {
    'schedule': 'every tuesday',
    'priority': 'medium',
    'estimated_duration': '2h',
    'description': 'Weekly review meeting with the team'
}

with open('tasks.ini', 'a') as configfile:
    config.write(configfile)
```

Then run:
```bash
python task_scheduler.py
```
The scheduler will read and display any tasks within the `tasks.ini` file.

---

## Usage

1. **Create or update** your `tasks.ini` following the structure above.
2. **Run the scheduler**:
   ```bash
   python task_scheduler.py
   ```
3. The output includes:
   - An **ASCII art header**.
   - **Date headers** for today and the next 3 **business days**.
   - A **hierarchical tree** of tasks organized by client.
   - Task information, including `priority`, `estimated_duration`, and `description`.

---

## Task Display

The tasks appear in a **hierarchical tree** structure. For example:
```
📅 Tasks
└── 👥 Acme
    ├── 📌 daily_backup
    │   ├── schedule: everyday
    │   ├── priority: high
    │   ├── estimated_duration: 30m
    │   └── description: Perform daily backup of client systems
    └── 📌 monthly_report
        ├── schedule: days:1,15
        ├── priority: medium
        ├── estimated_duration: 2h
        └── description: Generate and send monthly progress report
```
Similar sections for other clients will follow in the same tree.

---
