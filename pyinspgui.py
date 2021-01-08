import inspect
import tkinter as tk
import tkinter.ttk as ttk


def show(target):
    root = tk.Tk()
    tree = ttk.Treeview(root)
    tree["columns"] = ("value", "type")
    tree.heading("#0", text="Name", anchor=tk.W)
    tree.heading("value", text="Value", anchor=tk.W)
    tree.heading("type", text="Type", anchor=tk.W)

    def clear_children(node):
        for child in tree.get_children(node):
            tree.delete(child)

    def insert_node(parent, text, value):
        ti2 = tree.insert(parent, "end", text=text, values=(repr(value), type(value)))
        if isinstance(value, (list, tuple, dict)):
            tree.insert(ti2, "end", text="", values=("", ""))

    def open_node(event):
        items = tree.selection()
        if len(items) == 0:
            return
        item = items[0]
        item_name = tree.item(item)["text"]
        if len(item_name) == 0:
            print(tree.item(item))
            target2 = eval(tree.item(item)["values"][0])
        else:
            print("item_name")
            print(item_name)
            target2 = getattr(target, item_name)
        # clear
        clear_children(item)
        # add
        print("target2")
        print(target2)
        if isinstance(target2, (list, tuple)):
            for itr in target2:
                insert_node(item, "", itr)
                # ti2 = tree.insert(item, "end", text="", values=(repr(itr), type(itr)))
                # if isinstance(itr, (list, tuple, dict)):
                #     tree.insert(ti2, "end", text="", values=("", ""))
            return
        if isinstance(target2, dict):
            for k, v in target2.items():
                ti2 = tree.insert(item, "end", text=k, values=(repr(v), type(v)))
                if isinstance(v, (list, tuple, dict)):
                    tree.insert(ti2, "end", text="", values=("", ""))
            return
        for mem3 in inspect.getmembers(target2):
            ti2 = tree.insert(item, "end", text=mem3[0],
                              values=(repr(mem3[1]), type(mem3[1])))
            if isinstance(mem3, tuple):
                tree.insert(ti2, "end", text="",
                            values=("", ""))

    tree.bind('<<TreeviewOpen>>', open_node)

    for mem in inspect.getmembers(target):
        if mem[0].startswith("_"):
            continue
        ti = tree.insert("", "end", text=mem[0],
                         values=(repr(mem[1]), type(mem[1])))
        if callable(mem[1]):
            continue
        if isinstance(mem[1], (list, tuple, dict)):
            tree.insert(ti, "end", text="",
                        values=("", ""))

    tree.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


class Sample:
    def __init__(self, parent=None):
        self.parent = parent
        self.prop1 = [[1, 2, 3], [1, 2, 3], [1, 2, 3], ]
        self.prop2 = (["x", "y", "z"], ["x", "y", "z"], )
        self.prop3 = {"key": "a", "value": "b"}

    def method1(self, x, y):
        return x + y


if __name__ == "__main__":
    sample1 = Sample()
    sample2 = Sample(sample1)

    show(sample2)
