
        
        # ---------------------------
        # Panel derecho - Lista de tareas
        # ---------------------------
        tasks_frame = ttk.LabelFrame(right_panel, text="Lista de Tareas", padding=10)
        tasks_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para mostrar las tareas
        self.tasks_tree = ttk.Treeview(tasks_frame, columns=("title", "due_date", "priority", "status", "tags"), show="headings")
        self.tasks_tree.heading("title", text="Título")
        self.tasks_tree.heading("due_date", text="Fecha Límite")
        self.tasks_tree.heading("priority", text="Prioridad")
        self.tasks_tree.heading("status", text="Estado")
        self.tasks_tree.heading("tags", text="Etiquetas")
        
        self.tasks_tree.column("title", width=200)
        self.tasks_tree.column("due_date", width=100)
        self.tasks_tree.column("priority", width=80)
        self.tasks_tree.column("status", width=100)
        self.tasks_tree.column("tags", width=150)
        
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones para editar/eliminar
        button_frame = ttk.Frame(tasks_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="Editar", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ver Detalles", command=self.view_details).pack(side=tk.LEFT, padx=5)
        
        # ---------------------------
        # Panel derecho - Calendario
        # ---------------------------
        calendar_frame = ttk.LabelFrame(right_panel, text="Calendario", padding=10)
        calendar_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Calendario interactivo
        self.calendar = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(fill=tk.BOTH, expand=True)
        
        # Visualización de tareas en el calendario
        ttk.Button(calendar_frame, text="Mostrar Tareas en Calendario", 
                  command=self.show_calendar_tasks).pack(pady=5)
        
        # Gráfico de tareas pendientes
        self.create_timeline_chart(right_panel)
    
    def create_timeline_chart(self, parent):
        chart_frame = ttk.LabelFrame(parent, text="Línea de Tiempo de Tareas", padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(chart_frame, text="Actualizar Gráfico", 
                  command=self.update_timeline_chart).pack(pady=5)
    
    def update_timeline_chart(self):
        self.ax.clear()
        
        if not self.filtered_tasks:
            self.ax.text(0.5, 0.5, 'No hay tareas para mostrar', 
                        ha='center', va='center', fontsize=12)
            self.canvas.draw()
            return
        
        # Preparar datos para el gráfico
        tasks = sorted(self.filtered_tasks, key=lambda x: x['due_date'])
        titles = [task['title'] for task in tasks]
        dates = [datetime.strptime(task['due_date'], '%Y-%m-%d') for task in tasks]
        priorities = [task['priority'] for task in tasks]
        
        # Colores según prioridad
        colors = {'alta': 'red', 'media': 'orange', 'baja': 'green'}
        
        # Crear líneas de tiempo
        for i, (title, date, priority) in enumerate(zip(titles, dates, priorities)):
            self.ax.plot([date, date], [i-0.4, i+0.4], color=colors[priority], linewidth=3)
            self.ax.text(date + timedelta(days=1), i, title, va='center')
        
        # Configurar el gráfico
        self.ax.set_yticks(range(len(tasks)))
        self.ax.set_yticklabels(titles)
        self.ax.set_xlim(min(dates) - timedelta(days=2), max(dates) + timedelta(days=5))
        self.ax.grid(True)
        
        # Rotar etiquetas de fecha
        for label in self.ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')
        
        self.fig.tight_layout()
        self.canvas.draw()
    
  
