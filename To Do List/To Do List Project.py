import tkinter as tk
import os


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow Pro")
        self.root.geometry("450x550")
        self.root.configure(bg="#1a1a1a")

        self.header = tk.Label(
            self.root,
            text="My Tasks",
            font=("Arial", 24, "bold"),
            bg="#1a1a1a",
            fg="white"
        )
        self.header.pack(anchor="w", padx=20, pady=(20, 10))

        self.input_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.input_frame.pack(fill="x", padx=20, pady=10)

        self.task_entry = tk.Entry(
            self.input_frame,
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="white",
            insertbackground="white",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#3f3f3f"
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        self.add_button = tk.Button(
            self.input_frame,
            text="Add",
            command=self.add_task,
            bg="#1f538d",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            width=8,
            height=2,
            activebackground="#14375e",
            activeforeground="white"
        )
        self.add_button.pack(side="right")

        self.canvas = tk.Canvas(self.root, bg="#242424", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#242424")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 20))

        self.load_tasks()

    def add_task(self, text=None):
        if text is None:
            text = self.task_entry.get()

        if text:
            row = tk.Frame(self.scrollable_frame, bg="#242424")
            row.pack(fill="x", pady=5)

            cb = tk.Checkbutton(
                row,
                text=text,
                bg="#242424",
                fg="white",
                font=("Arial", 11),
                selectcolor="#1a1a1a",
                activebackground="#242424",
                activeforeground="white"
            )
            cb.pack(side="left")

            del_btn = tk.Button(
                row,
                text="✕",
                command=lambda: self.delete_task(row),
                bg="#444444",
                fg="white",
                relief="flat",
                font=("Arial", 8),
                activebackground="#FF5555"
            )
            del_btn.pack(side="right", padx=5)

            if self.task_entry.get() == text:
                self.task_entry.delete(0, tk.END)

            self.save_tasks()

    def delete_task(self, row):
        row.destroy()
        self.root.after(100, self.save_tasks)

    def save_tasks(self):
        tasks = []
        for widget in self.scrollable_frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Checkbutton):
                    tasks.append(child.cget("text"))

        with open("tasks.txt", "w") as f:
            for task in tasks:
                f.write(task + "\n")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as f:
                for line in f:
                    task = line.strip()
                    if task:
                        self.add_task(task)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()