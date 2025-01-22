import configparser
from datetime import datetime, timedelta
import calendar
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.tree import Tree
import csv
import sys

class TaskScheduler:
    def __init__(self, config_file: str, csv_file: Optional[str] = None):
        self.config = configparser.ConfigParser()
        # Load tasks from INI file
        self.config.read(config_file)
        
        # If CSV file is provided, import additional tasks
        if csv_file:
            self.read_csv_tasks(csv_file)
        
        self.console = Console()
        
    def read_csv_tasks(self, csv_file: str) -> None:
        """Reads tasks from a CSV file and adds them to the config."""
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                client_name = row["Client"]
                task_name = row["TaskName"]
                section_name = f"Client.{client_name}.{task_name}"
                self.config.add_section(section_name)
                self.config.set(section_name, "schedule", row["Schedule"])
                self.config.set(section_name, "priority", row["Priority"])
                self.config.set(section_name, "estimated_duration", row["EstimatedDuration"])
                self.config.set(section_name, "description", row["Description"])

    def is_business_day(self, date: datetime) -&gt; bool:
        return date.weekday() &lt; 5  # Monday=0, Tuesday=1, ...

    def get_next_business_days(self, start_date: datetime, num_days: int) -&gt; List[datetime]:
        business_days = []
        current_date = start_date
        while len(business_days) &lt; num_days:
            if self.is_business_day(current_date):
                business_days.append(current_date)
            current_date += timedelta(days=1)
        return business_days

    def should_run_task(self, schedule: str, target_date: datetime) -&gt; bool:
        schedule = schedule.lower()
        if schedule == 'everyday':
            return True
        
        if schedule.startswith('every '):
            day_name = schedule.split('every ')[1]
            return calendar.day_name[target_date.weekday()].lower() == day_name
        
        if schedule.startswith('days:'):
            days = [int(d.strip()) for d in schedule[5:].split(',')]
            return target_date.day in days
        
        return False

    def get_tasks_for_date(self, target_date: datetime) -&gt; Dict:
        tasks = {}
        for section in self.config.sections():
            parts = section.split('.')
            if len(parts) == 3:  # [Client.<clientName>.<taskName>]
                client = parts[1]
                task_name = parts[2]
                
                schedule = self.config[section].get('schedule', '')
                if self.should_run_task(schedule, target_date):
                    if client not in tasks:
                        tasks[client] = {}
                    tasks[client][task_name] = dict(self.config[section])
        return tasks

    def display_ascii_header(self):
        header = """
╔════════════════════════════════════════╗
║         Task Schedule Manager          ║
║         ───────────────────            ║
║       Planning Your Business Day       ║
╚════════════════════════════════════════╝
        """
        self.console.print(Panel(header, style="bold blue", box=box.DOUBLE))

    def display_date_header(self, date: datetime):
        date_str = date.strftime("%A, %B %d, %Y")
        self.console.print(Panel(date_str, style="bold green", box=box.ROUNDED))

    def create_task_tree(self, tasks: Dict) -&gt; Tree:
        tree = Tree("📅 Tasks")
        for client, client_tasks in tasks.items():
            client_branch = tree.add(f"[bold blue]👥 {client}")
            for task_name, task_data in client_tasks.items():
                task_branch = client_branch.add(f"[bold green]📌 {task_name}")
                for meta_key, meta_value in task_data.items():
                    task_branch.add(f"[yellow]{meta_key}: {meta_value}")
        return tree

    def run(self):
        self.console.clear()
        self.display_ascii_header()

        today = datetime.now()
        # Today + next 3 business days
        business_days = self.get_next_business_days(today, 4)

        for date in business_days:
            self.display_date_header(date)
            tasks = self.get_tasks_for_date(date)
            if tasks:
                tree = self.create_task_tree(tasks)
                self.console.print(tree)
            else:
                self.console.print("[italic]No tasks scheduled for this day[/italic]\n")
            
            self.console.print("─" * 50 + "\n")


if __name__ == "__main__":
    csv_file = None
    
    if len(sys.argv) &gt;= 3:
        ini_file = sys.argv[1]
        csv_file = sys.argv[2]
    elif len(sys.argv) &gt;= 2:
        ini_file = sys.argv[1]
    else:
        ini_file = "tasks.ini"
    
    scheduler = TaskScheduler(config_file=ini_file, csv_file=csv_file)
    scheduler.run()
