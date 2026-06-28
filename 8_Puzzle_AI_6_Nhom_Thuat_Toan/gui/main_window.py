from __future__ import annotations
import json, threading, datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.core import (
    START_DEFAULT, GOAL_DEFAULT, DEFAULT_MAX_NODES, State, parse_state, state_to_text,
    is_solvable, random_solvable_state
)
from algorithms.registry import ALGORITHM_GROUPS, HEURISTIC_ALGORITHMS

HISTORY_FILE = Path(__file__).resolve().parent.parent / 'history' / 'history.json'

class EightPuzzleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('8 Puzzle AI Solver - 6 nhóm thuật toán')
        self.geometry('1380x780')
        self.minsize(1280, 720)
        self.configure(bg='#eef3f8')
        self.path: list[State] = []
        self.moves: list[str] = []
        self.current_step = 0
        self.playing = False
        self.after_id = None
        self.running = False
        self.history: list[dict] = []
        self._style()
        self._build_ui()
        self._load_history()
        self.draw_board(START_DEFAULT)
        self._refresh_algo_box()
        self._update_heuristic_state()

    def _style(self):
        style = ttk.Style(self)
        try: style.theme_use('clam')
        except tk.TclError: pass
        style.configure('TFrame', background='#eef3f8')
        style.configure('Card.TFrame', background='white', relief='flat')
        style.configure('TLabel', background='#eef3f8', font=('Segoe UI', 10))
        style.configure('Title.TLabel', background='#eef3f8', foreground='#1d3557', font=('Segoe UI', 20, 'bold'))
        style.configure('Sub.TLabel', background='#eef3f8', foreground='#52616b', font=('Segoe UI', 10))
        style.configure('TLabelframe', background='#eef3f8')
        style.configure('TLabelframe.Label', font=('Segoe UI', 10, 'bold'), foreground='#1d3557')
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        style.configure('TButton', padding=4)
        style.configure('Treeview', rowheight=30, font=('Segoe UI', 9))
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))

    def _build_ui(self):
        header = ttk.Frame(self, padding=(16, 14, 16, 8))
        header.pack(fill=tk.X)
        ttk.Label(header, text='8 Puzzle AI Solver', style='Title.TLabel').pack(anchor='w')
        ttk.Label(header, text='Đủ 6 nhóm thuật toán, có mô phỏng đường đi và lưu lịch sử chạy.', style='Sub.TLabel').pack(anchor='w')

        main = ttk.Frame(self, padding=(16, 6, 16, 16))
        main.pack(fill=tk.BOTH, expand=True)
        left = ttk.Frame(main, width=270)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)
        center = ttk.Frame(main, width=360)
        center.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        center.pack_propagate(False)
        right = ttk.Frame(main, width=720)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right.pack_propagate(False)

        setup = ttk.LabelFrame(left, text='Thiết lập', padding=12)
        setup.pack(fill=tk.X)
        self.start_var = tk.StringVar(value=state_to_text(START_DEFAULT))
        self.goal_var = tk.StringVar(value=state_to_text(GOAL_DEFAULT))
        self.group_var = tk.StringVar(value='Informed Search')
        self.algorithm_var = tk.StringVar(value='A*')
        self.heuristic_var = tk.StringVar(value='Manhattan')
        self.depth_var = tk.IntVar(value=35)
        self.beam_var = tk.IntVar(value=10)
        self.max_nodes_var = tk.IntVar(value=DEFAULT_MAX_NODES)
        self.speed_var = tk.IntVar(value=450)

        rows = [
            ('Trạng thái đầu', ttk.Entry(setup, textvariable=self.start_var, width=23)),
            ('Trạng thái đích', ttk.Entry(setup, textvariable=self.goal_var, width=23)),
            ('Nhóm thuật toán', ttk.Combobox(setup, textvariable=self.group_var, values=list(ALGORITHM_GROUPS), state='readonly', width=32)),
            ('Thuật toán', ttk.Combobox(setup, textvariable=self.algorithm_var, state='readonly', width=32)),
            ('Heuristic', ttk.Combobox(setup, textvariable=self.heuristic_var, values=['Manhattan', 'Số ô sai'], state='readonly', width=18)),
            ('Depth limit / vòng lặp', ttk.Spinbox(setup, from_=1, to=120, textvariable=self.depth_var, width=10)),
            ('Beam / Restart', ttk.Spinbox(setup, from_=1, to=200, textvariable=self.beam_var, width=10)),
            ('Giới hạn node', ttk.Entry(setup, textvariable=self.max_nodes_var, width=16)),
            ('Tốc độ mô phỏng ms', ttk.Scale(setup, from_=80, to=1200, variable=self.speed_var, orient=tk.HORIZONTAL)),
        ]
        for i,(label,widget) in enumerate(rows):
            ttk.Label(setup, text=label+':').grid(row=i, column=0, sticky='w', pady=5)
            widget.grid(row=i, column=1, sticky='ew', pady=5)
        setup.columnconfigure(1, weight=1)
        rows[2][1].bind('<<ComboboxSelected>>', lambda e: self._refresh_algo_box())
        rows[3][1].bind('<<ComboboxSelected>>', lambda e: self._update_heuristic_state())

        actions = ttk.LabelFrame(left, text='Thao tác', padding=6)
        actions.pack(fill=tk.X, pady=6)
        self.run_btn = ttk.Button(actions, text='▶ Chạy thuật toán', style='Accent.TButton', command=self.start_run)
        self.run_btn.pack(fill=tk.X, pady=2)
        ttk.Button(actions, text='🎲 Random', command=self.random_start).pack(fill=tk.X, pady=2)
        ttk.Button(actions, text='↺ Reset', command=self.reset_default).pack(fill=tk.X, pady=2)
        ttk.Button(actions, text='🗑 Xóa lịch sử', command=self.clear_history).pack(fill=tk.X, pady=2)

        info = ttk.LabelFrame(left, text='Ghi chú', padding=8)
        info.pack(fill=tk.BOTH, expand=True)
        ttk.Label(info, justify=tk.LEFT, wraplength=250, text=(
            '• BFS/UCS/A* thường cho lời giải tối ưu.\n'
            '• DFS/IDS phụ thuộc giới hạn độ sâu.\n'
            '• Local Search có thể kẹt ở cực trị cục bộ.\n'
            '• CSP và Adversarial được mô phỏng để minh họa vì 8-puzzle gốc không phải game đối kháng/CSP tự nhiên.'
        )).pack(anchor='w')

        board_box = ttk.LabelFrame(center, text='Bàn cờ', padding=8)
        board_box.pack(fill=tk.X)
        self.board = tk.Canvas(board_box, width=240, height=240, bg='white', highlightthickness=0)
        self.board.pack(pady=2)

        controls = ttk.Frame(center)
        controls.pack(fill=tk.X, pady=6)
        ttk.Button(controls, text='⏮ Đầu', command=self.first_step).pack(side=tk.LEFT, padx=3)
        ttk.Button(controls, text='◀ Trước', command=self.prev_step).pack(side=tk.LEFT, padx=3)
        self.play_btn = ttk.Button(controls, text='▶ Play', command=self.toggle_play)
        self.play_btn.pack(side=tk.LEFT, padx=3)
        ttk.Button(controls, text='Sau ▶', command=self.next_step).pack(side=tk.LEFT, padx=3)
        ttk.Button(controls, text='Cuối ⏭', command=self.last_step).pack(side=tk.LEFT, padx=3)

        self.status_var = tk.StringVar(value='Sẵn sàng.')
        ttk.Label(center, textvariable=self.status_var, wraplength=380, font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(2, 6))
        self.move_var = tk.StringVar(value='Bước: 0/0')
        ttk.Label(center, textvariable=self.move_var).pack(anchor='w')

        result_box = ttk.LabelFrame(center, text='Kết quả', padding=10)
        result_box.pack(fill=tk.BOTH, expand=True)
        self.result_text = tk.Text(result_box, height=7, wrap='word', bg='#fbfdff', relief='flat', font=('Consolas', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)

        history_box = ttk.LabelFrame(right, text='Lịch sử chạy', padding=10)
        history_box.pack(fill=tk.BOTH, expand=True)
        cols=('time','group','algorithm','start','goal','cost','expanded','generated','elapsed','status')
        self.tree = ttk.Treeview(history_box, columns=cols, show='headings', height=30)
        headings={
            'time':'Thời gian','group':'Nhóm thuật toán','algorithm':'Thuật toán',
            'start':'Start','goal':'Goal','cost':'Cost','expanded':'Expanded',
            'generated':'Generated','elapsed':'Time(s)','status':'Trạng thái'
        }
        widths={'time':135,'group':220,'algorithm':210,'start':85,'goal':85,'cost':55,'expanded':85,'generated':90,'elapsed':85,'status':85}
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=widths[c], minwidth=widths[c], anchor='w', stretch=False)
        ybar = ttk.Scrollbar(history_box, orient=tk.VERTICAL, command=self.tree.yview)
        xbar = ttk.Scrollbar(history_box, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        ybar.grid(row=0, column=1, sticky='ns')
        xbar.grid(row=1, column=0, sticky='ew')
        history_box.rowconfigure(0, weight=1)
        history_box.columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self.load_history_item)

    def _refresh_algo_box(self):
        algos = list(ALGORITHM_GROUPS[self.group_var.get()].keys())
        box = self.nametowidget(str(self.children['!frame2'].children['!frame'].children['!labelframe'].grid_slaves(row=3, column=1)[0])) if False else None
        # direct search by stored widget is unnecessary; combobox is found by textvariable via children traversal not stable.
        for child in self.winfo_children(): pass
        # simpler: keep reference by querying setup children from _build_ui impossible here, so recreate via recursive lookup
        cb = self._find_combo_for_var(self.algorithm_var)
        if cb: cb['values'] = algos
        if self.algorithm_var.get() not in algos: self.algorithm_var.set(algos[0])
        self._update_heuristic_state()

    def _find_combo_for_var(self, var):
        def walk(w):
            for ch in w.winfo_children():
                if isinstance(ch, ttk.Combobox) and str(ch.cget('textvariable')) == str(var): return ch
                r=walk(ch)
                if r: return r
        return walk(self)

    def _update_heuristic_state(self):
        cb = self._find_combo_for_var(self.heuristic_var)
        if cb: cb.configure(state='readonly' if self.algorithm_var.get() in HEURISTIC_ALGORITHMS else 'disabled')

    def draw_board(self, state: State):
        self.board.delete('all')
        size=66; gap=7; ox=12; oy=12
        colors = {'tile':'#457b9d','blank':'#e9f1f7','text':'white'}
        for i,v in enumerate(state):
            r,c=divmod(i,3); x=ox+c*(size+gap); y=oy+r*(size+gap)
            fill = colors['blank'] if v==0 else colors['tile']
            self.board.create_rectangle(x,y,x+size,y+size, fill=fill, outline='#d6e0ea', width=2)
            if v!=0:
                self.board.create_text(x+size/2,y+size/2,text=str(v),fill=colors['text'],font=('Segoe UI',22,'bold'))
        self.move_var.set(f'Bước: {self.current_step}/{max(0,len(self.path)-1)}')

    def start_run(self):
        if self.running: return
        try:
            start=parse_state(self.start_var.get()); goal=parse_state(self.goal_var.get())
            if not is_solvable(start, goal):
                messagebox.showerror('Không giải được', 'Trạng thái đầu và đích khác parity nghịch thế nên không giải được.'); return
        except Exception as e:
            messagebox.showerror('Lỗi nhập liệu', str(e)); return
        self.running=True; self.run_btn.configure(state='disabled'); self.status_var.set('Đang chạy thuật toán...')
        threading.Thread(target=self._run_worker, args=(start,goal), daemon=True).start()

    def _run_worker(self, start, goal):
        group=self.group_var.get(); algo=self.algorithm_var.get(); fn=ALGORITHM_GROUPS[group][algo]
        try:
            r=fn(start, goal, heuristic=self.heuristic_var.get(), depth_limit=int(self.depth_var.get()),
                 beam_width=int(self.beam_var.get()), restarts=int(self.beam_var.get()), max_nodes=int(self.max_nodes_var.get()))
            r.group=group; r.algorithm=algo
            self.after(0, lambda: self._show_result(r, start, goal))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('Lỗi khi chạy', str(e)))
            self.after(0, self._finish_run)

    def _show_result(self, r, start, goal):
        self.path=r.path or [start]; self.moves=r.moves; self.current_step=0; self.draw_board(self.path[0])
        self.status_var.set(r.message)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f'Nhóm: {r.group}\nThuật toán: {r.algorithm}\n')
        self.result_text.insert(tk.END, f'Trạng thái đầu: {state_to_text(start)}\nTrạng thái đích: {state_to_text(goal)}\n')
        self.result_text.insert(tk.END, f'Tìm thấy: {"Có" if r.found else "Không"}\nCost/Số bước: {r.cost}\nExpanded: {r.expanded}\nGenerated: {r.generated}\nMax frontier: {r.max_frontier}\nThời gian: {r.elapsed:.6f}s\n')
        self.result_text.insert(tk.END, 'Moves: ' + (', '.join(r.moves) if r.moves else '(trống)'))
        self._add_history(r, start, goal)
        self._finish_run()

    def _finish_run(self):
        self.running=False; self.run_btn.configure(state='normal')

    def _add_history(self, r, start, goal):
        item={
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'group': r.group, 'algorithm': r.algorithm,
            'start': state_to_text(start), 'goal': state_to_text(goal), 'found': r.found, 'cost': r.cost,
            'expanded': r.expanded, 'generated': r.generated, 'elapsed': r.elapsed, 'message': r.message,
            'path': [state_to_text(s) for s in r.path], 'moves': r.moves
        }
        self.history.insert(0,item); self.history=self.history[:100]; self._save_history(); self._render_history()

    def _load_history(self):
        if HISTORY_FILE.exists():
            try: self.history=json.loads(HISTORY_FILE.read_text(encoding='utf-8'))
            except Exception: self.history=[]
        self._render_history()

    def _save_history(self):
        HISTORY_FILE.write_text(json.dumps(self.history, ensure_ascii=False, indent=2), encoding='utf-8')

    def _render_history(self):
        self.tree.delete(*self.tree.get_children())
        for idx,item in enumerate(self.history):
            self.tree.insert('', tk.END, iid=str(idx), values=(
                item['time'], item['group'], item['algorithm'], item.get('start',''), item.get('goal',''),
                item.get('cost',''), item.get('expanded',''), item.get('generated',''),
                f"{item.get('elapsed',0):.6f}" if isinstance(item.get('elapsed',0),(int,float)) else item.get('elapsed',''),
                'OK' if item.get('found') else 'Fail'
            ))

    def load_history_item(self, event=None):
        sel=self.tree.selection()
        if not sel: return
        item=self.history[int(sel[0])]
        self.start_var.set(item['start']); self.goal_var.set(item['goal']); self.group_var.set(item['group']); self._refresh_algo_box(); self.algorithm_var.set(item['algorithm'])
        self.path=[parse_state(s) for s in item.get('path', [])] or [parse_state(item['start'])]
        self.moves=item.get('moves', []); self.current_step=0; self.draw_board(self.path[0])
        self.status_var.set('Đã tải lại lịch sử: ' + item['message'])
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, json.dumps(item, ensure_ascii=False, indent=2))

    def clear_history(self):
        self.history=[]; self._save_history(); self._render_history(); self.status_var.set('Đã xóa lịch sử.')

    def random_start(self):
        self.start_var.set(state_to_text(random_solvable_state(GOAL_DEFAULT, 70)))
        self.draw_board(parse_state(self.start_var.get()))

    def reset_default(self):
        self.start_var.set(state_to_text(START_DEFAULT)); self.goal_var.set(state_to_text(GOAL_DEFAULT)); self.group_var.set('Informed Search'); self._refresh_algo_box(); self.algorithm_var.set('A*'); self.path=[]; self.moves=[]; self.current_step=0; self.draw_board(START_DEFAULT); self.status_var.set('Đã reset mặc định.')

    def first_step(self):
        if self.path: self.current_step=0; self.draw_board(self.path[0])
    def last_step(self):
        if self.path: self.current_step=len(self.path)-1; self.draw_board(self.path[-1])
    def prev_step(self):
        if self.path and self.current_step>0: self.current_step-=1; self.draw_board(self.path[self.current_step])
    def next_step(self):
        if self.path and self.current_step<len(self.path)-1: self.current_step+=1; self.draw_board(self.path[self.current_step])
    def toggle_play(self):
        if not self.path: return
        self.playing=not self.playing; self.play_btn.configure(text='⏸ Pause' if self.playing else '▶ Play')
        if self.playing: self._play_loop()
    def _play_loop(self):
        if not self.playing: return
        if self.current_step>=len(self.path)-1:
            self.playing=False; self.play_btn.configure(text='▶ Play'); return
        self.next_step(); self.after_id=self.after(int(self.speed_var.get()), self._play_loop)


