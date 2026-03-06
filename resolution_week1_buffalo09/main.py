import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"


def load_tasks():
    """
    Loads Tasks from Json
    """
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent = 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type = str, nargs="?", help = "Task to add")
    parser.add_argument("-l", "--list", help="List all tasks", action ="store_true")
    parser.add_argument("-c", "--complete", type = int, help = "Mark a task complete using its ID")
    parser.add_argument("-d", "--delete", type = int, help = "delete a task")
    parser.add_argument("--due", type = str, help = "Add task Due Date YYYY-MM-DD")
    parser.add_argument("-e", "--edit", type = int, help = "Edit task with ID")
    parser.add_argument("-da", "--deleteall", help = "Delete all tasks", action = "store_true")
    args = parser.parse_args()



    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.list:
        tasks = load_tasks()
        if len(tasks) == 0:
            print(f"No tasks found")
        for task in tasks:
            status = "x" if task["done"] else " "
            due = task.get('due')
            if due:
                print(f"[{status}] {task['id']}: {task['task']} Due: {task['due']}")
            else:
                print(f"[{status}] {task['id']}: {task['task']}")
        sys.exit(0)
    elif args.task:
        tasks = load_tasks()
        if not args.edit:
            print(tasks)
            if len(tasks) == 0:
                id = 1
            else:
                id = tasks[-1]["id"] + 1
        #add to json
            tasks.append({
                "id": id, 
                "task": args.task, 
                "done": False, 
                "due": args.due})
                
            save_task(tasks)

            print(f"Task {args.task} added with ID of {id}")
        else:
            tasks = load_tasks()
        for task in tasks:
            if task['id'] == args.edit:
                task['task'] = args.task
                save_task(tasks)
                print(f"Changed task to {args.task}")
                break

    elif args.complete:
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.complete:
                task["done"] = True
                save_task(tasks)
                print(f"Task {args.complete} complete")
                break
    elif args.delete:
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.delete:
                tasks.remove(task)
                save_task(tasks)
                print(f"Task {args.delete} removed")
                break
    
    #delete all tasks
    elif args.deleteall:
        tasks = load_tasks()
        tasks.clear()
        save_task(tasks)
        print(f"All tasks removed")


if __name__ == "__main__":
    main()