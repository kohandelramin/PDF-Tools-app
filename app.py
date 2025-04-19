from tabs.page_counter import PageCounterTab
from tabs.datamatrix_extractor import DataMatrixTab
from tabs.pattern_matcher import PatternFinderTab
import customtkinter as ctk

class PDFToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Tools App")
        self.geometry("500x550")
        ctk.set_appearance_mode("dark")

        tab_control = ctk.CTkTabview(self)
        self.tab1 = tab_control.add("Page Counter")
        self.tab2 = tab_control.add("Data Matrix Extractor")
        self.tab3 = tab_control.add("Pattern Finder")
        tab_control.pack(expand=True, fill="both", padx=10, pady=10)

        version_label = ctk.CTkLabel(self, text="Version 3.2.0 - RK Licence", font=("Arial", 10), text_color="gray")
        version_label.pack(side="bottom", pady=(0, 5))

        PageCounterTab(self.tab1)
        DataMatrixTab(self.tab2)
        PatternFinderTab(self.tab3)

if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()