"""
Disease Prediction System GUI
----------------------------
A graphical user interface for predicting diseases based on symptoms using machine learning.
Features:
- Interactive symptom selection
- Real-time search filtering
- Confidence visualization
- Disease descriptions and precautions
- Model retraining capability
- Patient prediction history
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pickle
import numpy as np
import os
import pandas as pd
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import PatientDatabase
from datetime import datetime

class DiseasePredictionGUI:
    def __init__(self, root):
        # Configure main window
        self.root = root
        self.root.title("Disease Prediction System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')
        
        # Initialize database
        self.db = PatientDatabase()
        
        # Initialize core components
        self.load_descriptions()
        self.setup_styles()
        self.load_model()
        
    def load_descriptions(self):
        try:
            self.descriptions = pd.read_csv('symptom_Description.csv')
            self.precautions = pd.read_csv('symptom_precaution.csv')
        except:
            self.descriptions = None
            self.precautions = None
    
    def setup_styles(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.style = ttk.Style()
        self.style.configure('Main.TFrame', background='#1e1e2e')
        
    def load_model(self):
        try:
            with open('disease_model.pkl', 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.label_encoder = data['label_encoder']
                self.symptoms = data['symptoms']
            self.create_main_interface()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {str(e)}")
            
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
        
        for i, symptom in enumerate(self.symptoms):
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
    
    def filter_symptoms(self, *args):
        self.create_symptom_buttons()
    
    def predict(self):
        if not self.name_var.get().strip():
            messagebox.showwarning("Warning", "Please enter patient name")
            return
            
        selected_symptoms = [s for s, v in self.symptom_vars.items() if v.get()]
        
        if not selected_symptoms:
            messagebox.showwarning("Warning", "Please select at least one symptom")
            return
        
        X = np.zeros(len(self.symptoms))
        for symptom in selected_symptoms:
            idx = self.symptoms.index(symptom)
            X[idx] = 1
        
        try:
            prediction = self.model.predict([X])
            probability = self.model.predict_proba([X]).max()
            disease = self.label_encoder.inverse_transform(prediction)[0]
            
            # Store prediction with patient info
            patient_info = {
                'name': self.name_var.get(),
                'age': self.age_var.get(),
                'gender': self.gender_var.get()
            }
            self.db.add_prediction(disease, probability, selected_symptoms, patient_info)
            
            self.result_label.configure(
                text=f"Predicted Disease: {disease}\nConfidence: {probability*100:.2f}%")
            
            self.update_disease_info(disease)
                        
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Error making prediction: {str(e)}")
    
    def show_history(self):
        history_window = ctk.CTkToplevel(self.root)
        history_window.title("Prediction History")
        history_window.geometry("800x600")
        history_window.configure(fg_color='#1e1e2e')
        
        history_frame = ctk.CTkScrollableFrame(history_window,
                                             fg_color='#313244',
                                             width=750,
                                             height=550)
        history_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        predictions = self.db.get_all_predictions()
        
        for pred in predictions:
            pred_frame = ctk.CTkFrame(history_frame, fg_color='#1e1e2e')
            pred_frame.pack(fill='x', pady=5, padx=10)
            
            patient_info = eval(pred[5]) if pred[5] else {}
            
            info_text = f"Patient: {patient_info.get('name', 'N/A')}\n"
            info_text += f"Age: {patient_info.get('age', 'N/A')} | "
            info_text += f"Gender: {patient_info.get('gender', 'N/A')}\n"
            info_text += f"Time: {pred[1].split('.')[0]}\n"
            info_text += f"Disease: {pred[2]}\n"
            info_text += f"Confidence: {pred[3]*100:.2f}%\n"
            info_text += f"Symptoms: {pred[4]}"
            
            label = ctk.CTkLabel(pred_frame,
                               text=info_text,
                               font=('Helvetica', 12),
                               text_color='#cdd6f4',
                               justify='left')
            label.pack(pady=10, padx=10)
    
    def clear_selection(self):
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("Male")
        for var in self.symptom_vars.values():
            var.set(False)
        self.result_label.configure(text="Select symptoms and click Predict")
        self.description_label.configure(text="Disease description will appear here")
        for label in self.precautions_labels:
            label.configure(text="")
    
    def update_disease_info(self, disease):
        if self.descriptions is not None:
            description = self.descriptions[
                self.descriptions['Disease'] == disease]['Description'].values
            if len(description) > 0:
                self.description_label.configure(text=description[0])
            else:
                self.description_label.configure(text="No description available")
        
        if self.precautions is not None:
            precaution_row = self.precautions[self.precautions['Disease'] == disease]
            if not precaution_row.empty:
                for i, label in enumerate(self.precautions_labels):
                    precaution = precaution_row[f'Precaution_{i+1}'].values[0]
                    label.configure(text=f"{i+1}. {precaution}")
            else:
                for label in self.precautions_labels:
                    label.configure(text="")

if __name__ == "__main__":
    root = ctk.CTk()
    app = DiseasePredictionGUI(root)
    root.mainloop()