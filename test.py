import tkinter as tk
from table import Table, TableColumn

root = tk.Tk()

table = Table(opaqueresize=True)
table.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

lista_1 = list(range(100))
col1 = TableColumn(
    table,
    width=15,
    title='titulo',
    row_type='label',
    rows=lista_1
)
col1.add_callback(callback=[lambda *x: print('callback_1')])

lista_2 = list(range(100))
col2 = TableColumn(
    table,
    width=10,
    title='titulo_2',
    row_type='entry',
    rows=lista_2,
    callback=[lambda *x: print('callback')]
)

table.add_columns([col1, col2])

but = tk.Button(root, text='boton', command=table.ok_command)
but.pack(side=tk.TOP)
root.mainloop()
