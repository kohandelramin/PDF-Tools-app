# pattern_matcher.py

import os
import threading
import pandas as pd
from tkinter import filedialog, messagebox
import customtkinter as ctk


class PatternFinderTab:
    def __init__(self, parent):
        self.build_ui(parent)

    def build_ui(self, parent):
        def browse_pattern_file():
            file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
            if file_path:
                entry_pattern_source.delete(0, "end")
                entry_pattern_source.insert(0, file_path)

        def browse_qr_file():
            file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if file_path:
                entry_qr_code.delete(0, "end")
                entry_qr_code.insert(0, file_path)

        def browse_output_file():
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
            if file_path:
                entry_output_path.delete(0, "end")
                entry_output_path.insert(0, file_path)

        def process_pattern():
            btn_execute.configure(state="disabled")
            btn_browse1.configure(state="disabled")
            btn_browse2.configure(state="disabled")
            btn_browse3.configure(state="disabled")
            status_label.configure(text="⏳ Matching patterns...")
            try:
                mode = mode_var.get()
                pattern_source_file = entry_pattern_source.get()
                qr_code_file = entry_qr_code.get()
                save_path = entry_output_path.get()

                if not pattern_source_file or not qr_code_file or not save_path:
                    messagebox.showerror("Missing Information", "Please select all required files.")
                    return

                pattern_source_df = pd.read_excel(pattern_source_file)
                qr_code_df = pd.read_csv(qr_code_file)
                output_df = []

                if mode == "Auto":
                    pattern_column = pattern_source_df.iloc[:, 3].astype(str).str.strip()
                    for i, row in qr_code_df.iterrows():
                        raw_code = str(row[1]).strip()
                        processed_pattern = raw_code[3:16].strip()
                        matched = pattern_source_df[pattern_column == processed_pattern]
                        if not matched.empty:
                            output_df.append({
                                "Image Path": raw_code,
                                "Processed Pattern": processed_pattern,
                                "Brand": matched.iloc[0, 0],
                                "Pattern": matched.iloc[0, 1],
                                "Size": matched.iloc[0, 2],
                                "Notes": ""
                            })
                        else:
                            output_df.append({
                                "Image Path": raw_code,
                                "Processed Pattern": processed_pattern,
                                "Brand": "",
                                "Pattern": "",
                                "Size": "",
                                "Notes": "pattern not found"
                            })

                elif mode == "Scanner":
                    pattern_column = pattern_source_df.iloc[:, 3].astype(str).str.strip()
                    for i, row in qr_code_df.iterrows():
                        barcode = str(row[4]).strip()
                        if barcode.startswith("01"):
                            processed = barcode[3:16]
                        else:
                            processed = barcode[:14]
                        processed = processed.strip()
                        matched = pattern_source_df[pattern_column == processed]
                        if not matched.empty:
                            output_df.append({
                                "Raw Value": barcode,
                                "Processed Barcode": processed,
                                "Brand": matched.iloc[0, 0],
                                "Pattern": matched.iloc[0, 1],
                                "Size": matched.iloc[0, 2],
                                "Notes": ""
                            })
                        else:
                            output_df.append({
                                "Raw Value": barcode,
                                "Processed Barcode": processed,
                                "Brand": "",
                                "Pattern": "",
                                "Size": "",
                                "Notes": "pattern not found"
                            })

                if not output_df:
                    status_label.configure(text="⚠️ No matches found.")
                    messagebox.showwarning("No Matches", "No matching patterns found.")
                    return

                pd.DataFrame(output_df).to_excel(save_path, index=False)
                status_label.configure(text=f"✅ Done! File saved to: {save_path}")

            except Exception as e:
                status_label.configure(text=f"❌ Error: {str(e)}")

            finally:
                btn_execute.configure(state="normal")
                btn_browse1.configure(state="normal")
                btn_browse2.configure(state="normal")
                btn_browse3.configure(state="normal")

        frame = ctk.CTkFrame(parent)
        frame.pack(pady=20, padx=20, expand=True)

        mode_var = ctk.StringVar(value="Auto")
        mode_selector = ctk.CTkSegmentedButton(frame, values=["Auto", "Scanner"], variable=mode_var)
        mode_selector.pack(pady=10)

        ctk.CTkLabel(frame, text="Pattern Source File (.xlsx)").pack(anchor="w", pady=(10, 0))
        row1 = ctk.CTkFrame(frame)
        row1.pack(fill="x", pady=5)
        entry_pattern_source = ctk.CTkEntry(row1, width=300)
        entry_pattern_source.pack(side="left", padx=(0, 5))
        btn_browse1 = ctk.CTkButton(row1, text="Browse", command=browse_pattern_file)
        btn_browse1.pack(side="right")

        ctk.CTkLabel(frame, text="QR Code Export File (.csv)").pack(anchor="w", pady=(10, 0))
        row2 = ctk.CTkFrame(frame)
        row2.pack(fill="x", pady=5)
        entry_qr_code = ctk.CTkEntry(row2, width=300)
        entry_qr_code.pack(side="left", padx=(0, 5))
        btn_browse2 = ctk.CTkButton(row2, text="Browse", command=browse_qr_file)
        btn_browse2.pack(side="right")

        ctk.CTkLabel(frame, text="Output Excel File").pack(anchor="w", pady=(10, 0))
        row3 = ctk.CTkFrame(frame)
        row3.pack(fill="x", pady=5)
        entry_output_path = ctk.CTkEntry(row3, width=300)
        entry_output_path.pack(side="left", padx=(0, 5))
        btn_browse3 = ctk.CTkButton(row3, text="Browse", command=browse_output_file)
        btn_browse3.pack(side="right")

        btn_execute = ctk.CTkButton(frame, text="Execute", command=process_pattern)
        btn_execute.pack(pady=20)

        status_label = ctk.CTkLabel(frame, text="", text_color="gray")
        status_label.pack(pady=(10, 0))
