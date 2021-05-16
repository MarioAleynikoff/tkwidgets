import tkinter as tk
from tkinter import ttk
import copy
from dataclasses import dataclass

@dataclass(repr=True)
class Event:
    index: int
    value: any
    item_index: int = 0


"""
####################################### COMBOBOXCELL #########################################################
"""
class ComboboxCell(tk.Frame):

    def __init__(
            self, parent, text, check_fields: bool = False, callback: list = [],
            combobox_values: list = [], *args, **kwargs):
        super().__init__(
            parent, height=25, highlightthickness=0.5,
            highlightbackground="grey", *args, **kwargs)
        self.pack_propagate(0)

        self._check_fields = check_fields
        self._combo_values = combobox_values
        self._callbacks = callback
        self._init_val = text
        self._var = self.select_vartype(value=self._init_val)
        self._widget = ttk.Combobox(
            self,
            state='readonly',
            values=self._combo_values,
            textvariable=self._var
        )
        self._var.set(value=self._init_val)
        self._widget.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def select_vartype(self, value) -> tk:
        if isinstance(value, int):
            return tk.IntVar(value=value)
        elif isinstance(value, str):
            return tk.StringVar(value=value)
        elif isinstance(value, float):
            return tk.DoubleVar(value=value)
        elif isinstance(value, bool):
            return tk.BooleanVar(value=value)
        elif isinstance(value, type(None)):
            return self.select_vartype(value=self._combo_values[0])
        else:
            raise Exception("TABLE ERROR: UNKNOWN TYPE OF DATA CELL")

    def add_callback(self, callback: list):
        self._callbacks = callback

    def ok_command(self, num_cell):
        self.event = Event(
            index=num_cell,
            value=self._var.get(),
            item_index=self._widget.current()
        )

        if self._check_fields:
            result = self.with_check()
            return result
        else:
            result = self.without_check()
            return result


    def with_check(self):
        if bool(self._var.get()):
            if isinstance(self._callbacks, list):
                for i in range(len(self._callbacks)):
                    self._callbacks[i](self.event)
                    self._init_val = self._var.get()
                return True
            else:
                self._callbacks(self.event)
                self._init_val = self._var.get()
                return True
        else:
            return False


    def without_check(self):
        if self._var.get() != self._init_val:
            if isinstance(self._callbacks, list):
                for i in range(len(self._callbacks)):
                    self._callbacks[i](self.event)
                    self._init_val = self._var.get()
                return True
            else:
                self._callbacks(self.event)
                self._init_val = self._var.get()
                return True
        else:
            return True


    def set_col_index(self, index):
        pass


"""
####################################### LABELCELL #########################################################
"""

class LabelCell(tk.Frame):

    def __init__(self, parent, text, callback: list = [], *args, **kwargs):
        super().__init__(
            parent, height=25, highlightthickness=0.5,
            highlightbackground="grey", *args, **kwargs)
        self.pack_propagate(0)

        self._callbacks = callback
        self._init_val = text
        self._var = self.select_vartype(value=self._init_val)
        self._widget = tk.Label(self, bg='white', textvariable=self._var)
        self._widget.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._widget.bind('<Enter>', self.on_enter)
        self._widget.bind('<Leave>', self.on_leave)


    def select_vartype(self, value) -> tk:
        if isinstance(value, int):
            return tk.IntVar(value=value)
        elif isinstance(value, str):
            return tk.StringVar(value=value)
        elif isinstance(value, float):
            return tk.DoubleVar(value=value)
        elif isinstance(value, bool):
            return tk.BooleanVar(value=value)
        else:
            raise Exception("TABLE ERROR: UNKNOWN TYPE OF DATA CELL")

    def on_leave(self, event):
        self._widget.configure(bg='white')

    def on_enter(self, event):
        self._widget.configure(bg='light blue')

    def on_focusout(self, event):
        self._widget.configure(bg='white')

    def add_callback(self, callback: list):
        self._callbacks = callback

    def ok_command(self, num_cell):
        if self._var.get() != self._init_val:
            if isinstance(self._callbacks, list):
                for i in range(len(self._callbacks)):
                    self._callbacks[i]()
                    self._init_val = self._var.get()
            else:
                self._callbacks()
                self._init_val = self._var.get()
        else:
            None

    def set_col_index(self, index):
        pass


"""
####################################### ENTRYCELL #########################################################
"""

class EntryCell(tk.Frame):

    def __init__(self, parent, text, col_index, table_instance,
                 cell_index, callback: list = [], *args, **kwargs):
        super().__init__(parent, height=25, bd=0, *args, **kwargs)
        self.pack_propagate(0)

        self._table_instance = table_instance
        self._col_index = col_index
        self._cell_index = cell_index
        self._callbacks = callback
        self._init_val = text
        self._var = self.select_vartype(value=self._init_val)
        self._widget = ttk.Entry(
            self, justify=tk.CENTER, textvariable=self._var)
        self._widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #self._widget.bind("<Tab>", self.set_focus_onwidget)


    def select_vartype(self, value) -> tk:
        if isinstance(value, int):
            return tk.IntVar(value=value)
        elif isinstance(value, str):
            return tk.StringVar(value=value)
        elif isinstance(value, float):
            return tk.DoubleVar(value=value)
        elif isinstance(value, bool):
            return tk.BooleanVar(value=value)
        else:
            raise Exception("TABLE ERROR: UNKNOWN TYPE OF DATA CELL")

    def add_callback(self, callback: list):
        self._callbacks = callback

    def ok_command(self, num_cell):
        event = Event(index=num_cell, value=self._var.get())
        if self._var.get() != self._init_val:
            if isinstance(self._callbacks, list):
                for i in range(len(self._callbacks)):
                    self._callbacks[i](event)
                    self._init_val = self._var.get()
            else:
                self._callbacks(event)
                self._init_val = self._var.get()
        else:
            None

    def set_col_index(self, index):
        self._col_index = index

    def set_focus_onwidget(self, event):
        self._table_instance.focus_nextwidget(
            col_index=self._col_index, cell_index=self._cell_index)

"""
####################################### TABLE COLUMN #########################################################
"""

class TableColumn(tk.Frame):

    def __init__(self,
                 parent,
                 rows,
                 row_type: str,
                 title: str,
                 index: int = 0,
                 title_bg: str = None,
                 title_height : float = 2,
                 width: float = 3,
                 check_fields: bool = False,
                 callback: list = [],
                 combobox_values: list = None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack_propagate(1)
        self._title = title
        self._width = width
        self._title_bg = title_bg
        self._title_height = title_height
        self._rows_type = row_type
        self._rows = rows
        self._col_index = index
        self._cells = []
        self._combobox_values = combobox_values
        self._callback = callback
        self._parent = parent
        self._check_fields = check_fields
        self._cells_dict = dict()

        self.set_header()
        self.set_dataframe()
        self.set_rows()

        if self._callback:
            self.add_callback(self._callback)


    def set_dataframe(self):
        self.data_frame = tk.Frame(self, bg='white')
        self.data_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def set_header(self):
        self.header = tk.Label(
            self,
            text=self._title,
            width=self._width,
            height=self._title_height,
            bg=self._title_bg,
        )
        self.header.pack(side=tk.TOP, fill=tk.X)


    def set_rows(self):
        if self._rows_type == 'label':
            for i in range(len(self._rows)):
                idx = i
                i = LabelCell(
                    self.data_frame,
                    text=self._rows[i]
                )
                i.pack(side=tk.TOP, fill=tk.X)
                self._cells.append(i)
        elif self._rows_type == 'entry':
            for i in range(len(self._rows)):
                idx = i
                i = EntryCell(
                    self.data_frame,
                    text=self._rows[i],
                    col_index=self._col_index,
                    cell_index=idx,
                    table_instance=self._parent
                )
                i.pack(side=tk.TOP, fill=tk.X)
                self._cells.append(i)
        elif self._rows_type == 'combobox':
            for i in range(len(self._rows)):
                idx = i
                i = ComboboxCell(
                    self.data_frame,
                    text=self._rows[i],
                    combobox_values=self._combobox_values,
                    check_fields=self._check_fields
                )
                i.pack(side=tk.TOP, fill=tk.X)
                self._cells.append(i)

    def add_callback(self, callback: list):
        for i in range(len(self._cells)):
            self._cells[i].add_callback(callback=callback)

    def ok_command(self):
        for i in range(len(self._cells)):
            result = self._cells[i].ok_command(num_cell=i)
            if result:
                pass
            elif result == False:
                break
            else:
                pass

    def set_col_index(self, index):
        self._col_index = index
        for i in range(len(self._cells)):
            self._cells[i].set_col_index(index=index)


"""
####################################### TABLE #########################################################
"""

class Table(tk.PanedWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(bd=0, bg='grey', sashwidth=1, *args, **kwargs)
        self.pack_propagate(1)
        self._columns = []

    def add_columns(self, columns: list):
        for i in range(len(columns)):
            columns[i].set_col_index(index=i)
            self.add(columns[i])
            self._columns.append(columns[i])

    def ok_command(self):
        for i in range(len(self._columns)):
            self._columns[i].ok_command()

    def focus_nextwidget(self, col_index, cell_index):
        #cell = self._columns[col_index + 1]._cells[cell_index]
        print('col index', col_index, 'cel index', cell_index)
        widget = self._columns[col_index]._cells[cell_index]._widget
        widget.focus_set()
        widget.focus()
        self.update_idletasks()
        self.update()
        print(type(widget))
