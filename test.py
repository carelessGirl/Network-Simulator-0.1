# # __author__ = 'sjha1'



#from constants import WIDTH,HEIGHT

# #
# # import Tkinter as tk
# # import tkFont
# #
# # class SampleApp(tk.Tk):
# #     def __init__(self, *args, **kwargs):
# #         tk.Tk.__init__(self, *args, **kwargs)
# #         self._textFont = tkFont.Font(name="TextFont")
# #         self._textFont.configure(**tkFont.nametofont("TkDefaultFont").configure())
# #
# #         toolbar = tk.Frame(self, borderwidth=0)
# #         container = tk.Frame(self, borderwidth=1, relief="sunken",
# #                              width=600, height=600)
# #         container.grid_propagate(False)
# #         toolbar.pack(side="top", fill="x")
# #         container.pack(side="bottom", fill="both", expand=True)
# #
# #         container.grid_rowconfigure(0, weight=1)
# #         container.grid_columnconfigure(0, weight=1)
# #         text = tk.Text(container, font="TextFont")
# #         text.grid(row=0, column=0, sticky="nsew")
# #
# #         zoomin = tk.Button(toolbar, text="+", command=self.zoom_in)
# #         zoomout = tk.Button(toolbar, text="-", command=self.zoom_out)
# #         zoomin.pack(side="left")
# #         zoomout.pack(side="left")
# #
# #         text.insert("end", '''Press te + and - buttons to increase or decrease the font size''')
# #
# #     def zoom_in(self):
# #         font = tkFont.nametofont("TextFont")
# #         size = font.actual()["size"]+2
# #         font.configure(size=size)
# #
# #     def zoom_out(self):
# #         font = tkFont.nametofont("TextFont")
# #         size = font.actual()["size"]-2
# #         font.configure(size=max(size, 8))
# #
# # if __name__ == "__main__":
# #     app = SampleApp()
# #     app.mainloop()
#
#
# # from Tkinter import *
# # import tkFont
# # root=Tk()
# # dFont=tkFont.Font(family="Arial", size=30)
# # def killme():
# #     root.quit()
# #     root.destroy()
# # LB=Text(root, width=16, height=5, font=dFont)
# # LB.grid(row=0, column=0, sticky=W+N+S)
# # yscrollbar=Scrollbar(root, orient=VERTICAL, command=LB.yview)
# # yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)
# # LB["yscrollcommand"]=yscrollbar.set
# # LB.update()
# # h=int(round(LB.winfo_height()/LB["height"])), int(round(LB.winfo_width()/LB["width"]))
# # def resize(event):
# #
# #     pixelX=root.winfo_width()-yscrollbar.winfo_width()
# #     pixelY=root.winfo_height()
# #     LB["width"]=int(round(pixelX/h[1]))
# #     LB["height"]=int(round(pixelY/h[0]))
# # root.bind("<Configure>", resize)
# # root.mainloop()
#
# # from Tkinter import *
# #
# # master = Tk()
# #
# # scrollbar = Scrollbar(master)
# # scrollbar.pack(side=RIGHT, fill=Y)
# #
# # listbox = Listbox(master, yscrollcommand=scrollbar.set)
# # for i in range(15):
# #     listbox.insert(END, str(i))
# # listbox.pack(side=LEFT, fill=BOTH)
# #
# # scrollbar.config(command=listbox.yview)
# #
# # mainloop()
#
# import Tkinter as tk
#
# class Example(tk.Frame):
#     def __init__(self, root):
#
#         tk.Frame.__init__(self, root)
#         self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
#         self.frame = tk.Frame(self.canvas, background="#ffffff")
#         self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.vsb.set)
#
#         self.vsb.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((4,4), window=self.frame, anchor="nw",
#                                   tags="self.frame")
#
#         self.frame.bind("<Configure>", self.onFrameConfigure)
#
#         self.populate()
#
#     def populate(self):
#         '''Put in some fake data'''
#         for row in range(100):
#             tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
#                      relief="solid").grid(row=row, column=0)
#             t="this is the second column for row %s" %row
#             tk.Label(self.frame, text=t).grid(row=row, column=1)
#
#     def onFrameConfigure(self, event):
#         '''Reset the scroll region to encompass the inner frame'''
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
# if __name__ == "__main__":
#     root=tk.Tk()
#     Example(root).pack(side="top", fill="both", expand=True)
#     root.mainloop()

# At some point, we should rewrite this tool to use the new canvas
# widget system.



import nltk.compat
import pickle
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter
import math
import os.path
import tkinter.font, tkinter.messagebox

from nltk.parse.chart import (BottomUpPredictCombineRule, BottomUpPredictRule,
                              Chart, LeafEdge, LeafInitRule, SingleEdgeFundamentalRule,
                              SteppingChartParser, TopDownInitRule, TopDownPredictRule,
                              TreeEdge)
from nltk.tree import Tree
from nltk.grammar import Nonterminal, CFG
from nltk.util import in_idle
from nltk.draw.util import (CanvasFrame, ColorizedList,
                            EntryDialog, MutableOptionMenu,
                            ShowText, SymbolWidget)
from nltk.draw import CFGEditor, tree_to_treesegment, TreeSegmentWidget

# Known bug: ChartView doesn't handle edges generated by epsilon
# productions (e.g., [Production: PP -> ]) very well.

#######################################################################
# Edge List
#######################################################################

class EdgeList(ColorizedList):
    ARROW = SymbolWidget.SYMBOLS['rightarrow']

    def _init_colortags(self, textwidget, options):
        textwidget.tag_config('terminal', foreground='#006000')
        textwidget.tag_config('arrow', font='symbol', underline='0')
        textwidget.tag_config('dot', foreground = '#000000')
        textwidget.tag_config('nonterminal', foreground='blue',
                              font=('helvetica', -12, 'bold'))

    def _item_repr(self, item):
        contents = []
        contents.append(('%s\t' % item.lhs(), 'nonterminal'))
        contents.append((self.ARROW, 'arrow'))
        for i, elt in enumerate(item.rhs()):
            if i == item.dot():
                contents.append((' *', 'dot'))
            if isinstance(elt, Nonterminal):
                contents.append((' %s' % elt.symbol(), 'nonterminal'))
            else:
                contents.append((' %r' % elt, 'terminal'))
        if item.is_complete():
            contents.append((' *', 'dot'))
        return contents

#######################################################################
# Chart Matrix View
#######################################################################

class ChartMatrixView(object):
    """
    A view of a chart that displays the contents of the corresponding matrix.
    """
    def __init__(self, parent, chart, toplevel=True, title='Chart Matrix',
                 show_numedges=False):
        self._chart = chart
        self._cells = []
        self._marks = []

        self._selected_cell = None

        if toplevel:
            self._root = tkinter.Toplevel(parent)
            self._root.title(title)
            self._root.bind('<Control-q>', self.destroy)
            self._init_quit(self._root)
        else:
            self._root = tkinter.Frame(parent)

        self._init_matrix(self._root)
        self._init_list(self._root)
        if show_numedges:
            self._init_numedges(self._root)
        else:
            self._numedges_label = None

        self._callbacks = {}

        self._num_edges = 0

        self.draw()

    def _init_quit(self, root):
        quit = tkinter.Button(root, text='Quit', command=self.destroy)
        quit.pack(side='bottom', expand=0, fill='none')

    def _init_matrix(self, root):
        cframe = tkinter.Frame(root, border=2, relief='sunken')
        cframe.pack(expand=0, fill='none', padx=1, pady=3, side='top')
        self._canvas = tkinter.Canvas(cframe, width=200, height=200,
                                      background='white')
        self._canvas.pack(expand=0, fill='none')

    def _init_numedges(self, root):
        self._numedges_label = tkinter.Label(root, text='0 edges')
        self._numedges_label.pack(expand=0, fill='none', side='top')

    def _init_list(self, root):
        self._list = EdgeList(root, [], width=20, height=5)
        self._list.pack(side='top', expand=1, fill='both', pady=3)
        def cb(edge, self=self): self._fire_callbacks('select', edge)
        self._list.add_callback('select', cb)
        self._list.focus()

    def destroy(self, *e):
        if self._root is None: return
        try: self._root.destroy()
        except: pass
        self._root = None

    def set_chart(self, chart):
        if chart is not self._chart:
            self._chart = chart
            self._num_edges = 0
            self.draw()

    def update(self):
        if self._root is None: return

        # Count the edges in each cell
        N = len(self._cells)
        cell_edges = [[0 for i in range(N)] for j in range(N)]
        for edge in self._chart:
            cell_edges[edge.start()][edge.end()] += 1

        # Color the cells correspondingly.
        for i in range(N):
            for j in range(i, N):
                if cell_edges[i][j] == 0:
                    color = 'gray20'
                else:
                    color = ('#00%02x%02x' %
                             (min(255, 50+128*cell_edges[i][j]/10),
                              max(0, 128-128*cell_edges[i][j]/10)))
                cell_tag = self._cells[i][j]
                self._canvas.itemconfig(cell_tag, fill=color)
                if (i,j) == self._selected_cell:
                    self._canvas.itemconfig(cell_tag, outline='#00ffff',
                                            width=3)
                    self._canvas.tag_raise(cell_tag)
                else:
                    self._canvas.itemconfig(cell_tag, outline='black',
                                            width=1)

        # Update the edge list.
        edges = list(self._chart.select(span=self._selected_cell))
        self._list.set(edges)

        # Update our edge count.
        self._num_edges = self._chart.num_edges()
        if self._numedges_label is not None:
            self._numedges_label['text'] = '%d edges' % self._num_edges

    def activate(self):
        self._canvas.itemconfig('inactivebox', state='hidden')
        self.update()

    def inactivate(self):
        self._canvas.itemconfig('inactivebox', state='normal')
        self.update()

    def add_callback(self, event, func):
        self._callbacks.setdefault(event,{})[func] = 1

    def remove_callback(self, event, func=None):
        if func is None: del self._callbacks[event]
        else:
            try: del self._callbacks[event][func]
            except: pass

    def _fire_callbacks(self, event, *args):
        if event not in self._callbacks: return
        for cb_func in list(self._callbacks[event].keys()): cb_func(*args)

    def select_cell(self, i, j):
        if self._root is None: return

        # If the cell is already selected (and the chart contents
        # haven't changed), then do nothing.
        if ((i,j) == self._selected_cell and
            self._chart.num_edges() == self._num_edges): return

        self._selected_cell = (i,j)
        self.update()

        # Fire the callback.
        self._fire_callbacks('select_cell', i, j)

    def deselect_cell(self):
        if self._root is None: return
        self._selected_cell = None
        self._list.set([])
        self.update()

    def _click_cell(self, i, j):
        if self._selected_cell == (i,j):
            self.deselect_cell()
        else:
            self.select_cell(i, j)

    def view_edge(self, edge):
        self.select_cell(*edge.span())
        self._list.view(edge)

    def mark_edge(self, edge):
        if self._root is None: return
        self.select_cell(*edge.span())
        self._list.mark(edge)

    def unmark_edge(self, edge=None):
        if self._root is None: return
        self._list.unmark(edge)

    def markonly_edge(self, edge):
        if self._root is None: return
        self.select_cell(*edge.span())
        self._list.markonly(edge)

    def draw(self):
        if self._root is None: return
        LEFT_MARGIN = BOT_MARGIN = 15
        TOP_MARGIN = 5
        c = self._canvas
        c.delete('all')
        N = self._chart.num_leaves()+1
        dx = (int(c['width'])-LEFT_MARGIN)/N
        dy = (int(c['height'])-TOP_MARGIN-BOT_MARGIN)/N

        c.delete('all')

        # Labels and dotted lines
        for i in range(N):
            c.create_text(LEFT_MARGIN-2, i*dy+dy/2+TOP_MARGIN,
                          text=repr(i), anchor='e')
            c.create_text(i*dx+dx/2+LEFT_MARGIN, N*dy+TOP_MARGIN+1,
                          text=repr(i), anchor='n')
            c.create_line(LEFT_MARGIN, dy*(i+1)+TOP_MARGIN,
                          dx*N+LEFT_MARGIN, dy*(i+1)+TOP_MARGIN, dash='.')
            c.create_line(dx*i+LEFT_MARGIN, TOP_MARGIN,
                          dx*i+LEFT_MARGIN, dy*N+TOP_MARGIN, dash='.')

        # A box around the whole thing
        c.create_rectangle(LEFT_MARGIN, TOP_MARGIN,
                           LEFT_MARGIN+dx*N, dy*N+TOP_MARGIN,
                           width=2)

        # Cells
        self._cells = [[None for i in range(N)] for j in range(N)]
        for i in range(N):
            for j in range(i, N):
                t = c.create_rectangle(j*dx+LEFT_MARGIN, i*dy+TOP_MARGIN,
                                       (j+1)*dx+LEFT_MARGIN,
                                       (i+1)*dy+TOP_MARGIN,
                                       fill='gray20')
                self._cells[i][j] = t
                def cb(event, self=self, i=i, j=j): self._click_cell(i,j)
                c.tag_bind(t, '<Button-1>', cb)

        # Inactive box
        xmax, ymax = int(c['width']), int(c['height'])
        t = c.create_rectangle(-100, -100, xmax+100, ymax+100,
                               fill='gray50', state='hidden',
                               tag='inactivebox')
        c.tag_lower(t)

        # Update the cells.
        self.update()

    def pack(self, *args, **kwargs):
        self._root.pack(*args, **kwargs)

#######################################################################
# Chart Results View
#######################################################################

class ChartResultsView(object):
    def __init__(self, parent, chart, grammar, toplevel=True):
        self._chart = chart
        self._grammar = grammar
        self._trees = []
        self._y = 10
        self._treewidgets = []
        self._selection = None
        self._selectbox = None

        if toplevel:
            self._root = tkinter.Toplevel(parent)
            self._root.title('Chart Parser Application: Results')
            self._root.bind('<Control-q>', self.destroy)
        else:
            self._root = tkinter.Frame(parent)

        # Buttons
        if toplevel:
            buttons = tkinter.Frame(self._root)
            buttons.pack(side='bottom', expand=0, fill='x')
            tkinter.Button(buttons, text='Quit',
                           command=self.destroy).pack(side='right')
            tkinter.Button(buttons, text='Print All',
                           command=self.print_all).pack(side='left')
            tkinter.Button(buttons, text='Print Selection',
                           command=self.print_selection).pack(side='left')

        # Canvas frame.
        self._cframe = CanvasFrame(self._root, closeenough=20)
        self._cframe.pack(side='top', expand=1, fill='both')

        # Initial update
        self.update()

    def update(self, edge=None):
        if self._root is None: return
        # If the edge isn't a parse edge, do nothing.
        if edge is not None:
            if edge.lhs() != self._grammar.start(): return
            if edge.span() != (0, self._chart.num_leaves()): return

        for parse in self._chart.parses(self._grammar.start()):
            if parse not in self._trees:
                self._add(parse)

    def _add(self, parse):
        # Add it to self._trees.
        self._trees.append(parse)

        # Create a widget for it.
        c = self._cframe.canvas()
        treewidget = tree_to_treesegment(c, parse)

        # Add it to the canvas frame.
        self._treewidgets.append(treewidget)
        self._cframe.add_widget(treewidget, 10, self._y)

        # Register callbacks.
        treewidget.bind_click(self._click)

        # Update y.
        self._y = treewidget.bbox()[3] + 10

    def _click(self, widget):
        c = self._cframe.canvas()
        if self._selection is not None:
            c.delete(self._selectbox)
        self._selection = widget
        (x1, y1, x2, y2) = widget.bbox()
        self._selectbox = c.create_rectangle(x1, y1, x2, y2,
                                             width=2, outline='#088')

    def _color(self, treewidget, color):
        treewidget.label()['color'] = color
        for child in treewidget.subtrees():
            if isinstance(child, TreeSegmentWidget):
                self._color(child, color)
            else:
                child['color'] = color

    def print_all(self, *e):
        if self._root is None: return
        self._cframe.print_to_file()

    def print_selection(self, *e):
        if self._root is None: return
        if self._selection is None:
            tkinter.messagebox.showerror('Print Error', 'No tree selected')
        else:
            c = self._cframe.canvas()
            for widget in self._treewidgets:
                if widget is not self._selection:
                    self._cframe.destroy_widget(widget)
            c.delete(self._selectbox)
            (x1,y1,x2,y2) = self._selection.bbox()
            self._selection.move(10-x1,10-y1)
            c['scrollregion'] = '0 0 %s %s' % (x2-x1+20, y2-y1+20)
            self._cframe.print_to_file()

            # Restore our state.
            self._treewidgets = [self._selection]
            self.clear()
            self.update()

    def clear(self):
        if self._root is None: return
        for treewidget in self._treewidgets:
            self._cframe.destroy_widget(treewidget)
        self._trees = []
        self._treewidgets = []
        if self._selection is not None:
            self._cframe.canvas().delete(self._selectbox)
        self._selection = None
        self._y = 10

    def set_chart(self, chart):
        self.clear()
        self._chart = chart
        self.update()

    def set_grammar(self, grammar):
        self.clear()
        self._grammar = grammar
        self.update()

    def destroy(self, *e):
        if self._root is None: return
        try: self._root.destroy()
        except: pass
        self._root = None

    def pack(self, *args, **kwargs):
        self._root.pack(*args, **kwargs)

#######################################################################
# Chart Comparer
#######################################################################

class ChartComparer(object):
    """

    :ivar _root: The root window

    :ivar _charts: A dictionary mapping names to charts.  When
        charts are loaded, they are added to this dictionary.

    :ivar _left_chart: The left ``Chart``.
    :ivar _left_name: The name ``_left_chart`` (derived from filename)
    :ivar _left_matrix: The ``ChartMatrixView`` for ``_left_chart``
    :ivar _left_selector: The drop-down ``MutableOptionsMenu`` used
          to select ``_left_chart``.

    :ivar _right_chart: The right ``Chart``.
    :ivar _right_name: The name ``_right_chart`` (derived from filename)
    :ivar _right_matrix: The ``ChartMatrixView`` for ``_right_chart``
    :ivar _right_selector: The drop-down ``MutableOptionsMenu`` used
          to select ``_right_chart``.

    :ivar _out_chart: The out ``Chart``.
    :ivar _out_name: The name ``_out_chart`` (derived from filename)
    :ivar _out_matrix: The ``ChartMatrixView`` for ``_out_chart``
    :ivar _out_label: The label for ``_out_chart``.

    :ivar _op_label: A Label containing the most recent operation.
    """

    _OPSYMBOL = {'-': '-',
                 'and': SymbolWidget.SYMBOLS['intersection'],
                 'or': SymbolWidget.SYMBOLS['union']}

    def __init__(self, *chart_filenames):
        # This chart is displayed when we don't have a value (eg
        # before any chart is loaded).
        faketok = [''] * 8
        self._emptychart = Chart(faketok)

        # The left & right charts start out empty.
        self._left_name = 'None'
        self._right_name = 'None'
        self._left_chart = self._emptychart
        self._right_chart = self._emptychart

        # The charts that have been loaded.
        self._charts = {'None': self._emptychart}

        # The output chart.
        self._out_chart = self._emptychart

        # The most recent operation
        self._operator = None

        # Set up the root window.
        self._root = tkinter.Tk()
        self._root.title('Chart Comparison')
        self._root.bind('<Control-q>', self.destroy)
        self._root.bind('<Control-x>', self.destroy)

        # Initialize all widgets, etc.
        self._init_menubar(self._root)
        self._init_chartviews(self._root)
        self._init_divider(self._root)
        self._init_buttons(self._root)
        self._init_bindings(self._root)

        # Load any specified charts.
        for filename in chart_filenames:
            self.load_chart(filename)

    def destroy(self, *e):
        if self._root is None: return
        try: self._root.destroy()
        except: pass
        self._root = None

    def mainloop(self, *args, **kwargs):
        return
        self._root.mainloop(*args, **kwargs)

    #////////////////////////////////////////////////////////////
    # Initialization
    #////////////////////////////////////////////////////////////

    def _init_menubar(self, root):
        menubar = tkinter.Menu(root)

        # File menu
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Load Chart', accelerator='Ctrl-o',
                             underline=0, command=self.load_chart_dialog)
        filemenu.add_command(label='Save Output', accelerator='Ctrl-s',
                             underline=0, command=self.save_chart_dialog)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', underline=1,
                             command=self.destroy, accelerator='Ctrl-x')
        menubar.add_cascade(label='File', underline=0, menu=filemenu)

        # Compare menu
        opmenu = tkinter.Menu(menubar, tearoff=0)
        opmenu.add_command(label='Intersection',
                           command=self._intersection,
                           accelerator='+')
        opmenu.add_command(label='Union',
                           command=self._union,
                           accelerator='*')
        opmenu.add_command(label='Difference',
                           command=self._difference,
                           accelerator='-')
        opmenu.add_separator()
        opmenu.add_command(label='Swap Charts',
                           command=self._swapcharts)
        menubar.add_cascade(label='Compare', underline=0, menu=opmenu)

        # Add the menu
        self._root.config(menu=menubar)

    def _init_divider(self, root):
        divider = tkinter.Frame(root, border=2, relief='sunken')
        divider.pack(side='top', fill='x', ipady=2)

    def _init_chartviews(self, root):
        opfont=('symbol', -36) # Font for operator.
        eqfont=('helvetica', -36) # Font for equals sign.

        frame = tkinter.Frame(root, background='#c0c0c0')
        frame.pack(side='top', expand=1, fill='both')

        # The left matrix.
        cv1_frame = tkinter.Frame(frame, border=3, relief='groove')
        cv1_frame.pack(side='left', padx=8, pady=7, expand=1, fill='both')
        self._left_selector = MutableOptionMenu(
            cv1_frame, list(self._charts.keys()), command=self._select_left)
        self._left_selector.pack(side='top', pady=5, fill='x')
        self._left_matrix = ChartMatrixView(cv1_frame, self._emptychart,
                                            toplevel=False,
                                            show_numedges=True)
        self._left_matrix.pack(side='bottom', padx=5, pady=5,
                               expand=1, fill='both')
        self._left_matrix.add_callback('select', self.select_edge)
        self._left_matrix.add_callback('select_cell', self.select_cell)
        self._left_matrix.inactivate()

        # The operator.
        self._op_label = tkinter.Label(frame, text=' ', width=3,
                                       background='#c0c0c0', font=opfont)
        self._op_label.pack(side='left', padx=5, pady=5)

        # The right matrix.
        cv2_frame = tkinter.Frame(frame, border=3, relief='groove')
        cv2_frame.pack(side='left', padx=8, pady=7, expand=1, fill='both')
        self._right_selector = MutableOptionMenu(
            cv2_frame, list(self._charts.keys()), command=self._select_right)
        self._right_selector.pack(side='top', pady=5, fill='x')
        self._right_matrix = ChartMatrixView(cv2_frame, self._emptychart,
                                            toplevel=False,
                                            show_numedges=True)
        self._right_matrix.pack(side='bottom', padx=5, pady=5,
                               expand=1, fill='both')
        self._right_matrix.add_callback('select', self.select_edge)
        self._right_matrix.add_callback('select_cell', self.select_cell)
        self._right_matrix.inactivate()

        # The equals sign
        tkinter.Label(frame, text='=', width=3, background='#c0c0c0',
                      font=eqfont).pack(side='left', padx=5, pady=5)

        # The output matrix.
        out_frame = tkinter.Frame(frame, border=3, relief='groove')
        out_frame.pack(side='left', padx=8, pady=7, expand=1, fill='both')
        self._out_label = tkinter.Label(out_frame, text='Output')
        self._out_label.pack(side='top', pady=9)
        self._out_matrix = ChartMatrixView(out_frame, self._emptychart,
                                            toplevel=False,
                                            show_numedges=True)
        self._out_matrix.pack(side='bottom', padx=5, pady=5,
                                 expand=1, fill='both')
        self._out_matrix.add_callback('select', self.select_edge)
        self._out_matrix.add_callback('select_cell', self.select_cell)
        self._out_matrix.inactivate()

    def _init_buttons(self, root):
        buttons = tkinter.Frame(root)
        buttons.pack(side='bottom', pady=5, fill='x', expand=0)
        tkinter.Button(buttons, text='Intersection',
                       command=self._intersection).pack(side='left')
        tkinter.Button(buttons, text='Union',
                       command=self._union).pack(side='left')
        tkinter.Button(buttons, text='Difference',
                       command=self._difference).pack(side='left')
        tkinter.Frame(buttons, width=20).pack(side='left')
        tkinter.Button(buttons, text='Swap Charts',
                       command=self._swapcharts).pack(side='left')

        tkinter.Button(buttons, text='Detatch Output',
                       command=self._detatch_out).pack(side='right')

    def _init_bindings(self, root):
        #root.bind('<Control-s>', self.save_chart)
        root.bind('<Control-o>', self.load_chart_dialog)
        #root.bind('<Control-r>', self.reset)

    #////////////////////////////////////////////////////////////
    # Input Handling
    #////////////////////////////////////////////////////////////

    def _select_left(self, name):
        self._left_name = name
        self._left_chart = self._charts[name]
        self._left_matrix.set_chart(self._left_chart)
        if name == 'None': self._left_matrix.inactivate()
        self._apply_op()

    def _select_right(self, name):
        self._right_name = name
        self._right_chart = self._charts[name]
        self._right_matrix.set_chart(self._right_chart)
        if name == 'None': self._right_matrix.inactivate()
        self._apply_op()

    def _apply_op(self):
        if self._operator == '-': self._difference()
        elif self._operator == 'or': self._union()
        elif self._operator == 'and': self._intersection()


    #////////////////////////////////////////////////////////////
    # File
    #////////////////////////////////////////////////////////////
    CHART_FILE_TYPES = [('Pickle file', '.pickle'),
                        ('All files', '*')]

    def save_chart_dialog(self, *args):
        filename = asksaveasfilename(filetypes=self.CHART_FILE_TYPES,
                                     defaultextension='.pickle')
        if not filename: return
        try:
            with open(filename, 'wb') as outfile:
                pickle.dump(self._out_chart, outfile)
        except Exception as e:
            tkinter.messagebox.showerror('Error Saving Chart',
                                   'Unable to open file: %r\n%s' %
                                   (filename, e))

    def load_chart_dialog(self, *args):
        filename = askopenfilename(filetypes=self.CHART_FILE_TYPES,
                                   defaultextension='.pickle')
        if not filename: return
        try: self.load_chart(filename)
        except Exception as e:
            tkinter.messagebox.showerror('Error Loading Chart',
                                   'Unable to open file: %r\n%s' %
                                   (filename, e))

    def load_chart(self, filename):
        with open(filename, 'rb') as infile:
            chart = pickle.load(infile)
        name = os.path.basename(filename)
        if name.endswith('.pickle'): name = name[:-7]
        if name.endswith('.chart'): name = name[:-6]
        self._charts[name] = chart
        self._left_selector.add(name)
        self._right_selector.add(name)

        # If either left_matrix or right_matrix is empty, then
        # display the new chart.
        if self._left_chart is self._emptychart:
            self._left_selector.set(name)
        elif self._right_chart is self._emptychart:
            self._right_selector.set(name)

    def _update_chartviews(self):
        self._left_matrix.update()
        self._right_matrix.update()
        self._out_matrix.update()

    #////////////////////////////////////////////////////////////
    # Selection
    #////////////////////////////////////////////////////////////

    def select_edge(self, edge):
        if edge in self._left_chart:
            self._left_matrix.markonly_edge(edge)
        else:
            self._left_matrix.unmark_edge()
        if edge in self._right_chart:
            self._right_matrix.markonly_edge(edge)
        else:
            self._right_matrix.unmark_edge()
        if edge in self._out_chart:
            self._out_matrix.markonly_edge(edge)
        else:
            self._out_matrix.unmark_edge()

    def select_cell(self, i, j):
        self._left_matrix.select_cell(i, j)
        self._right_matrix.select_cell(i, j)
        self._out_matrix.select_cell(i, j)

    #////////////////////////////////////////////////////////////
    # Operations
    #////////////////////////////////////////////////////////////

    def _difference(self):
        if not self._checkcompat(): return

        out_chart = Chart(self._left_chart.tokens())
        for edge in self._left_chart:
            if edge not in self._right_chart:
                out_chart.insert(edge, [])

        self._update('-', out_chart)

    def _intersection(self):
        if not self._checkcompat(): return

        out_chart = Chart(self._left_chart.tokens())
        for edge in self._left_chart:
            if edge in self._right_chart:
                out_chart.insert(edge, [])

        self._update('and', out_chart)

    def _union(self):
        if not self._checkcompat(): return

        out_chart = Chart(self._left_chart.tokens())
        for edge in self._left_chart:
            out_chart.insert(edge, [])
        for edge in self._right_chart:
            out_chart.insert(edge, [])

        self._update('or', out_chart)

    def _swapcharts(self):
        left, right = self._left_name, self._right_name
        self._left_selector.set(right)
        self._right_selector.set(left)

    def _checkcompat(self):
        if (self._left_chart.tokens() != self._right_chart.tokens() or
            self._left_chart.property_names() !=
            self._right_chart.property_names() or
            self._left_chart == self._emptychart or
            self._right_chart == self._emptychart):
            # Clear & inactivate the output chart.
            self._out_chart = self._emptychart
            self._out_matrix.set_chart(self._out_chart)
            self._out_matrix.inactivate()
            self._out_label['text'] = 'Output'
            # Issue some other warning?
            return False
        else:
            return True

    def _update(self, operator, out_chart):
        self._operator = operator
        self._op_label['text'] = self._OPSYMBOL[operator]
        self._out_chart = out_chart
        self._out_matrix.set_chart(out_chart)
        self._out_label['text'] = '%s %s %s' % (self._left_name,
                                                self._operator,
                                                self._right_name)

    def _clear_out_chart(self):
        self._out_chart = self._emptychart
        self._out_matrix.set_chart(self._out_chart)
        self._op_label['text'] = ' '
        self._out_matrix.inactivate()

    def _detatch_out(self):
        ChartMatrixView(self._root, self._out_chart,
                        title=self._out_label['text'])








#######################################################################
# Chart View
#######################################################################

class ChartView(object):
    """
    A component for viewing charts.  This is used by ``ChartParserApp`` to
    allow students to interactively experiment with various chart
    parsing techniques.  It is also used by ``Chart.draw()``.

    :ivar _chart: The chart that we are giving a view of.  This chart
       may be modified; after it is modified, you should call
       ``update``.
    :ivar _sentence: The list of tokens that the chart spans.

    :ivar _root: The root window.
    :ivar _chart_canvas: The canvas we're using to display the chart
        itself.
    :ivar _tree_canvas: The canvas we're using to display the tree
        that each edge spans.  May be None, if we're not displaying
        trees.
    :ivar _sentence_canvas: The canvas we're using to display the sentence
        text.  May be None, if we're not displaying the sentence text.
    :ivar _edgetags: A dictionary mapping from edges to the tags of
        the canvas elements (lines, etc) used to display that edge.
        The values of this dictionary have the form
        ``(linetag, rhstag1, dottag, rhstag2, lhstag)``.
    :ivar _treetags: A list of all the tags that make up the tree;
        used to erase the tree (without erasing the loclines).
    :ivar _chart_height: The height of the chart canvas.
    :ivar _sentence_height: The height of the sentence canvas.
    :ivar _tree_height: The height of the tree

    :ivar _text_height: The height of a text string (in the normal
        font).

    :ivar _edgelevels: A list of edges at each level of the chart (the
        top level is the 0th element).  This list is used to remember
        where edges should be drawn; and to make sure that no edges
        are overlapping on the chart view.

    :ivar _unitsize: Pixel size of one unit (from the location).  This
       is determined by the span of the chart's location, and the
       width of the chart display canvas.

    :ivar _fontsize: The current font size

    :ivar _marks: A dictionary from edges to marks.  Marks are
        strings, specifying colors (e.g. 'green').
    """

    _LEAF_SPACING = 10
    _MARGIN = 10
    _TREE_LEVEL_SIZE = 12
    _CHART_LEVEL_SIZE = 40

    def __init__(self, chart, root=None, **kw):
        """
        Construct a new ``Chart`` display.
        """
        # Process keyword args.
        draw_tree = kw.get('draw_tree', 0)
        draw_sentence = kw.get('draw_sentence', 1)
        self._fontsize = kw.get('fontsize', -12)

        # The chart!
        self._chart = chart

        # Callback functions
        self._callbacks = {}

        # Keep track of drawn edges
        self._edgelevels = []
        self._edgetags = {}

        # Keep track of which edges are marked.
        self._marks = {}

        # These are used to keep track of the set of tree tokens
        # currently displayed in the tree canvas.
        self._treetoks = []
        self._treetoks_edge = None
        self._treetoks_index = 0

        # Keep track of the tags used to draw the tree
        self._tree_tags = []

        # Put multiple edges on each level?
        self._compact = 0

        # If they didn't provide a main window, then set one up.
        if root is None:
            top = tkinter.Tk()
            top.title('Chart View')
            def destroy1(e, top=top): top.destroy()
            def destroy2(top=top): top.destroy()
            top.bind('q', destroy1)
            b = tkinter.Button(top, text='Done', command=destroy2)
            b.pack(side='bottom')
            self._root = top
        else:
            self._root = root

        # Create some fonts.
        self._init_fonts(root)

        # Create the chart canvas.
        (self._chart_sb, self._chart_canvas) = self._sb_canvas(self._root)
        self._chart_canvas['height'] = 300
        self._chart_canvas['closeenough'] = 15

        # Create the sentence canvas.
        if draw_sentence:
            cframe = tkinter.Frame(self._root, relief='sunk', border=2)
            cframe.pack(fill='both', side='bottom')
            self._sentence_canvas = tkinter.Canvas(cframe, height=50)
            self._sentence_canvas['background'] = '#e0e0e0'
            self._sentence_canvas.pack(fill='both')
            #self._sentence_canvas['height'] = self._sentence_height
        else:
            self._sentence_canvas = None

        # Create the tree canvas.
        if draw_tree:
            (sb, canvas) = self._sb_canvas(self._root, 'n', 'x')
            (self._tree_sb, self._tree_canvas) = (sb, canvas)
            self._tree_canvas['height'] = 200
        else:
            self._tree_canvas = None

        # Do some analysis to figure out how big the window should be
        self._analyze()
        self.draw()
        self._resize()
        self._grow()

        # Set up the configure callback, which will be called whenever
        # the window is resized.
        self._chart_canvas.bind('<Configure>', self._configure)

    def _init_fonts(self, root):
        self._boldfont = tkinter.font.Font(family='helvetica', weight='bold',
                                    size=self._fontsize)
        self._font = tkinter.font.Font(family='helvetica',
                                    size=self._fontsize)
        # See: <http://www.astro.washington.edu/owen/ROTKFolklore.html>
        self._sysfont = tkinter.font.Font(font=tkinter.Button()["font"])
        root.option_add("*Font", self._sysfont)

    def _sb_canvas(self, root, expand='y',
                   fill='both', side='bottom'):
        """
        Helper for __init__: construct a canvas with a scrollbar.
        """
        cframe =tkinter.Frame(root, relief='sunk', border=2)
        cframe.pack(fill=fill, expand=expand, side=side)
        canvas = tkinter.Canvas(cframe, background='#e0e0e0')

        # Give the canvas a scrollbar.
        sb = tkinter.Scrollbar(cframe, orient='vertical')
        sb.pack(side='right', fill='y')
        canvas.pack(side='left', fill=fill, expand='yes')

        # Connect the scrollbars to the canvas.
        sb['command']= canvas.yview
        canvas['yscrollcommand'] = sb.set

        return (sb, canvas)

    def scroll_up(self, *e):
        self._chart_canvas.yview('scroll', -1, 'units')

    def scroll_down(self, *e):
        self._chart_canvas.yview('scroll', 1, 'units')

    def page_up(self, *e):
        self._chart_canvas.yview('scroll', -1, 'pages')

    def page_down(self, *e):
        self._chart_canvas.yview('scroll', 1, 'pages')

    def _grow(self):
        """
        Grow the window, if necessary
        """
        # Grow, if need-be
        N = self._chart.num_leaves()
        width = max(int(self._chart_canvas['width']),
                    N * self._unitsize + ChartView._MARGIN * 2 )

        # It won't resize without the second (height) line, but I
        # don't understand why not.
        self._chart_canvas.configure(width=width)
        self._chart_canvas.configure(height=self._chart_canvas['height'])

        self._unitsize = (width - 2*ChartView._MARGIN) / N

        # Reset the height for the sentence window.
        if self._sentence_canvas is not None:
            self._sentence_canvas['height'] = self._sentence_height

    def set_font_size(self, size):
        self._font.configure(size=-abs(size))
        self._boldfont.configure(size=-abs(size))
        self._sysfont.configure(size=-abs(size))
        self._analyze()
        self._grow()
        self.draw()

    def get_font_size(self):
        return abs(self._fontsize)

    def _configure(self, e):
        """
        The configure callback.  This is called whenever the window is
        resized.  It is also called when the window is first mapped.
        It figures out the unit size, and redraws the contents of each
        canvas.
        """
        N = self._chart.num_leaves()
        self._unitsize = (e.width - 2*ChartView._MARGIN) / N
        self.draw()

    def update(self, chart=None):
        """
        Draw any edges that have not been drawn.  This is typically
        called when a after modifies the canvas that a CanvasView is
        displaying.  ``update`` will cause any edges that have been
        added to the chart to be drawn.

        If update is given a ``chart`` argument, then it will replace
        the current chart with the given chart.
        """
        if chart is not None:
            self._chart = chart
            self._edgelevels = []
            self._marks = {}
            self._analyze()
            self._grow()
            self.draw()
            self.erase_tree()
            self._resize()
        else:
            for edge in self._chart:
                if edge not in self._edgetags:
                    self._add_edge(edge)
            self._resize()


    def _edge_conflict(self, edge, lvl):
        """
        Return True if the given edge overlaps with any edge on the given
        level.  This is used by _add_edge to figure out what level a
        new edge should be added to.
        """
        (s1, e1) = edge.span()
        for otheredge in self._edgelevels[lvl]:
            (s2, e2) = otheredge.span()
            if (s1 <= s2 < e1) or (s2 <= s1 < e2) or (s1==s2==e1==e2):
                return True
        return False

    def _analyze_edge(self, edge):
        """
        Given a new edge, recalculate:

            - _text_height
            - _unitsize (if the edge text is too big for the current
              _unitsize, then increase _unitsize)
        """
        c = self._chart_canvas

        if isinstance(edge, TreeEdge):
            lhs = edge.lhs()
            rhselts = []
            for elt in edge.rhs():
                if isinstance(elt, Nonterminal):
                    rhselts.append(str(elt.symbol()))
                else:
                    rhselts.append(repr(elt))
            rhs = " ".join(rhselts)
        else:
            lhs = edge.lhs()
            rhs = ''

        for s in (lhs, rhs):
            tag = c.create_text(0,0, text=s,
                                font=self._boldfont,
                                anchor='nw', justify='left')
            bbox = c.bbox(tag)
            c.delete(tag)
            width = bbox[2] #+ ChartView._LEAF_SPACING
            edgelen = max(edge.length(), 1)
            self._unitsize = max(self._unitsize, width/edgelen)
            self._text_height = max(self._text_height, bbox[3] - bbox[1])

    def _add_edge(self, edge, minlvl=0):
        """
        Add a single edge to the ChartView:

            - Call analyze_edge to recalculate display parameters
            - Find an available level
            - Call _draw_edge
        """
        # Do NOT show leaf edges in the chart.
        if isinstance(edge, LeafEdge): return

        if edge in self._edgetags: return
        self._analyze_edge(edge)
        self._grow()

        if not self._compact:
            self._edgelevels.append([edge])
            lvl = len(self._edgelevels)-1
            self._draw_edge(edge, lvl)
            self._resize()
            return

        # Figure out what level to draw the edge on.
        lvl = 0
        while True:
            # If this level doesn't exist yet, create it.
            while lvl >= len(self._edgelevels):
                self._edgelevels.append([])
                self._resize()

            # Check if we can fit the edge in this level.
            if lvl>=minlvl and not self._edge_conflict(edge, lvl):
                # Go ahead and draw it.
                self._edgelevels[lvl].append(edge)
                break

            # Try the next level.
            lvl += 1

        self._draw_edge(edge, lvl)

    def view_edge(self, edge):
        level = None
        for i in range(len(self._edgelevels)):
            if edge in self._edgelevels[i]:
                level = i
                break
        if level is None: return
        # Try to view the new edge..
        y = (level+1) * self._chart_level_size
        dy = self._text_height + 10
        self._chart_canvas.yview('moveto', 1.0)
        if self._chart_height != 0:
            self._chart_canvas.yview('moveto',
                                     float(y-dy)/self._chart_height)

    def _draw_edge(self, edge, lvl):
        """
        Draw a single edge on the ChartView.
        """
        c = self._chart_canvas

        # Draw the arrow.
        x1 = (edge.start() * self._unitsize + ChartView._MARGIN)
        x2 = (edge.end() * self._unitsize + ChartView._MARGIN)
        if x2 == x1: x2 += max(4, self._unitsize/5)
        y = (lvl+1) * self._chart_level_size
        linetag = c.create_line(x1, y, x2, y, arrow='last', width=3)

        # Draw a label for the edge.
        if isinstance(edge, TreeEdge):
            rhs = []
            for elt in edge.rhs():
                if isinstance(elt, Nonterminal):
                    rhs.append(str(elt.symbol()))
                else:
                    rhs.append(repr(elt))
            pos = edge.dot()
        else:
            rhs = []
            pos = 0

        rhs1 = " ".join(rhs[:pos])
        rhs2 = " ".join(rhs[pos:])
        rhstag1 = c.create_text(x1+3, y, text=rhs1,
                                font=self._font,
                                anchor='nw')
        dotx = c.bbox(rhstag1)[2] + 6
        doty = (c.bbox(rhstag1)[1]+c.bbox(rhstag1)[3])/2
        dottag = c.create_oval(dotx-2, doty-2, dotx+2, doty+2)
        rhstag2 = c.create_text(dotx+6, y, text=rhs2,
                                font=self._font,
                                anchor='nw')
        lhstag =  c.create_text((x1+x2)/2, y, text=str(edge.lhs()),
                                anchor='s',
                                font=self._boldfont)

        # Keep track of the edge's tags.
        self._edgetags[edge] = (linetag, rhstag1,
                                dottag, rhstag2, lhstag)

        # Register a callback for clicking on the edge.
        def cb(event, self=self, edge=edge):
            self._fire_callbacks('select', edge)
        c.tag_bind(rhstag1, '<Button-1>', cb)
        c.tag_bind(rhstag2, '<Button-1>', cb)
        c.tag_bind(linetag, '<Button-1>', cb)
        c.tag_bind(dottag, '<Button-1>', cb)
        c.tag_bind(lhstag, '<Button-1>', cb)

        self._color_edge(edge)

    def _color_edge(self, edge, linecolor=None, textcolor=None):
        """
        Color in an edge with the given colors.
        If no colors are specified, use intelligent defaults
        (dependent on selection, etc.)
        """
        if edge not in self._edgetags: return
        c = self._chart_canvas

        if linecolor is not None and textcolor is not None:
            if edge in self._marks:
                linecolor = self._marks[edge]
            tags = self._edgetags[edge]
            c.itemconfig(tags[0], fill=linecolor)
            c.itemconfig(tags[1], fill=textcolor)
            c.itemconfig(tags[2], fill=textcolor,
                         outline=textcolor)
            c.itemconfig(tags[3], fill=textcolor)
            c.itemconfig(tags[4], fill=textcolor)
            return
        else:
            N = self._chart.num_leaves()
            if edge in self._marks:
                self._color_edge(self._marks[edge])
            if (edge.is_complete() and edge.span() == (0, N)):
                self._color_edge(edge, '#084', '#042')
            elif isinstance(edge, LeafEdge):
                self._color_edge(edge, '#48c', '#246')
            else:
                self._color_edge(edge, '#00f', '#008')

    def mark_edge(self, edge, mark='#0df'):
        """
        Mark an edge
        """
        self._marks[edge] = mark
        self._color_edge(edge)

    def unmark_edge(self, edge=None):
        """
        Unmark an edge (or all edges)
        """
        if edge is None:
            old_marked_edges = list(self._marks.keys())
            self._marks = {}
            for edge in old_marked_edges:
                self._color_edge(edge)
        else:
            del self._marks[edge]
            self._color_edge(edge)

    def markonly_edge(self, edge, mark='#0df'):
        self.unmark_edge()
        self.mark_edge(edge, mark)

    def _analyze(self):
        """
        Analyze the sentence string, to figure out how big a unit needs
        to be, How big the tree should be, etc.
        """
        # Figure out the text height and the unit size.
        unitsize = 70 # min unitsize
        text_height = 0
        c = self._chart_canvas

        # Check against all tokens
        for leaf in self._chart.leaves():
            tag = c.create_text(0,0, text=repr(leaf),
                                font=self._font,
                                anchor='nw', justify='left')
            bbox = c.bbox(tag)
            c.delete(tag)
            width = bbox[2] + ChartView._LEAF_SPACING
            unitsize = max(width, unitsize)
            text_height = max(text_height, bbox[3] - bbox[1])

        self._unitsize = unitsize
        self._text_height = text_height
        self._sentence_height = (self._text_height +
                               2*ChartView._MARGIN)

        # Check against edges.
        for edge in self._chart.edges():
            self._analyze_edge(edge)

        # Size of chart levels
        self._chart_level_size = self._text_height * 2

        # Default tree size..
        self._tree_height = (3 * (ChartView._TREE_LEVEL_SIZE +
                                  self._text_height))

        # Resize the scrollregions.
        self._resize()

    def _resize(self):
        """
        Update the scroll-regions for each canvas.  This ensures that
        everything is within a scroll-region, so the user can use the
        scrollbars to view the entire display.  This does *not*
        resize the window.
        """
        c = self._chart_canvas

        # Reset the chart scroll region
        width = ( self._chart.num_leaves() * self._unitsize +
                  ChartView._MARGIN * 2 )

        levels = len(self._edgelevels)
        self._chart_height = (levels+2)*self._chart_level_size
        c['scrollregion']=(0,0,width,self._chart_height)

        # Reset the tree scroll region
        if self._tree_canvas:
            self._tree_canvas['scrollregion'] = (0, 0, width,
                                                 self._tree_height)

    def _draw_loclines(self):
        """
        Draw location lines.  These are vertical gridlines used to
        show where each location unit is.
        """
        BOTTOM = 50000
        c1 = self._tree_canvas
        c2 = self._sentence_canvas
        c3 = self._chart_canvas
        margin = ChartView._MARGIN
        self._loclines = []
        for i in range(0, self._chart.num_leaves()+1):
            x = i*self._unitsize + margin

            if c1:
                t1=c1.create_line(x, 0, x, BOTTOM)
                c1.tag_lower(t1)
            if c2:
                t2=c2.create_line(x, 0, x, self._sentence_height)
                c2.tag_lower(t2)
            t3=c3.create_line(x, 0, x, BOTTOM)
            c3.tag_lower(t3)
            t4=c3.create_text(x+2, 0, text=repr(i), anchor='nw',
                              font=self._font)
            c3.tag_lower(t4)
            #if i % 4 == 0:
            #    if c1: c1.itemconfig(t1, width=2, fill='gray60')
            #    if c2: c2.itemconfig(t2, width=2, fill='gray60')
            #    c3.itemconfig(t3, width=2, fill='gray60')
            if i % 2 == 0:
                if c1: c1.itemconfig(t1, fill='gray60')
                if c2: c2.itemconfig(t2, fill='gray60')
                c3.itemconfig(t3, fill='gray60')
            else:
                if c1: c1.itemconfig(t1, fill='gray80')
                if c2: c2.itemconfig(t2, fill='gray80')
                c3.itemconfig(t3, fill='gray80')

    def _draw_sentence(self):
        """Draw the sentence string."""
        if self._chart.num_leaves() == 0: return
        c = self._sentence_canvas
        margin = ChartView._MARGIN
        y = ChartView._MARGIN

        for i, leaf in enumerate(self._chart.leaves()):
            x1 = i * self._unitsize + margin
            x2 = x1 + self._unitsize
            x = (x1+x2)/2
            tag = c.create_text(x, y, text=repr(leaf),
                                font=self._font,
                                anchor='n', justify='left')
            bbox = c.bbox(tag)
            rt=c.create_rectangle(x1+2, bbox[1]-(ChartView._LEAF_SPACING/2),
                                  x2-2, bbox[3]+(ChartView._LEAF_SPACING/2),
                                  fill='#f0f0f0', outline='#f0f0f0')
            c.tag_lower(rt)

    def erase_tree(self):
        for tag in self._tree_tags: self._tree_canvas.delete(tag)
        self._treetoks = []
        self._treetoks_edge = None
        self._treetoks_index = 0

    def draw_tree(self, edge=None):
        if edge is None and self._treetoks_edge is None: return
        if edge is None: edge = self._treetoks_edge

        # If it's a new edge, then get a new list of treetoks.
        if self._treetoks_edge != edge:
            self._treetoks = [t for t in self._chart.trees(edge)
                              if isinstance(t, Tree)]
            self._treetoks_edge = edge
            self._treetoks_index = 0

        # Make sure there's something to draw.
        if len(self._treetoks) == 0: return

        # Erase the old tree.
        for tag in self._tree_tags: self._tree_canvas.delete(tag)

        # Draw the new tree.
        tree = self._treetoks[self._treetoks_index]
        self._draw_treetok(tree, edge.start())

        # Show how many trees are available for the edge.
        self._draw_treecycle()

        # Update the scroll region.
        w = self._chart.num_leaves()*self._unitsize+2*ChartView._MARGIN
        h = tree.height() * (ChartView._TREE_LEVEL_SIZE+self._text_height)
        self._tree_canvas['scrollregion'] = (0, 0, w, h)

    def cycle_tree(self):
        self._treetoks_index = (self._treetoks_index+1)%len(self._treetoks)
        self.draw_tree(self._treetoks_edge)

    def _draw_treecycle(self):
        if len(self._treetoks) <= 1: return

        # Draw the label.
        label = '%d Trees' % len(self._treetoks)
        c = self._tree_canvas
        margin = ChartView._MARGIN
        right = self._chart.num_leaves()*self._unitsize+margin-2
        tag = c.create_text(right, 2, anchor='ne', text=label,
                            font=self._boldfont)
        self._tree_tags.append(tag)
        _, _, _, y = c.bbox(tag)

        # Draw the triangles.
        for i in range(len(self._treetoks)):
            x = right - 20*(len(self._treetoks)-i-1)
            if i == self._treetoks_index: fill = '#084'
            else: fill = '#fff'
            tag = c.create_polygon(x, y+10, x-5, y, x-10, y+10,
                             fill=fill, outline='black')
            self._tree_tags.append(tag)

            # Set up a callback: show the tree if they click on its
            # triangle.
            def cb(event, self=self, i=i):
                self._treetoks_index = i
                self.draw_tree()
            c.tag_bind(tag, '<Button-1>', cb)

    def _draw_treetok(self, treetok, index, depth=0):
        """
        :param index: The index of the first leaf in the tree.
        :return: The index of the first leaf after the tree.
        """
        c = self._tree_canvas
        margin = ChartView._MARGIN

        # Draw the children
        child_xs = []
        for child in treetok:
            if isinstance(child, Tree):
                child_x, index = self._draw_treetok(child, index, depth+1)
                child_xs.append(child_x)
            else:
                child_xs.append((2*index+1)*self._unitsize/2 + margin)
                index += 1

        # If we have children, then get the node's x by averaging their
        # node x's.  Otherwise, make room for ourselves.
        if child_xs:
            nodex = sum(child_xs)/len(child_xs)
        else:
            # [XX] breaks for null productions.
            nodex = (2*index+1)*self._unitsize/2 + margin
            index += 1

        # Draw the node
        nodey = depth * (ChartView._TREE_LEVEL_SIZE + self._text_height)
        tag = c.create_text(nodex, nodey, anchor='n', justify='center',
                            text=str(treetok.label()), fill='#042',
                            font=self._boldfont)
        self._tree_tags.append(tag)

        # Draw lines to the children.
        childy = nodey + ChartView._TREE_LEVEL_SIZE + self._text_height
        for childx, child in zip(child_xs, treetok):
            if isinstance(child, Tree) and child:
                # A "real" tree token:
                tag = c.create_line(nodex, nodey + self._text_height,
                                    childx, childy, width=2, fill='#084')
                self._tree_tags.append(tag)
            if isinstance(child, Tree) and not child:
                # An unexpanded tree token:
                tag = c.create_line(nodex, nodey + self._text_height,
                                    childx, childy, width=2,
                                    fill='#048', dash='2 3')
                self._tree_tags.append(tag)
            if not isinstance(child, Tree):
                # A leaf:
                tag = c.create_line(nodex, nodey + self._text_height,
                                    childx, 10000, width=2, fill='#084')
                self._tree_tags.append(tag)

        return nodex, index

    def draw(self):
        """
        Draw everything (from scratch).
        """
        if self._tree_canvas:
            self._tree_canvas.delete('all')
            self.draw_tree()

        if self._sentence_canvas:
            self._sentence_canvas.delete('all')
            self._draw_sentence()

        self._chart_canvas.delete('all')
        self._edgetags = {}

        # Redraw any edges we erased.
        for lvl in range(len(self._edgelevels)):
            for edge in self._edgelevels[lvl]:
                self._draw_edge(edge, lvl)

        for edge in self._chart:
            self._add_edge(edge)

        self._draw_loclines()

    def add_callback(self, event, func):
        self._callbacks.setdefault(event,{})[func] = 1

    def remove_callback(self, event, func=None):
        if func is None: del self._callbacks[event]
        else:
            try: del self._callbacks[event][func]
            except: pass

    def _fire_callbacks(self, event, *args):
        if event not in self._callbacks: return
        for cb_func in list(self._callbacks[event].keys()): cb_func(*args)

#######################################################################
# Edge Rules
#######################################################################
# These version of the chart rules only apply to a specific edge.
# This lets the user select an edge, and then apply a rule.

class EdgeRule(object):
    """
    To create an edge rule, make an empty base class that uses
    EdgeRule as the first base class, and the basic rule as the
    second base class.  (Order matters!)
    """
    def __init__(self, edge):
        super = self.__class__.__bases__[1]
        self._edge = edge
        self.NUM_EDGES = super.NUM_EDGES-1
    def apply(self, chart, grammar, *edges):
        super = self.__class__.__bases__[1]
        edges += (self._edge,)
        for e in super.apply(self, chart, grammar, *edges): yield e
    def __str__(self):
        super = self.__class__.__bases__[1]
        return super.__str__(self)

class TopDownPredictEdgeRule(EdgeRule, TopDownPredictRule):
    pass
class BottomUpEdgeRule(EdgeRule, BottomUpPredictRule):
    pass
class BottomUpLeftCornerEdgeRule(EdgeRule, BottomUpPredictCombineRule):
    pass
class FundamentalEdgeRule(EdgeRule, SingleEdgeFundamentalRule):
    pass

#######################################################################
# Chart Parser Application
#######################################################################

class ChartParserApp(object):
    def __init__(self, grammar, tokens, title='Chart Parser Application'):
        # Initialize the parser
        self._init_parser(grammar, tokens)

        self._root = None
        try:
            # Create the root window.
            self._root = tkinter.Tk()
            self._root.title(title)
            self._root.bind('<Control-q>', self.destroy)

            # Set up some frames.
            frame3 = tkinter.Frame(self._root)
            frame2 = tkinter.Frame(self._root)
            frame1 = tkinter.Frame(self._root)
            frame3.pack(side='bottom', fill='none')
            frame2.pack(side='bottom', fill='x')
            frame1.pack(side='bottom', fill='both', expand=1)

            self._init_fonts(self._root)
            self._init_animation()
            self._init_chartview(frame1)
            self._init_rulelabel(frame2)
            self._init_buttons(frame3)
            self._init_menubar()

            self._matrix = None
            self._results = None

            # Set up keyboard bindings.
            self._init_bindings()

        except:
            print('Error creating Tree View')
            self.destroy()
            raise

    def destroy(self, *args):
        if self._root is None: return
        self._root.destroy()
        self._root = None

    def mainloop(self, *args, **kwargs):
        """
        Enter the Tkinter mainloop.  This function must be called if
        this demo is created from a non-interactive program (e.g.
        from a secript); otherwise, the demo will close as soon as
        the script completes.
        """
        if in_idle(): return
        self._root.mainloop(*args, **kwargs)

    #////////////////////////////////////////////////////////////
    # Initialization Helpers
    #////////////////////////////////////////////////////////////

    def _init_parser(self, grammar, tokens):
        self._grammar = grammar
        self._tokens = tokens
        self._reset_parser()

    def _reset_parser(self):
        self._cp = SteppingChartParser(self._grammar)
        self._cp.initialize(self._tokens)
        self._chart = self._cp.chart()

        # Insert LeafEdges before the parsing starts.
        for _new_edge in LeafInitRule().apply(self._chart, self._grammar):
            pass

        # The step iterator -- use this to generate new edges
        self._cpstep = self._cp.step()

        # The currently selected edge
        self._selection = None

    def _init_fonts(self, root):
        # See: <http://www.astro.washington.edu/owen/ROTKFolklore.html>
        self._sysfont = tkinter.font.Font(font=tkinter.Button()["font"])
        root.option_add("*Font", self._sysfont)

        # TWhat's our font size (default=same as sysfont)
        self._size = tkinter.IntVar(root)
        self._size.set(self._sysfont.cget('size'))

        self._boldfont = tkinter.font.Font(family='helvetica', weight='bold',
                                    size=self._size.get())
        self._font = tkinter.font.Font(family='helvetica',
                                    size=self._size.get())

    def _init_animation(self):
        # Are we stepping? (default=yes)
        self._step = tkinter.IntVar(self._root)
        self._step.set(1)

        # What's our animation speed (default=fast)
        self._animate = tkinter.IntVar(self._root)
        self._animate.set(3) # Default speed = fast

        # Are we currently animating?
        self._animating = 0

    def _init_chartview(self, parent):
        self._cv = ChartView(self._chart, parent,
                             draw_tree=1, draw_sentence=1)
        self._cv.add_callback('select', self._click_cv_edge)

    def _init_rulelabel(self, parent):
        ruletxt = 'Last edge generated by:'

        self._rulelabel1 = tkinter.Label(parent,text=ruletxt,
                                         font=self._boldfont)
        self._rulelabel2 = tkinter.Label(parent, width=40,
                                         relief='groove', anchor='w',
                                         font=self._boldfont)
        self._rulelabel1.pack(side='left')
        self._rulelabel2.pack(side='left')
        step = tkinter.Checkbutton(parent, variable=self._step,
                                   text='Step')
        step.pack(side='right')

    def _init_buttons(self, parent):
        frame1 = tkinter.Frame(parent)
        frame2 = tkinter.Frame(parent)
        frame1.pack(side='bottom', fill='x')
        frame2.pack(side='top', fill='none')

        tkinter.Button(frame1, text='Reset\nParser',
                       background='#90c0d0', foreground='black',
                       command=self.reset).pack(side='right')
        #Tkinter.Button(frame1, text='Pause',
        #               background='#90c0d0', foreground='black',
        #               command=self.pause).pack(side='left')

        tkinter.Button(frame1, text='Top Down\nStrategy',
                       background='#90c0d0', foreground='black',
                       command=self.top_down_strategy).pack(side='left')
        tkinter.Button(frame1, text='Bottom Up\nStrategy',
                       background='#90c0d0', foreground='black',
                       command=self.bottom_up_strategy).pack(side='left')
        tkinter.Button(frame1, text='Bottom Up\nLeft-Corner Strategy',
                       background='#90c0d0', foreground='black',
                       command=self.bottom_up_leftcorner_strategy).pack(side='left')

        tkinter.Button(frame2, text='Top Down Init\nRule',
                       background='#90f090', foreground='black',
                       command=self.top_down_init).pack(side='left')
        tkinter.Button(frame2, text='Top Down Predict\nRule',
                       background='#90f090', foreground='black',
                       command=self.top_down_predict).pack(side='left')
        tkinter.Frame(frame2, width=20).pack(side='left')

        tkinter.Button(frame2, text='Bottom Up Predict\nRule',
                       background='#90f090', foreground='black',
                       command=self.bottom_up).pack(side='left')
        tkinter.Frame(frame2, width=20).pack(side='left')

        tkinter.Button(frame2, text='Bottom Up Left-Corner\nPredict Rule',
                       background='#90f090', foreground='black',
                       command=self.bottom_up_leftcorner).pack(side='left')
        tkinter.Frame(frame2, width=20).pack(side='left')

        tkinter.Button(frame2, text='Fundamental\nRule',
                       background='#90f090', foreground='black',
                       command=self.fundamental).pack(side='left')

    def _init_bindings(self):
        self._root.bind('<Up>', self._cv.scroll_up)
        self._root.bind('<Down>', self._cv.scroll_down)
        self._root.bind('<Prior>', self._cv.page_up)
        self._root.bind('<Next>', self._cv.page_down)
        self._root.bind('<Control-q>', self.destroy)
        self._root.bind('<Control-x>', self.destroy)
        self._root.bind('<F1>', self.help)

        self._root.bind('<Control-s>', self.save_chart)
        self._root.bind('<Control-o>', self.load_chart)
        self._root.bind('<Control-r>', self.reset)

        self._root.bind('t', self.top_down_strategy)
        self._root.bind('b', self.bottom_up_strategy)
        self._root.bind('c', self.bottom_up_leftcorner_strategy)
        self._root.bind('<space>', self._stop_animation)

        self._root.bind('<Control-g>', self.edit_grammar)
        self._root.bind('<Control-t>', self.edit_sentence)

        # Animation speed control
        self._root.bind('-', lambda e,a=self._animate:a.set(1))
        self._root.bind('=', lambda e,a=self._animate:a.set(2))
        self._root.bind('+', lambda e,a=self._animate:a.set(3))

        # Step control
        self._root.bind('s', lambda e,s=self._step:s.set(not s.get()))

    def _init_menubar(self):
        menubar = tkinter.Menu(self._root)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save Chart', underline=0,
                             command=self.save_chart, accelerator='Ctrl-s')
        filemenu.add_command(label='Load Chart', underline=0,
                             command=self.load_chart, accelerator='Ctrl-o')
        filemenu.add_command(label='Reset Chart', underline=0,
                             command=self.reset, accelerator='Ctrl-r')
        filemenu.add_separator()
        filemenu.add_command(label='Save Grammar',
                             command=self.save_grammar)
        filemenu.add_command(label='Load Grammar',
                             command=self.load_grammar)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', underline=1,
                             command=self.destroy, accelerator='Ctrl-x')
        menubar.add_cascade(label='File', underline=0, menu=filemenu)

        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label='Edit Grammar', underline=5,
                             command=self.edit_grammar,
                             accelerator='Ctrl-g')
        editmenu.add_command(label='Edit Text', underline=5,
                             command=self.edit_sentence,
                             accelerator='Ctrl-t')
        menubar.add_cascade(label='Edit', underline=0, menu=editmenu)

        viewmenu = tkinter.Menu(menubar, tearoff=0)
        viewmenu.add_command(label='Chart Matrix', underline=6,
                             command=self.view_matrix)
        viewmenu.add_command(label='Results', underline=0,
                             command=self.view_results)
        menubar.add_cascade(label='View', underline=0, menu=viewmenu)

        rulemenu = tkinter.Menu(menubar, tearoff=0)
        rulemenu.add_command(label='Top Down Strategy', underline=0,
                             command=self.top_down_strategy,
                             accelerator='t')
        rulemenu.add_command(label='Bottom Up Strategy', underline=0,
                             command=self.bottom_up_strategy,
                             accelerator='b')
        rulemenu.add_command(label='Bottom Up Left-Corner Strategy', underline=0,
                             command=self.bottom_up_leftcorner_strategy,
                             accelerator='c')
        rulemenu.add_separator()
        rulemenu.add_command(label='Bottom Up Rule',
                             command=self.bottom_up)
        rulemenu.add_command(label='Bottom Up Left-Corner Rule',
                             command=self.bottom_up_leftcorner)
        rulemenu.add_command(label='Top Down Init Rule',
                             command=self.top_down_init)
        rulemenu.add_command(label='Top Down Predict Rule',
                             command=self.top_down_predict)
        rulemenu.add_command(label='Fundamental Rule',
                             command=self.fundamental)
        menubar.add_cascade(label='Apply', underline=0, menu=rulemenu)

        animatemenu = tkinter.Menu(menubar, tearoff=0)
        animatemenu.add_checkbutton(label="Step", underline=0,
                                    variable=self._step,
                                    accelerator='s')
        animatemenu.add_separator()
        animatemenu.add_radiobutton(label="No Animation", underline=0,
                                    variable=self._animate, value=0)
        animatemenu.add_radiobutton(label="Slow Animation", underline=0,
                                    variable=self._animate, value=1,
                                    accelerator='-')
        animatemenu.add_radiobutton(label="Normal Animation", underline=0,
                                    variable=self._animate, value=2,
                                    accelerator='=')
        animatemenu.add_radiobutton(label="Fast Animation", underline=0,
                                    variable=self._animate, value=3,
                                    accelerator='+')
        menubar.add_cascade(label="Animate", underline=1, menu=animatemenu)

        zoommenu = tkinter.Menu(menubar, tearoff=0)
        zoommenu.add_radiobutton(label='Tiny', variable=self._size,
                                 underline=0, value=10, command=self.resize)
        zoommenu.add_radiobutton(label='Small', variable=self._size,
                                 underline=0, value=12, command=self.resize)
        zoommenu.add_radiobutton(label='Medium', variable=self._size,
                                 underline=0, value=14, command=self.resize)
        zoommenu.add_radiobutton(label='Large', variable=self._size,
                                 underline=0, value=18, command=self.resize)
        zoommenu.add_radiobutton(label='Huge', variable=self._size,
                                 underline=0, value=24, command=self.resize)
        menubar.add_cascade(label='Zoom', underline=0, menu=zoommenu)

        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='About', underline=0,
                             command=self.about)
        helpmenu.add_command(label='Instructions', underline=0,
                             command=self.help, accelerator='F1')
        menubar.add_cascade(label='Help', underline=0, menu=helpmenu)

        self._root.config(menu=menubar)

    #////////////////////////////////////////////////////////////
    # Selection Handling
    #////////////////////////////////////////////////////////////

    def _click_cv_edge(self, edge):
        if edge != self._selection:
            # Clicking on a new edge selects it.
            self._select_edge(edge)
        else:
            # Repeated clicks on one edge cycle its trees.
            self._cv.cycle_tree()
            # [XX] this can get confused if animation is running
            # faster than the callbacks...

    def _select_matrix_edge(self, edge):
        self._select_edge(edge)
        self._cv.view_edge(edge)

    def _select_edge(self, edge):
        self._selection = edge
        # Update the chart view.
        self._cv.markonly_edge(edge, '#f00')
        self._cv.draw_tree(edge)
        # Update the matrix view.
        if self._matrix: self._matrix.markonly_edge(edge)
        if self._matrix: self._matrix.view_edge(edge)

    def _deselect_edge(self):
        self._selection = None
        # Update the chart view.
        self._cv.unmark_edge()
        self._cv.erase_tree()
        # Update the matrix view
        if self._matrix: self._matrix.unmark_edge()

    def _show_new_edge(self, edge):
        self._display_rule(self._cp.current_chartrule())
        # Update the chart view.
        self._cv.update()
        self._cv.draw_tree(edge)
        self._cv.markonly_edge(edge, '#0df')
        self._cv.view_edge(edge)
        # Update the matrix view.
        if self._matrix: self._matrix.update()
        if self._matrix: self._matrix.markonly_edge(edge)
        if self._matrix: self._matrix.view_edge(edge)
        # Update the results view.
        if self._results: self._results.update(edge)

    #////////////////////////////////////////////////////////////
    # Help/usage
    #////////////////////////////////////////////////////////////

    def help(self, *e):
        self._animating = 0
        # The default font's not very legible; try using 'fixed' instead.
        try:
            ShowText(self._root, 'Help: Chart Parser Application',
                     (__doc__ or '').strip(), width=75, font='fixed')
        except:
            ShowText(self._root, 'Help: Chart Parser Application',
                     (__doc__ or '').strip(), width=75)

    def about(self, *e):
        ABOUT = ("NLTK Chart Parser Application\n"+
                 "Written by Edward Loper")
        tkinter.messagebox.showinfo('About: Chart Parser Application', ABOUT)

    #////////////////////////////////////////////////////////////
    # File Menu
    #////////////////////////////////////////////////////////////

    CHART_FILE_TYPES = [('Pickle file', '.pickle'),
                        ('All files', '*')]
    GRAMMAR_FILE_TYPES = [('Plaintext grammar file', '.cfg'),
                          ('Pickle file', '.pickle'),
                          ('All files', '*')]

    def load_chart(self, *args):
        "Load a chart from a pickle file"
        filename = askopenfilename(filetypes=self.CHART_FILE_TYPES,
                                   defaultextension='.pickle')
        if not filename: return
        try:
            with open(filename, 'rb') as infile:
                chart = pickle.load(infile)
            self._chart = chart
            self._cv.update(chart)
            if self._matrix: self._matrix.set_chart(chart)
            if self._matrix: self._matrix.deselect_cell()
            if self._results: self._results.set_chart(chart)
            self._cp.set_chart(chart)
        except Exception as e:
            raise
            tkinter.messagebox.showerror('Error Loading Chart',
                                   'Unable to open file: %r' % filename)

    def save_chart(self, *args):
        "Save a chart to a pickle file"
        filename = asksaveasfilename(filetypes=self.CHART_FILE_TYPES,
                                     defaultextension='.pickle')
        if not filename: return
        try:
            with open(filename, 'wb') as outfile:
                pickle.dump(self._chart, outfile)
        except Exception as e:
            raise
            tkinter.messagebox.showerror('Error Saving Chart',
                                   'Unable to open file: %r' % filename)

    def load_grammar(self, *args):
        "Load a grammar from a pickle file"
        filename = askopenfilename(filetypes=self.GRAMMAR_FILE_TYPES,
                                   defaultextension='.cfg')
        if not filename: return
        try:
            if filename.endswith('.pickle'):
                with open(filename, 'rb') as infile:
                    grammar = pickle.load(infile)
            else:
                with open(filename, 'r') as infile:
                    grammar = CFG.fromstring(infile.read())
            self.set_grammar(grammar)
        except Exception as e:
            tkinter.messagebox.showerror('Error Loading Grammar',
                                   'Unable to open file: %r' % filename)

    def save_grammar(self, *args):
        filename = asksaveasfilename(filetypes=self.GRAMMAR_FILE_TYPES,
                                     defaultextension='.cfg')
        if not filename: return
        try:
            if filename.endswith('.pickle'):
                with open(filename, 'wb') as outfile:
                    pickle.dump((self._chart, self._tokens), outfile)
            else:
                with open(filename, 'w') as outfile:
                    prods = self._grammar.productions()
                    start = [p for p in prods if p.lhs() == self._grammar.start()]
                    rest = [p for p in prods if p.lhs() != self._grammar.start()]
                    for prod in start: outfile.write('%s\n' % prod)
                    for prod in rest: outfile.write('%s\n' % prod)
        except Exception as e:
            tkinter.messagebox.showerror('Error Saving Grammar',
                                   'Unable to open file: %r' % filename)

    def reset(self, *args):
        self._animating = 0
        self._reset_parser()
        self._cv.update(self._chart)
        if self._matrix: self._matrix.set_chart(self._chart)
        if self._matrix: self._matrix.deselect_cell()
        if self._results: self._results.set_chart(self._chart)

    #////////////////////////////////////////////////////////////
    # Edit
    #////////////////////////////////////////////////////////////

    def edit_grammar(self, *e):
        CFGEditor(self._root, self._grammar, self.set_grammar)

    def set_grammar(self, grammar):
        self._grammar = grammar
        self._cp.set_grammar(grammar)
        if self._results: self._results.set_grammar(grammar)

    def edit_sentence(self, *e):
        sentence = " ".join(self._tokens)
        title = 'Edit Text'
        instr = 'Enter a new sentence to parse.'
        EntryDialog(self._root, sentence, instr, self.set_sentence, title)

    def set_sentence(self, sentence):
        self._tokens = list(sentence.split())
        self.reset()

    #////////////////////////////////////////////////////////////
    # View Menu
    #////////////////////////////////////////////////////////////

    def view_matrix(self, *e):
        if self._matrix is not None: self._matrix.destroy()
        self._matrix = ChartMatrixView(self._root, self._chart)
        self._matrix.add_callback('select', self._select_matrix_edge)

    def view_results(self, *e):
        if self._results is not None: self._results.destroy()
        self._results = ChartResultsView(self._root, self._chart,
                                         self._grammar)

    #////////////////////////////////////////////////////////////
    # Zoom Menu
    #////////////////////////////////////////////////////////////

    def resize(self):
        self._animating = 0
        self.set_font_size(self._size.get())

    def set_font_size(self, size):
        self._cv.set_font_size(size)
        self._font.configure(size=-abs(size))
        self._boldfont.configure(size=-abs(size))
        self._sysfont.configure(size=-abs(size))

    def get_font_size(self):
        return abs(self._size.get())

    #////////////////////////////////////////////////////////////
    # Parsing
    #////////////////////////////////////////////////////////////

    def apply_strategy(self, strategy, edge_strategy=None):
        # If we're animating, then stop.
        if self._animating:
            self._animating = 0
            return

        # Clear the rule display & mark.
        self._display_rule(None)
        #self._cv.unmark_edge()

        if self._step.get():
            selection = self._selection
            if (selection is not None) and (edge_strategy is not None):
                # Apply the given strategy to the selected edge.
                self._cp.set_strategy([edge_strategy(selection)])
                newedge = self._apply_strategy()

                # If it failed, then clear the selection.
                if newedge is None:
                    self._cv.unmark_edge()
                    self._selection = None
            else:
                self._cp.set_strategy(strategy)
                self._apply_strategy()

        else:
            self._cp.set_strategy(strategy)
            if self._animate.get():
                self._animating = 1
                self._animate_strategy()
            else:
                for edge in self._cpstep:
                    if edge is None: break
                self._cv.update()
                if self._matrix: self._matrix.update()
                if self._results: self._results.update()

    def _stop_animation(self, *e):
        self._animating = 0

    def _animate_strategy(self, speed=1):
        if self._animating == 0: return
        if self._apply_strategy() is not None:
            if self._animate.get() == 0 or self._step.get() == 1:
                return
            if self._animate.get() == 1:
                self._root.after(3000, self._animate_strategy)
            elif self._animate.get() == 2:
                self._root.after(1000, self._animate_strategy)
            else:
                self._root.after(20, self._animate_strategy)

    def _apply_strategy(self):
        new_edge = next(self._cpstep)

        if new_edge is not None:
            self._show_new_edge(new_edge)
        return new_edge

    def _display_rule(self, rule):
        if rule is None:
            self._rulelabel2['text'] = ''
        else:
            name = str(rule)
            self._rulelabel2['text'] = name
            size = self._cv.get_font_size()

    #////////////////////////////////////////////////////////////
    # Parsing Strategies
    #////////////////////////////////////////////////////////////

    # Basic rules:
    _TD_INIT     = [TopDownInitRule()]
    _TD_PREDICT  = [TopDownPredictRule()]
    _BU_RULE     = [BottomUpPredictRule()]
    _BU_LC_RULE  = [BottomUpPredictCombineRule()]
    _FUNDAMENTAL = [SingleEdgeFundamentalRule()]

    # Complete strategies:
    _TD_STRATEGY =  _TD_INIT + _TD_PREDICT + _FUNDAMENTAL
    _BU_STRATEGY = _BU_RULE + _FUNDAMENTAL
    _BU_LC_STRATEGY = _BU_LC_RULE + _FUNDAMENTAL

    # Button callback functions:
    def top_down_init(self, *e):
        self.apply_strategy(self._TD_INIT, None)
    def top_down_predict(self, *e):
        self.apply_strategy(self._TD_PREDICT, TopDownPredictEdgeRule)
    def bottom_up(self, *e):
        self.apply_strategy(self._BU_RULE, BottomUpEdgeRule)
    def bottom_up_leftcorner(self, *e):
        self.apply_strategy(self._BU_LC_RULE, BottomUpLeftCornerEdgeRule)
    def fundamental(self, *e):
        self.apply_strategy(self._FUNDAMENTAL, FundamentalEdgeRule)
    def bottom_up_strategy(self, *e):
        self.apply_strategy(self._BU_STRATEGY, BottomUpEdgeRule)
    def bottom_up_leftcorner_strategy(self, *e):
        self.apply_strategy(self._BU_LC_STRATEGY, BottomUpLeftCornerEdgeRule)
    def top_down_strategy(self, *e):
        self.apply_strategy(self._TD_STRATEGY, TopDownPredictEdgeRule)

def app():
    grammar = CFG.fromstring("""
    # Grammatical productions.
        S -> NP VP
        VP -> VP PP | V NP | V
        NP -> Det N | NP PP
        PP -> P NP
    # Lexical productions.
        NP -> 'John' | 'I'
        Det -> 'the' | 'my' | 'a'
        N -> 'dog' | 'cookie' | 'table' | 'cake' | 'fork'
        V -> 'ate' | 'saw'
        P -> 'on' | 'under' | 'with'
    """)

    sent = 'John ate the cake on the table with a fork'
    sent = 'John ate the cake on the table'
    tokens = list(sent.split())

    print('grammar= (')
    for rule in grammar.productions():
        print(('    ', repr(rule)+','))
    print(')')
    print(('tokens = %r' % tokens))
    print('Calling "ChartParserApp(grammar, tokens)"...')
    ChartParserApp(grammar, tokens).mainloop()

if __name__ == '__main__':
    app()

    # Chart comparer:
    #charts = ['/tmp/earley.pickle',
    #          '/tmp/topdown.pickle',
    #          '/tmp/bottomup.pickle']
    #ChartComparer(*charts).mainloop()

    #import profile
    #profile.run('demo2()', '/tmp/profile.out')
    #import pstats
    #p = pstats.Stats('/tmp/profile.out')
    #p.strip_dirs().sort_stats('time', 'cum').print_stats(60)
    #p.strip_dirs().sort_stats('cum', 'time').print_stats(60)

__all__ = ['app']