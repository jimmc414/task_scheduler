import configparser
from datetime import datetime, timedelta
import calendar
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich import box
from pathlib import Path
from rich.tree import Tree

class TaskScheduler:
    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.console = Console()
        
    def is_business_day(self, date: datetime) -> bool:
        return date.weekday() < 5  # 0-4 are Monday to Friday
        
    def get_next_business_days(self, start_date: datetime, num_days: int) -> List[datetime]:
        business_days = []
        current_date = start_date
        while len(business_days) < num_days:
            if self.is_business_day(current_date):
                business_days.append(current_date)
            current_date += timedelta(days=1)
        return business_days
        
    def should_run_task(self, schedule: str, target_date: datetime) -> bool:
        if schedule.lower() == 'everyday':
            return True
            
        if schedule.lower().startswith('every '):
            day_name = schedule.lower().split('every ')[1]
            return calendar.day_name[target_date.weekday()].lower() == day_name.lower()
            
        if schedule.startswith('days:'):
            days = [int(d.strip()) for d in schedule[5:].split(',')]
            return target_date.day in days
            
        return False
        
    def get_tasks_for_date(self, target_date: datetime) -> Dict:
        tasks = {}
        
        for section in self.config.sections():
            parts = section.split('.')
            if len(parts) == 3:  # Client.Name.TaskName
                client = parts[1]
                task_name = parts[2]
                
                if self.should_run_task(self.config[section]['schedule'], target_date):
                    if client not in tasks:
                        tasks[client] = {}
                    
                    tasks[client][task_name] = dict(self.config[section])
                    
        return tasks
        
    def display_ascii_header(self):
        header = """
╔════════════════════════════════════════╗
║         Task Schedule Manager          ║
║         ───────────────────           ║
║    🕒 Planning Your Business Day 📋    ║
╚════════════════════════════════════════╝
        """
        self.console.print(Panel(header, style="bold blue", box=box.DOUBLE))
        
    def display_date_header(self, date: datetime):
        date_str = date.strftime("%A, %B %d, %Y")
        self.console.print(Panel(date_str, style="bold green", box=box.ROUNDED))
        
    def create_task_tree(self, tasks: Dict) -> Tree:
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
        business_days = self.get_next_business_days(today, 4)  # Today + 3 more
        
        layout = Layout()
        layout.split_column(
            Layout(name="header"),
            Layout(name="body"),
        )
        
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
    scheduler = TaskScheduler("tasks.ini")
    scheduler.run()