import tkinter as tk
from tkinter import ttk, messagebox
import threading
from core.scanner import SystemScanner
from core.exporter import DataExporter

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SysInfo Collector")
        self.setup_fullscreen()
        self.scanner = SystemScanner()
        self.exporter = DataExporter()
        
        self.hardware_var = tk.BooleanVar(value=True)
        self.software_var = tk.BooleanVar(value=True)
        self.network_var = tk.BooleanVar(value=True)
        
        self.setup_styles()
        self.setup_ui()
        self.show_main_page()
    
    def setup_fullscreen(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.minsize(400, 550)
        window_width = 450
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def setup_styles(self):
        self.colors = {
            'background': '#111c21',
            'card': '#1E1E1E',
            'text': '#E5E5E7',
            'secondary_text': '#8E8E93',
            'primary': '#1791cf',
            'button_bg': '#2C2C2E',
            'button_hover': '#3C3C3E',
            'button_text': '#E5E5E7',
            'border': '#374151',
            'tab_bg': '#2C2C2E',
            'tab_active': '#1791cf',
            'success': '#34C759'
        }
        self.root.configure(bg=self.colors['background'])
    
    def setup_ui(self):
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.grid(row=0, column=0, sticky='nsew')
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
    
    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_main_page(self):
        self.clear_container()
        
        center_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        center_frame.grid(row=0, column=0, sticky='nsew')
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        
        main_card = tk.Frame(center_frame, bg=self.colors['card'], padx=24, pady=24)
        main_card.grid(row=0, column=0, sticky='', padx=20, pady=20)
        
        header_frame = tk.Frame(main_card, bg=self.colors['card'])
        header_frame.pack(fill='x', pady=(0, 24))
        
        title_label = tk.Label(header_frame, text="SysInfo Collector", 
                              font=('Inter', 16, 'bold'),
                              bg=self.colors['card'], fg=self.colors['text'])
        title_label.pack(side='left', expand=True, padx=10)
        
        separator = tk.Frame(main_card, height=1, bg=self.colors['border'])
        separator.pack(fill='x', pady=(0, 24))
        
        content_frame = tk.Frame(main_card, bg=self.colors['card'])
        content_frame.pack(fill='both', expand=True)
        
        section_title = tk.Label(content_frame, text="Сбор системной информации",
                                font=('Inter', 16, 'bold'),
                                bg=self.colors['card'], fg=self.colors['text'])
        section_title.pack(anchor='w', pady=(0, 24))
        
        checkboxes_frame = tk.Frame(content_frame, bg=self.colors['card'])
        checkboxes_frame.pack(fill='x', pady=12)
        
        self.create_checkbox(checkboxes_frame, "Аппаратное обеспечение", self.hardware_var)
        self.create_checkbox(checkboxes_frame, "Программное обеспечение", self.software_var)
        self.create_checkbox(checkboxes_frame, "Сетевые настройки", self.network_var)
        
        footer_frame = tk.Frame(main_card, bg=self.colors['card'])
        footer_frame.pack(fill='x', pady=(24, 0))
        
        self.scan_button = tk.Button(footer_frame, text="Начать сканирование",
                                    bg=self.colors['button_bg'],
                                    fg=self.colors['button_text'],
                                    font=('Inter', 14, 'bold'),
                                    relief='flat',
                                    border=0,
                                    cursor='hand2',
                                    command=self.start_scan)
        self.scan_button.pack(fill='x', ipady=16)
        
        self.scan_button.bind('<Enter>', self.on_button_enter)
        self.scan_button.bind('<Leave>', self.on_button_leave)
    
    def create_checkbox(self, parent, text, variable):
        checkbox_frame = tk.Frame(parent, bg=self.colors['card'])
        checkbox_frame.pack(fill='x', pady=12)
        
        canvas = tk.Canvas(checkbox_frame, width=24, height=24, bg=self.colors['card'],
                          highlightthickness=0, cursor='hand2')
        canvas.pack(side='left', padx=(0, 16))
        
        text_label = tk.Label(checkbox_frame, text=text, font=('Inter', 14),
                             bg=self.colors['card'], fg=self.colors['text'], cursor='hand2')
        text_label.pack(side='left')
        
        def update_checkbox():
            canvas.delete("all")
            canvas.create_rectangle(2, 2, 22, 22, outline=self.colors['primary'], width=2)
            if variable.get():
                canvas.create_rectangle(4, 4, 20, 20, fill=self.colors['primary'], 
                                      outline=self.colors['primary'])
        
        def toggle_checkbox(event=None):
            variable.set(not variable.get())
            update_checkbox()
        
        canvas.bind('<Button-1>', toggle_checkbox)
        text_label.bind('<Button-1>', toggle_checkbox)
        
        update_checkbox()
    
    def on_button_enter(self, event):
        self.scan_button.configure(bg=self.colors['button_hover'])
    
    def on_button_leave(self, event):
        self.scan_button.configure(bg=self.colors['button_bg'])
    
    def start_scan(self):
        categories = {
            'hardware': self.hardware_var.get(),
            'software': self.software_var.get(),
            'network': self.network_var.get()
        }
        
        if not any(categories.values()):
            messagebox.showerror("Ошибка", "Выберите хотя бы одну категорию для сканирования")
            return
        
        self.show_scan_page(categories)
    
    def show_scan_page(self, categories):
        self.clear_container()
        
        main_frame = tk.Frame(self.main_container, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_frame, bg=self.colors['background'])
        header_frame.pack(fill='x', pady=(0, 30))
        
        back_button = tk.Button(header_frame, text="←", font=('Inter', 16),
                               bg=self.colors['background'], fg=self.colors['text'],
                               relief='flat', border=0, cursor='hand2',
                               command=self.show_main_page)
        back_button.pack(side='left')
        
        title_label = tk.Label(header_frame, text="Сканирование системы",
                              font=('Inter', 16, 'bold'),
                              bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(side='left', padx=10)
        
        progress_section = tk.Frame(main_frame, bg=self.colors['background'])
        progress_section.pack(fill='x', pady=(0, 30))
        
        self.progress_label = tk.Label(progress_section, text="Сбор данных...",
                                 font=('Inter', 14, 'bold'),
                                 bg=self.colors['background'], fg=self.colors['text'])
        self.progress_label.pack(anchor='w')
        
        progress_bg = tk.Frame(progress_section, bg='#374151', height=8)
        progress_bg.pack(fill='x', pady=(10, 0))
        
        self.progress_bar = tk.Frame(progress_bg, bg=self.colors['primary'], height=8)
        self.progress_bar.place(relx=0, rely=0, relwidth=0.0, relheight=1)
        
        self.categories_list = tk.Frame(main_frame, bg=self.colors['background'])
        self.categories_list.pack(fill='both', expand=True)
        
        self.category_frames = {}
        
        if categories.get('hardware', False):
            self.category_frames['hardware'] = self.create_category_row(
                self.categories_list, "Аппаратное обеспечение", "waiting"
            )
        
        if categories.get('network', False):
            self.category_frames['network'] = self.create_category_row(
                self.categories_list, "Сетевые настройки", "waiting"
            )
        
        if categories.get('software', False):
            self.category_frames['software'] = self.create_category_row(
                self.categories_list, "Программное обеспечение", "waiting"
            )
        
        self.results_button = tk.Button(
            main_frame, 
            text="Посмотреть результаты",
            bg=self.colors['primary'],
            fg='white',
            font=('Inter', 12, 'bold'),
            relief='flat',
            border=0,
            cursor='hand2',
            command=lambda: self.show_results_page(self.scan_data)
        )
        self.results_button.pack(fill='x', pady=(20, 0))
        self.results_button.pack_forget()
        
        self.start_scanning(categories)
    
    def create_category_row(self, parent, text, status):
        frame = tk.Frame(parent, bg=self.colors['card'], height=56)
        frame.pack(fill='x', pady=4)
        frame.pack_propagate(False)
        
        inner_frame = tk.Frame(frame, bg=self.colors['card'], padx=16)
        inner_frame.pack(fill='both', expand=True)
        
        icon_frame = tk.Frame(inner_frame, bg=self.colors['card'], width=40, height=40)
        icon_frame.pack(side='left', padx=(0, 16))
        icon_frame.pack_propagate(False)
        
        status_icon = tk.Label(icon_frame, bg=self.colors['card'], 
                                   font=('Arial', 16))
        status_icon.pack(expand=True)
        
        text_label = tk.Label(inner_frame, text=text, font=('Inter', 14),
                             bg=self.colors['card'], fg=self.colors['text'])
        text_label.pack(side='left', fill='x', expand=True)
        
        self.update_status_icon(status_icon, status)
        
        return {
            'frame': frame,
            'icon': status_icon,
            'text': text_label
        }
    
    def update_status_icon(self, icon, status):
        status_config = {
            'waiting': {'text': '⏳', 'fg': '#8E8E93'},
            'scanning': {'text': '🔄', 'fg': self.colors['primary']},
            'completed': {'text': '✓', 'fg': self.colors['success']}
        }
        
        config = status_config.get(status, status_config['waiting'])
        icon.config(text=config['text'], fg=config['fg'])
    
    def start_scanning(self, categories):
        scan_thread = threading.Thread(target=self._perform_scan, args=(categories,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def _perform_scan(self, categories):
        try:
            total_categories = sum(categories.values())
            if total_categories == 0:
                return
            
            progress_per_category = 100 / total_categories
            current_progress = 0
            
            scan_data = {'timestamp': '', 'scan_categories': {}}
            
            if categories.get('hardware', False):
                self.root.after(0, self._update_category_status, 'hardware', 'scanning')
                hardware_data = self.scanner.scan_hardware()
                scan_data['scan_categories']['hardware'] = hardware_data
                self.root.after(0, self._update_category_status, 'hardware', 'completed')
                current_progress += progress_per_category
                self.root.after(0, self._update_progress_bar, current_progress)
            
            if categories.get('network', False):
                self.root.after(0, self._update_category_status, 'network', 'scanning')
                network_data = self.scanner.scan_network()
                scan_data['scan_categories']['network'] = network_data
                self.root.after(0, self._update_category_status, 'network', 'completed')
                current_progress += progress_per_category
                self.root.after(0, self._update_progress_bar, current_progress)
            
            if categories.get('software', False):
                self.root.after(0, self._update_category_status, 'software', 'scanning')
                software_data = self.scanner.scan_software()
                scan_data['scan_categories']['software'] = software_data
                self.root.after(0, self._update_category_status, 'software', 'completed')
                current_progress += progress_per_category
                self.root.after(0, self._update_progress_bar, current_progress)
            
            self.root.after(0, self._update_progress_bar, 100)
            self.root.after(0, self.on_scan_complete, scan_data)
            
        except Exception as e:
            self.root.after(0, self.on_scan_error, str(e))
    
    def _update_progress_bar(self, value):
        self.progress_bar.place(relx=0, rely=0, relwidth=value/100, relheight=1)
    
    def _update_category_status(self, category, status):
        if category in self.category_frames:
            frame_info = self.category_frames[category]
            self.update_status_icon(frame_info['icon'], status)
    
    def on_scan_complete(self, scan_data):
        self.progress_label.config(text="Сканирование завершено!")
        self.results_button.pack(fill='x', pady=(20, 0))
        self.scan_data = scan_data
    
    def on_scan_error(self, error_message):
        self.progress_label.config(text="Ошибка сканирования")
        messagebox.showerror("Ошибка", f"Ошибка при сканировании:\n{error_message}")
    
    def show_results_page(self, scan_data):
        self.clear_container()
        
        main_frame = tk.Frame(self.main_container, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(main_frame, bg=self.colors['background'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        back_button = tk.Button(header_frame, text="←", font=('Inter', 16),
                               bg=self.colors['background'], fg=self.colors['text'],
                               relief='flat', border=0, cursor='hand2',
                               command=self.show_main_page)
        back_button.pack(side='left')
        
        title_label = tk.Label(header_frame, text="Результаты сканирования",
                              font=('Inter', 24, 'bold'),
                              bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(side='left', padx=10)
        
        tabs_frame = tk.Frame(main_frame, bg=self.colors['tab_bg'], height=40, pady=5)
        tabs_frame.pack(fill='x', pady=(0, 20))
        tabs_frame.pack_propagate(False)
        
        tabs_container = tk.Frame(tabs_frame, bg=self.colors['tab_bg'])
        tabs_container.pack(expand=True, fill='both', padx=5)
        
        self.tab_var = tk.StringVar(value="hardware")
        
        self.content_frame = tk.Frame(main_frame, bg=self.colors['background'])
        self.content_frame.pack(fill='both', expand=True)

        hardware_tab = self.create_tab(tabs_container, "Аппаратура", "hardware", 0)
        software_tab = self.create_tab(tabs_container, "ПО", "software", 1)
        network_tab = self.create_tab(tabs_container, "Сеть", "network", 2)
        export_tab = self.create_tab(tabs_container, "Экспорт", "export", 3)

        self.show_tab_content("hardware", scan_data)
    
    def create_tab(self, parent, text, value, index):
        tab_frame = tk.Frame(parent, bg=self.colors['tab_bg'], relief='flat', 
                            borderwidth=0, cursor='hand2')
        tab_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        tab_label = tk.Label(tab_frame, text=text, 
                           font=('Inter', 10, 'bold'),
                           bg=self.colors['tab_bg'], 
                           fg=self.colors['secondary_text'],
                           padx=10, pady=8)
        tab_label.pack(expand=True, fill='both')
        
        def select_tab():
            for widget in parent.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.configure(bg=self.colors['tab_bg'], fg=self.colors['secondary_text'])

            tab_label.configure(bg=self.colors['tab_active'], fg='white')
            self.tab_var.set(value)
            self.show_tab_content(value, self.scan_data)
        
        tab_frame.bind('<Button-1>', lambda e: select_tab())
        tab_label.bind('<Button-1>', lambda e: select_tab())

        if index == 0:
            tab_label.configure(bg=self.colors['tab_active'], fg='white')
        
        return tab_frame
    
    def show_tab_content(self, tab, scan_data):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if tab == "hardware":
            self.show_hardware_tab(scan_data)
        elif tab == "software":
            self.show_software_tab(scan_data)
        elif tab == "network":
            self.show_network_tab(scan_data)
        elif tab == "export":
            self.show_export_tab(scan_data)
    
    def show_hardware_tab(self, scan_data):
        content = self.create_scrollable_frame(self.content_frame)
        
        if 'hardware' not in scan_data['scan_categories']:
            no_data_label = tk.Label(content, text="Данные об аппаратном обеспечении не собраны",
                                   font=('Inter', 14), bg=self.colors['background'], fg=self.colors['text'])
            no_data_label.pack(pady=20)
            return
        
        hardware_data = scan_data['scan_categories']['hardware']
        
        system_card = tk.Frame(content, bg=self.colors['card'], padx=16, pady=16)
        system_card.pack(fill='x', pady=(0, 16))
        
        system_title = tk.Label(system_card, text="💻 Система",
                              font=('Inter', 18, 'bold'),
                              bg=self.colors['card'], fg=self.colors['text'])
        system_title.pack(anchor='w', pady=(0, 10))
        
        if 'cpu' in hardware_data:
            cpu_info = hardware_data['cpu']
            self.create_info_row(system_card, "Процессор", cpu_info.get('processor', 'Неизвестно'))
            self.create_info_row(system_card, "Ядра", f"{cpu_info.get('physical_cores', '?')} физических, {cpu_info.get('total_cores', '?')} логических")
            if cpu_info.get('frequency'):
                self.create_info_row(system_card, "Частота", f"{cpu_info['frequency']} ГГц")
        
        if 'memory' in hardware_data:
            memory_info = hardware_data['memory']
            self.create_info_row(system_card, "Память (RAM)", f"{memory_info.get('total', '?')} ГБ (доступно: {memory_info.get('available', '?')} ГБ)")
        
        if 'disks' in hardware_data and hardware_data['disks']:
            disks_card = tk.Frame(content, bg=self.colors['card'], padx=16, pady=16)
            disks_card.pack(fill='x', pady=(0, 16))
            
            disks_title = tk.Label(disks_card, text="💾 Диски",
                                 font=('Inter', 18, 'bold'),
                                 bg=self.colors['card'], fg=self.colors['text'])
            disks_title.pack(anchor='w', pady=(0, 10))
            
            for disk in hardware_data['disks']:
                disk_name = disk.get('device', 'Неизвестный диск')
                total_gb = disk.get('total', 0)
                free_gb = disk.get('free', 0)
                self.create_disk_row(disks_card, disk_name, f"{total_gb} ГБ", f"Свободно {free_gb} ГБ")
    
    def show_software_tab(self, scan_data):
        content = self.create_scrollable_frame(self.content_frame)
        
        if 'software' not in scan_data['scan_categories']:
            no_data_label = tk.Label(content, text="Данные о программном обеспечении не собраны",
                                   font=('Inter', 14), bg=self.colors['background'], fg=self.colors['text'])
            no_data_label.pack(pady=20)
            return
        
        software_data = scan_data['scan_categories']['software']
        
        os_card = tk.Frame(content, bg=self.colors['card'], padx=16, pady=16)
        os_card.pack(fill='x', pady=(0, 16))
        
        os_title = tk.Label(os_card, text="🖥️ Операционная система",
                          font=('Inter', 18, 'bold'),
                          bg=self.colors['card'], fg=self.colors['text'])
        os_title.pack(anchor='w', pady=(0, 10))
        
        if 'os' in software_data:
            os_info = software_data['os']
            self.create_info_row(os_card, "Система", os_info.get('system', 'Неизвестно'))
            self.create_info_row(os_card, "Версия", os_info.get('release', 'Неизвестно'))
            self.create_info_row(os_card, "Сборка", os_info.get('version', 'Неизвестно'))
            self.create_info_row(os_card, "Имя хоста", os_info.get('hostname', 'Неизвестно'))
    
    def show_network_tab(self, scan_data):
        content = self.create_scrollable_frame(self.content_frame)

        
        if 'network' not in scan_data['scan_categories']:
            no_data_label = tk.Label(content, text="Данные о сетевых настройках не собраны",
                                   font=('Inter', 14), bg=self.colors['background'], fg=self.colors['text'])
            no_data_label.pack(pady=20)
            return
        
        network_data = scan_data['scan_categories']['network']
        
        network_card = tk.Frame(content, bg=self.colors['card'], padx=16, pady=16)
        network_card.pack(fill='x', pady=(0, 16))
        
        network_title = tk.Label(network_card, text="🌐 Сетевые интерфейсы",
                               font=('Inter', 18, 'bold'),
                               bg=self.colors['card'], fg=self.colors['text'])
        network_title.pack(anchor='w', pady=(0, 10))
        
        if 'interfaces' in network_data:
            for interface in network_data['interfaces']:
                interface_name = interface.get('name', 'Неизвестный интерфейс')
                self.create_info_row(network_card, f"Интерфейс {interface_name}", "")
                
                if 'addresses' in interface:
                    for addr in interface['addresses']:
                        addr_info = f"{addr.get('family', '')}: {addr.get('address', '')}"
                        self.create_info_row(network_card, "  Адрес", addr_info, indent=20)
    
    def show_export_tab(self, scan_data):
        content = self.create_scrollable_frame(self.content_frame)
        
        export_card = tk.Frame(content, bg=self.colors['card'], padx=16, pady=16)
        export_card.pack(fill='x', pady=(0, 16))
        
        export_title = tk.Label(export_card, text="📤 Экспорт данных",
                          font=('Inter', 18, 'bold'),
                          bg=self.colors['card'], fg=self.colors['text'])
        export_title.pack(anchor='w', pady=(0, 20))
        
        format_section = tk.Frame(export_card, bg=self.colors['card'])
        format_section.pack(fill='x', pady=(0, 20))
        
        format_label = tk.Label(format_section, text="Формат экспорта:",
                          font=('Inter', 12, 'bold'),
                          bg=self.colors['card'], fg=self.colors['text'])
        format_label.pack(anchor='w', pady=(0, 10))
        
        self.export_format = tk.StringVar(value="json")
        
        radio_frame = tk.Frame(format_section, bg=self.colors['card'])
        radio_frame.pack(fill='x')
        
        def create_radio_option(parent, text, value):
            radio_container = tk.Frame(parent, bg=self.colors['border'], relief='solid', 
                                 borderwidth=1)
            radio_container.pack(fill='x', pady=5)
            
            inner_frame = tk.Frame(radio_container, bg=self.colors['card'])
            inner_frame.pack(fill='x', padx=1, pady=1)
            
            radio_btn = tk.Radiobutton(inner_frame, variable=self.export_format, 
                                 value=value, bg=self.colors['card'], 
                                 activebackground=self.colors['card'],
                                 selectcolor=self.colors['primary'])
            radio_btn.pack(side='left', padx=16, pady=16)
            
            text_label = tk.Label(inner_frame, text=text, 
                            font=('Inter', 12, 'bold'),
                            bg=self.colors['card'], fg=self.colors['text'])
            text_label.pack(side='left', fill='x', expand=True)
            
            def update_style(*args):
                if self.export_format.get() == value:
                    inner_frame.configure(bg=self.colors['primary'])
                    text_label.configure(bg=self.colors['primary'], fg='white')
                    radio_btn.configure(bg=self.colors['primary'], activebackground=self.colors['primary'])
                else:
                    inner_frame.configure(bg=self.colors['card'])
                    text_label.configure(bg=self.colors['card'], fg=self.colors['text'])
                    radio_btn.configure(bg=self.colors['card'], activebackground=self.colors['card'])
            
            self.export_format.trace('w', update_style)
            update_style()
            
            def select_radio(event):
                self.export_format.set(value)
            
            radio_container.bind('<Button-1>', select_radio)
            inner_frame.bind('<Button-1>', select_radio)
            text_label.bind('<Button-1>', select_radio)
            
            return radio_container
        
        json_option = create_radio_option(radio_frame, "JSON", "json")
        xml_option = create_radio_option(radio_frame, "XML", "xml")
        
        path_section = tk.Frame(export_card, bg=self.colors['card'])
        path_section.pack(fill='x', pady=(0, 20))
        
        path_label = tk.Label(path_section, text="Сохранить в:",
                        font=('Inter', 12, 'bold'),
                        bg=self.colors['card'], fg=self.colors['text'])
        path_label.pack(anchor='w', pady=(0, 10))
        
        path_input_frame = tk.Frame(path_section, bg=self.colors['card'])
        path_input_frame.pack(fill='x')
        
        self.export_path = tk.StringVar()
        self.update_default_export_path()
        
        path_entry = tk.Entry(path_input_frame, textvariable=self.export_path,
                         font=('Inter', 11), relief='solid', borderwidth=1,
                         bg=self.colors['background'], fg=self.colors['text'],
                         insertbackground=self.colors['text'],
                         selectbackground=self.colors['primary'])
        path_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        browse_btn = tk.Button(path_input_frame, text="📁", 
                          font=('Inter', 12),
                          bg=self.colors['button_bg'],
                          fg=self.colors['text'],
                          relief='flat', border=0,
                          cursor='hand2',
                          command=self.browse_export_directory)
        browse_btn.pack(side='right', padx=(10, 0), ipadx=12, ipady=8)
        
        buttons_frame = tk.Frame(export_card, bg=self.colors['card'])
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        buttons_container = tk.Frame(buttons_frame, bg=self.colors['card'])
        buttons_container.pack(fill='x')
        
        cancel_btn = tk.Button(buttons_container, text="Отмена",
                          bg=self.colors['button_bg'],
                          fg=self.colors['text'],
                          font=('Inter', 12, 'bold'),
                          relief='flat',
                          border=0,
                          cursor='hand2',
                          command=lambda: self.show_tab_content("hardware", self.scan_data))
        cancel_btn.pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=12)
        
        export_btn = tk.Button(buttons_container, text="Экспортировать",
                          bg=self.colors['primary'],
                          fg='white',
                          font=('Inter', 12, 'bold'),
                          relief='flat',
                          border=0,
                          cursor='hand2',
                          command=lambda: self.perform_export(scan_data))
        export_btn.pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=12)
        
        def update_path_on_format_change(*args):
            self.update_default_export_path()
        
        self.export_format.trace('w', update_path_on_format_change)
    
    def update_default_export_path(self):
        import os
        from datetime import datetime
        
        home_dir = os.path.expanduser("~")
        documents_dir = os.path.join(home_dir, "Documents")
        
        if not os.path.exists(documents_dir):
            documents_dir = home_dir
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        format_ext = "json" if self.export_format.get() == "json" else "xml"
        filename = f"system_info_{timestamp}.{format_ext}"
        
        default_path = os.path.join(documents_dir, filename)
        self.export_path.set(default_path)
    
    def browse_export_directory(self):
        from tkinter import filedialog
        import os
        
        current_path = self.export_path.get()
        initial_dir = os.path.dirname(current_path) if current_path else os.path.expanduser("~")
        
        file_ext = "*.json" if self.export_format.get() == "json" else "*.xml"
        file_types = [
            ("JSON files", "*.json") if self.export_format.get() == "json" else ("XML files", "*.xml"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Сохранить как",
            initialdir=initial_dir,
            initialfile=os.path.basename(current_path),
            defaultextension=f".{self.export_format.get()}",
            filetypes=file_types
        )
        
        if filename:
            self.export_path.set(filename)
    
    def perform_export(self, scan_data):
        try:
            export_path = self.export_path.get().strip()
            
            if not export_path:
                messagebox.showerror("Ошибка", "Укажите путь для сохранения файла")
                return
            
            format_type = self.export_format.get()
            
            if format_type == 'json':
                result = self.exporter.export_json(scan_data, export_path)
            else:
                result = self.exporter.export_xml(scan_data, export_path)
            
            if result['success']:
                messagebox.showinfo("Успех", f"Данные успешно экспортированы в:\n{result['filename']}")
                self.show_tab_content("hardware", self.scan_data)
            else:
                messagebox.showerror("Ошибка", f"Ошибка при экспорте:\n{result['error']}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте:\n{str(e)}")
    
    def create_info_row(self, parent, label, value, indent=0):
        row_frame = tk.Frame(parent, bg=self.colors['card'])
        row_frame.pack(fill='x', pady=8)
        
        label_label = tk.Label(row_frame, text=label,
                             font=('Inter', 12),
                             bg=self.colors['card'], fg=self.colors['secondary_text'])
        label_label.pack(side='left', padx=(indent, 20))
        
        value_label = tk.Label(row_frame, text=value,
                             font=('Inter', 12),
                             bg=self.colors['card'], fg=self.colors['text'])
        value_label.pack(side='left', fill='x', expand=True)
    
    def create_disk_row(self, parent, name, size, free):
        row_frame = tk.Frame(parent, bg=self.colors['card'])
        row_frame.pack(fill='x', pady=8)
        
        name_label = tk.Label(row_frame, text=name,
                            font=('Inter', 12, 'bold'),
                            bg=self.colors['card'], fg=self.colors['text'])
        name_label.pack(side='left', padx=(0, 20))
        
        size_label = tk.Label(row_frame, text=size,
                            font=('Inter', 12),
                            bg=self.colors['card'], fg=self.colors['secondary_text'])
        size_label.pack(side='left', padx=(0, 20))
        
        free_label = tk.Label(row_frame, text=free,
                            font=('Inter', 12),
                            bg=self.colors['card'], fg=self.colors['secondary_text'])
        free_label.pack(side='left')
    
    def create_scrollable_frame(self, parent):
        container = tk.Frame(parent, bg=self.colors['background'])
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(
            container,
            bg=self.colors['background'],
            highlightthickness=0
        )
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(
            container,
            orient='vertical',
            command=canvas.yview
        )
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        holder = tk.Frame(canvas, bg=self.colors['background'])
        canvas_window = canvas.create_window((0, 0), window=holder, anchor='n', width=canvas.winfo_width())

        def resize_holder(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", resize_holder)

        inner_frame = tk.Frame(holder, bg=self.colors['background'])
        inner_frame.pack(fill='x', expand=True, anchor='n')

        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", update_scroll_region)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return inner_frame
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()