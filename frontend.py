def create_main_interface(self):
    # Header section
    header_frame = ctk.CTkFrame(self.root, fg_color='#1e1e2e')
    header_frame.pack(fill='x', pady=20)
    
    title = ctk.CTkLabel(header_frame, 
                        text="Disease Prediction System",
                        font=('Helvetica', 32, 'bold'),
                        text_color='#89b4fa')
    title.pack(side='left', padx=30)
    
    # Patient Information Entry
    info_frame = ctk.CTkFrame(self.root, fg_color='#313244')
    info_frame.pack(fill='x', padx=30, pady=10)
    
    # Name Entry
    name_label = ctk.CTkLabel(info_frame, text="Patient Name:", text_color='#cdd6f4')
    name_label.pack(side='left', padx=10)
    self.name_var = tk.StringVar()
    name_entry = ctk.CTkEntry(info_frame, textvariable=self.name_var, width=200)
    name_entry.pack(side='left', padx=10)
    
    # Age Entry
    age_label = ctk.CTkLabel(info_frame, text="Age:", text_color='#cdd6f4')
    age_label.pack(side='left', padx=10)
    self.age_var = tk.StringVar()
    age_entry = ctk.CTkEntry(info_frame, textvariable=self.age_var, width=50)
    age_entry.pack(side='left', padx=10)
    
    # Gender Selection
    gender_label = ctk.CTkLabel(info_frame, text="Gender:", text_color='#cdd6f4')
    gender_label.pack(side='left', padx=10)
    self.gender_var = tk.StringVar(value="Male")
    gender_menu = ctk.CTkOptionMenu(info_frame, 
                                  variable=self.gender_var,
                                  values=["Male", "Female", "Other"])
    gender_menu.pack(side='left', padx=10)
    
    # Symptom Search
    search_frame = ctk.CTkFrame(self.root, fg_color='#313244')
    search_frame.pack(fill='x', padx=30, pady=10)
    
    search_label = ctk.CTkLabel(search_frame,
                              text="Search Symptoms:",
                              text_color='#cdd6f4')
    search_label.pack(side='left', padx=10)
    
    self.search_var = tk.StringVar()
    self.search_var.trace('w', self.filter_symptoms)
    search_entry = ctk.CTkEntry(search_frame,
                              textvariable=self.search_var,
                              width=200)
    search_entry.pack(side='left', padx=10)
    
    # Symptoms selection area
    self.symptoms_frame = ctk.CTkScrollableFrame(self.root, 
                                               label_text="Select Symptoms",
                                               fg_color='#313244',
                                               label_text_color='#cba6f7')
    self.symptoms_frame.pack(fill='x', padx=30, pady=10)
    
    self.symptom_vars = {}
    self.symptom_buttons = {}
    self.create_symptom_buttons()
    
    # Control buttons
    button_frame = ctk.CTkFrame(self.root, fg_color='#1e1e2e')
    button_frame.pack(pady=20)
    
    predict_btn = ctk.CTkButton(button_frame,
                              text="Predict Disease",
                              command=self.predict,
                              fg_color='#89b4fa',
                              hover_color='#74c7ec')
    predict_btn.pack(side='left', padx=10)
    
    history_btn = ctk.CTkButton(button_frame,
                              text="View History",
                              command=self.show_history,
                              fg_color='#89b4fa',
                              hover_color='#74c7ec')
    history_btn.pack(side='left', padx=10)
    
    clear_btn = ctk.CTkButton(button_frame,
                             text="Clear Selection",
                             command=self.clear_selection,
                             fg_color='#f38ba8',
                             hover_color='#eba0ac')
    clear_btn.pack(side='left', padx=10)
    
    # Results section
    self.result_frame = ctk.CTkFrame(self.root, fg_color='#313244')
    self.result_frame.pack(fill='x', padx=30, pady=10)
    
    self.result_label = ctk.CTkLabel(self.result_frame,
                                   text="Select symptoms and click Predict",
                                   font=('Helvetica', 14),
                                   text_color='#cdd6f4')
    self.result_label.pack(pady=20)
    
    # Description and Precautions
    info_frame = ctk.CTkFrame(self.root, fg_color='#313244')
    info_frame.pack(fill='x', padx=30, pady=10)
    
    self.description_label = ctk.CTkLabel(info_frame,
                                        text="Disease description will appear here",
                                        font=('Helvetica', 12),
                                        text_color='#cdd6f4',
                                        wraplength=1100)
    self.description_label.pack(pady=10, padx=10)
    
    self.precautions_frame = ctk.CTkFrame(info_frame, fg_color='#313244')
    self.precautions_frame.pack(fill='x', pady=10)
    
    self.precautions_title = ctk.CTkLabel(self.precautions_frame,
                                        text="Precautions",
                                        font=('Helvetica', 14, 'bold'),
                                        text_color='#cba6f7')
    self.precautions_title.pack(pady=10)
    
    self.precautions_labels = []
    for i in range(4):
        label = ctk.CTkLabel(self.precautions_frame,
                           text="",
                           font=('Helvetica', 12),
                           text_color='#cdd6f4')
        label.pack(pady=5)
        self.precautions_labels.append(label)

def create_symptom_buttons(self):
    for widget in self.symptoms_frame.winfo_children():
        widget.destroy()
    
    symptoms = self.predictor.get_all_symptoms()
    for i, symptom in enumerate(symptoms):
        if self.search_var.get().lower() in symptom.lower():
            var = tk.BooleanVar()
            self.symptom_vars[symptom] = var
            btn = ctk.CTkCheckBox(self.symptoms_frame,
                                text=symptom.replace('_', ' ').title(),
                                variable=var,
                                text_color='#cdd6f4',
                                fg_color='#89b4fa',
                                hover_color='#74c7ec')
            btn.grid(row=i//3, column=i%3, padx=20, pady=10, sticky='w')
            self.symptom_buttons[symptom] = btn

def clear_selection(self):
    for var in self.symptom_vars.values():
        var.set(False)
    self.result_label.configure(text="Select symptoms and click Predict")
    self.description_label.configure(text="Disease description will appear here")
    for label in self.precautions_labels:
        label.configure(text="")