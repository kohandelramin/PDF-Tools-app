# datamatrix_extractor.py

import os
import threading
import tempfile
from tkinter import filedialog, messagebox
import pandas as pd
from pdf2image import convert_from_path
from pylibdmtx import pylibdmtx
import cv2
import customtkinter as ctk


class DataMatrixTab:
    def __init__(self, parent):
        self.build_ui(parent)

    def build_ui(self, parent):
        def browse_pdf():
            file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                entry_pdf.delete(0, "end")
                entry_pdf.insert(0, file_path)

        def browse_output():
            folder_path = filedialog.askdirectory()
            if folder_path:
                entry_output.delete(0, "end")
                entry_output.insert(0, folder_path)

        def pdf_to_images(pdf_file_path, progress_bar, percentage_label, total_pages):
            output_folder = tempfile.mkdtemp()
            image_paths = []
            images = convert_from_path(pdf_file_path, dpi=300)
            for i, image in enumerate(images):
                image_path = os.path.join(output_folder, f"page_{i+1}.png")
                image.save(image_path, "PNG")
                image_paths.append(image_path)
                progress = (i + 1) / total_pages * 100
                progress_bar.set(progress / 100)
                percentage_label.configure(text=f"{int(progress)}%")
            return image_paths

        def decode_data_matrix(image_path):
            image = cv2.imread(image_path)
            decoded = pylibdmtx.decode(image)
            if decoded:
                return decoded[0].data.decode('utf-8')
            return None

        def extract_data_matrix_codes_to_csv(pdf_path, output_path, progress_bar, percentage_label):
            images = convert_from_path(pdf_path)
            total_pages = len(images)
            image_paths = pdf_to_images(pdf_path, progress_bar, percentage_label, total_pages)
            data = []
            for i, image_path in enumerate(image_paths):
                code = decode_data_matrix(image_path)
                if code:
                    data.append([image_path, code])
                progress = (i + 1) / total_pages * 100
                progress_bar.set(progress / 100)
                percentage_label.configure(text=f"{int(progress)}%")
            if data:
                df = pd.DataFrame(data, columns=["Image Path", "Data Matrix Code"])
                pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
                output_file = os.path.join(output_path, f"{pdf_name}.csv")
                df.to_csv(output_file, index=False)

        def start_extraction():
            pdf_file = entry_pdf.get()
            output_dir = entry_output.get()
            if not pdf_file or not output_dir:
                messagebox.showerror("Error", "Please select both PDF file and output folder.")
                return
            btn_start.configure(state="disabled")
            btn_pdf.configure(state="disabled")
            btn_output.configure(state="disabled")
            progress_bar.set(0)
            percentage_label.configure(text="0%")
            status_label.configure(text="⏳ Processing...")
            def run_task():
                try:
                    extract_data_matrix_codes_to_csv(pdf_file, output_dir, progress_bar, percentage_label)
                    status_label.configure(text="✅ Data Matrix extraction completed.")
                    messagebox.showinfo("Success", "Data Matrix extraction completed.")
                except Exception as e:
                    status_label.configure(text=f"❌ Error: {str(e)}")
                    messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
                finally:
                    btn_start.configure(state="normal")
                    btn_pdf.configure(state="normal")
                    btn_output.configure(state="normal")
            threading.Thread(target=run_task, daemon=True).start()

        frame = ctk.CTkFrame(parent)
        frame.pack(pady=20, padx=20, expand=True)

        ctk.CTkLabel(frame, text="PDF File:").pack(anchor="w")
        row1 = ctk.CTkFrame(frame)
        row1.pack(fill="x", pady=5)
        entry_pdf = ctk.CTkEntry(row1, width=300)
        entry_pdf.pack(side="left", padx=(0, 5))
        btn_pdf = ctk.CTkButton(row1, text="Browse", command=browse_pdf)
        btn_pdf.pack(side="right")

        ctk.CTkLabel(frame, text="Output Folder:").pack(anchor="w", pady=(10, 0))
        row2 = ctk.CTkFrame(frame)
        row2.pack(fill="x", pady=5)
        entry_output = ctk.CTkEntry(row2, width=300)
        entry_output.pack(side="left", padx=(0, 5))
        btn_output = ctk.CTkButton(row2, text="Browse", command=browse_output)
        btn_output.pack(side="right")

        btn_start = ctk.CTkButton(frame, text="Start Extraction", command=start_extraction)
        btn_start.pack(pady=(15, 5))

        progress_bar = ctk.CTkProgressBar(frame, width=300)
        progress_bar.set(0)
        progress_bar.pack(pady=5)
        percentage_label = ctk.CTkLabel(frame, text="0%")
        percentage_label.pack()

        status_label = ctk.CTkLabel(frame, text="", text_color="gray")
        status_label.pack(pady=(10, 0))
