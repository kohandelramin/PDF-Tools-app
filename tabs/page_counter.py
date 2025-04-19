# PageCounterTab logic

import os
from io import BytesIO
from tkinter import filedialog, messagebox
from datetime import datetime
import threading
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import customtkinter as ctk


class PageCounterTab:
    def __init__(self, parent):
        self.build_ui(parent)

    def build_ui(self, parent):
        def select_file():
            file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                entry_input.delete(0, "end")
                entry_input.insert(0, file_path)
                output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_counter.pdf"
                entry_output.delete(0, "end")
                entry_output.insert(0, output_filename)

        def process_pdf():
            btn_process.configure(state="disabled")
            btn_select.configure(state="disabled")
            status_label.configure(text="⏳ Processing...")

            def run_task():
                try:
                    input_path = entry_input.get()
                    output_path = entry_output.get()
                    font_size = int(entry_font_size.get())
                    x_pos = int(entry_x_pos.get())
                    y_pos = int(entry_y_pos.get())
                    start_number = int(entry_start_number.get())
                    pattern_prefix = entry_pattern_prefix.get()

                    input_pdf = PdfReader(input_path)
                    output_pdf = PdfWriter()

                    for i in range(len(input_pdf.pages)):
                        packet = BytesIO()
                        can = canvas.Canvas(packet)
                        can.setFont("Helvetica-Bold", font_size)
                        can.drawString(x_pos, y_pos, f"{pattern_prefix}{start_number + i:05d}")
                        can.save()
                        packet.seek(0)
                        watermark = PdfReader(packet)
                        page = input_pdf.pages[i]
                        page.merge_page(watermark.pages[0])
                        output_pdf.add_page(page)

                    with open(output_path, "wb") as output_file:
                        output_pdf.write(output_file)

                    status_label.configure(text="✅ PDF processed successfully!")
                    messagebox.showinfo("Success", "PDF processed successfully!")

                except Exception as e:
                    status_label.configure(text=f"❌ Error: {str(e)}")
                    messagebox.showerror("Error", str(e))

                finally:
                    btn_process.configure(state="normal")
                    btn_select.configure(state="normal")

            threading.Thread(target=run_task, daemon=True).start()

        frame = ctk.CTkFrame(parent)
        frame.pack(pady=20, padx=20, expand=True)

        input_row = ctk.CTkFrame(frame)
        input_row.pack(pady=5)
        ctk.CTkLabel(input_row, text="Select PDF File").pack(side="left", padx=5)
        entry_input = ctk.CTkEntry(input_row, width=250)
        entry_input.pack(side="left")
        btn_select = ctk.CTkButton(input_row, text="Browse", command=select_file)
        btn_select.pack(side="left", padx=5)

        settings_frame = ctk.CTkFrame(frame)
        settings_frame.pack(pady=5)

        month_number = datetime.now().strftime("%m")

        entry_fields = {}
        for label_text, default_value, var_name in [
            ("Output File Name", "", "entry_output"),
            ("Font Size", "8", "entry_font_size"),
            ("X Position", "5", "entry_x_pos"),
            ("Y Position", "20", "entry_y_pos"),
            ("Starting Number", "1", "entry_start_number"),
            ("Pattern Prefix", month_number, "entry_pattern_prefix")
        ]:
            row = ctk.CTkFrame(settings_frame)
            row.pack(pady=3, fill="x")
            ctk.CTkLabel(row, text=label_text, width=120, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, width=200)
            entry.insert(0, default_value)
            entry.pack(side="right")
            entry_fields[var_name] = entry

        entry_output = entry_fields["entry_output"]
        entry_font_size = entry_fields["entry_font_size"]
        entry_x_pos = entry_fields["entry_x_pos"]
        entry_y_pos = entry_fields["entry_y_pos"]
        entry_start_number = entry_fields["entry_start_number"]
        entry_pattern_prefix = entry_fields["entry_pattern_prefix"]

        btn_process = ctk.CTkButton(frame, text="Add Page Counters", command=process_pdf)
        btn_process.pack(pady=10)

        status_label = ctk.CTkLabel(frame, text="", text_color="gray")
        status_label.pack(pady=(10, 0))
