import argparse
import settings
import itertools
from datetime import datetime   

def get_today_time():
    return datetime.today().strftime('%Y-%m-%d')


class GetMaxLineNumber:
    # read line by line as we do not need to store it in memmory
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        with open(self.filename) as f:
            for counter in itertools.count():
                line = f.readline()
                if not line:
                    break
        return counter

class Handler:
    
    def __init__(self):
        self.todo_file = settings.TODO_FILE
        self.done_file = settings.DONE_FILE

    
    def handle(self):
        # interpret the first command line argument, and redirect
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action",
            choices=["add", "list", "delete", "do", "done", "pri"],
            help="The action to take",
        )
        parser.add_argument("other", nargs="*")
        args = parser.parse_args()

        action = getattr(self, args.action)
        action()

    
    def list(self):
        # show all items in the todo file
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["list"])
        parser.add_argument("filter", type=str, nargs="*")
        args = parser.parse_args()

        max_line_getter = GetMaxLineNumber(self.todo_file)
        max_line_num = max_line_getter.get()
        num_of_digits = len(str(max_line_num))
        printed_items = 0
        
        with open(self.todo_file) as f:
            items = f.readlines()

            if len(items) == 0:
                return
       
        sorted_items     = sorted((items, index+1) for index, items in enumerate(items))
        index_unranked   = next(index for index, item in enumerate(sorted_items) if item[0][0]  != '(')
        ranked_items     = sorted_items[0:index_unranked]
        unranked_items   = sorted(sorted_items[index_unranked::], key = lambda x: x[1])
        items            = ranked_items + unranked_items

        for item in items:
            if len(args.filter) == 0:
                    print(f"{item[1]:>{num_of_digits}} {item[0]}")
            else:
                    if args.filter[0] in item[0]:
                        printed_items += 1
                        print(f"{item[1]:>{num_of_digits}} {item[0]}")
        print(f"---\n{printed_items} item(s)")

    
    def add(self):
        # add a new item to the todo file
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["add"])
        parser.add_argument("item", type=str)
        args = parser.parse_args()

        with open(self.todo_file, "a") as f:  
            f.write(args.item.replace("\n", " ") + "\n")

    
    def delete(self):
        # delete an item from the todo file
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["delete"])
        parser.add_argument("line_number", type=int)
        args = parser.parse_args()

        with open(self.todo_file, "r") as f:
            items = f.readlines()
        
        list_index = args.line_number - 1

        if not len(items) > list_index:
            print(f"There is no item {args.line_number}. Please choose a number from 1 to {len(items)}")
            return
            
        with open(self.todo_file, "w") as f:
            new_todos = "".join(
                items[: list_index] + items[list_index + 1 :] 
            )
            f.write(new_todos)

        print(f"Deleted: {items[list_index].strip()}")
    

    def do(self):
        # move an item from the todo file to the done file
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["do"])
        parser.add_argument("line_number", type=int)
        args = parser.parse_args()
        
        list_index = args.line_number - 1

        if list_index < 0:
            print('Must start from 1')

        with open(self.todo_file, "r") as f:
            items = f.readlines()
        
        if not len(items) > list_index:
            print(f"There is no item {args.line_number}. Please choose a number from 1 to {len(items)}")
            return

        to_remove = items[list_index]
        with open(self.done_file, "a") as f:
            today_time = get_today_time()
            f.write(f"{items[list_index].strip()} ({today_time})\n")

        del items[list_index]

        with open(self.todo_file, "w") as f:
            f.write(''.join(items))

        print(f"Done: {to_remove.strip()}")


if __name__ == "__main__":
    handler = Handler()
    handler.handle()