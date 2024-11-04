# Task Scheduler

CLI-based task scheduling system to manage and visualize scheduled tasks across multiple clients. Shows tasks due today and in the coming business days.

## Features

- CLI interface with ASCII art and color-coded displays
- Shows tasks for today and the next 3 business days
- Dynamic task loading from configuration files
- Hierarchical organization (Client -> Task -> Metadata)
- Multiple scheduling options
- Metadata support for tasks
- Visual presentation using Rich library

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd task-scheduler
```

2. Install required dependencies:
```bash
pip install rich
```

## Configuration

Tasks are defined in an INI file (`tasks.ini`):

```ini
[Client.CompanyName.TaskName]
schedule = <schedule-type>
priority = <priority-level>
estimated_duration = <duration>
description = <task-description>
```

### Schedule Types

Define task schedules in three ways:
1. Daily Tasks: `schedule = everyday`
2. Weekly Tasks: `schedule = every monday` (or any other day)
3. Monthly Tasks: `schedule = days:5,20` (runs on 5th and 20th of each month)

### Example Configuration

```ini
[Client.Acme.daily_backup]
schedule = everyday
priority = high
estimated_duration = 30m
description = Perform daily backup of client systems

[Client.GlobalTech.security_scan]
schedule = days:5,20
priority = critical
estimated_duration = 4h
description = System security scan
```

## Usage

1. Create your `tasks.ini` file with task configurations

2. Run the scheduler:
```bash
python task_scheduler.py
```

The program displays:
- ASCII art header
- Date headers for today and next 3 business days
- Task trees organized by client
- Task information including priority, duration, and description

## Task Display

Tasks appear in a hierarchical tree structure:
```
Tasks
├── Client Name
│   └── Task Name
│       ├── schedule: everyday
│       ├── priority: high
│       ├── estimated_duration: 1h
│       └── description: Task description
```

