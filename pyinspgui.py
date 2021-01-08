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

    def open_node(event):
        for item in tree.selection():
            # clear
            for child in tree.get_children(item):
                tree.delete(child)
            # add
            item_name = tree.item(item)["text"]
            for mem2 in inspect.getmembers(target):
                if mem2[0] == item_name:
                    target2 = getattr(target, item_name)
                    if isinstance(target2, list):
                        for itr in target2:
                            tree.insert(item, "end", text="",
                                        values=(
                                            repr(itr), type(itr)))
                        break
                    if isinstance(target2, tuple):
                        for itr in target2:
                            tree.insert(item, "end", text="",
                                        values=(
                                            repr(itr), type(itr)))
                        break
                    if isinstance(target2, dict):
                        for k, v in target2.items():
                            tree.insert(item, "end", text=k,
                                        values=(
                                            repr(v), type(v)))
                        break
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
        if isinstance(mem, tuple):
            tree.insert(ti, "end", text="",
                        values=("", ""))

    tree.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


class Sample:
    def __init__(self):
        self.prop1 = [1, 2, 3]
        self.prop2 = ("x", "y", "z")
        self.prop3 = {"key": "a", "value": "b"}

    def method1(self, x, y):
        return x + y


if __name__ == "__main__":
    sample = Sample()
    show(sample)
