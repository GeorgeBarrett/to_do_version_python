import argparse
import settings
import itertools


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
        # Interpret the first command line argument, and redirect
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
        # Show all items in the todo file
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
        # Add a new item to the todo file
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["add"])
        parser.add_argument("item", type=str)
        args = parser.parse_args()

        with open(self.todo_file, "a") as f:  
            f.write(args.item.replace("\n", " ") + "\n")


if __name__ == "__main__":
    handler = Handler()
    handler.handle()