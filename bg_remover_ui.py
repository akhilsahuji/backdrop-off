import os
import threading
import subprocess
import platform
from rembg import remove
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser


class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backdrop-Off - Background Remover")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Variables
        self.input_folder = ""
        self.output_folder = ""
        self.worker_thread = None
        self.total_images = 0
        self.processed_images = 0
        self.background_color = (255, 255, 255)  # Default white background

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.root, text="Background Remover", font=("Arial", 20, "bold")).pack(pady=10)

        # Input folder selection
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(input_frame, text="Input Folder:", width=100).pack(side="left", padx=5)
        self.input_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter input folder path...")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.input_entry.bind("<KeyRelease>", self.on_input_path_change)
        
        self.input_btn = ctk.CTkButton(input_frame, text="Browse", command=self.select_input_folder, width=80)
        self.input_btn.pack(side="right", padx=5)

        # Output folder selection
        output_frame = ctk.CTkFrame(self.root)
        output_frame.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(output_frame, text="Output Folder:", width=100).pack(side="left", padx=5)
        self.output_entry = ctk.CTkEntry(output_frame, placeholder_text="Enter output folder path...")
        self.output_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.output_entry.bind("<KeyRelease>", self.on_output_path_change)
        
        self.output_btn = ctk.CTkButton(output_frame, text="Browse", command=self.select_output_folder, width=80)
        self.output_btn.pack(side="right", padx=5)

        # Color selection frame
        self.color_frame = ctk.CTkFrame(self.root)
        self.color_frame.pack(pady=10)

        ctk.CTkLabel(self.color_frame, text="Background Color:").pack(side="left", padx=5)
        
        self.color_btn = ctk.CTkButton(self.color_frame, text="Choose Color", command=self.choose_color, width=100)
        self.color_btn.pack(side="left", padx=5)
        
        # Hex code input
        ctk.CTkLabel(self.color_frame, text="Hex:").pack(side="left", padx=(10, 2))
        self.hex_entry = ctk.CTkEntry(self.color_frame, width=80, placeholder_text="#FFFFFF")
        self.hex_entry.pack(side="left", padx=2)
        self.hex_entry.bind("<Return>", self.on_hex_enter)
        self.hex_entry.bind("<FocusOut>", self.on_hex_enter)
        
        self.apply_hex_btn = ctk.CTkButton(self.color_frame, text="Apply", command=self.apply_hex_color, width=60)
        self.apply_hex_btn.pack(side="left", padx=2)
        
        self.color_preview = ctk.CTkLabel(self.color_frame, text="   ", width=30, height=20)
        self.color_preview.pack(side="left", padx=5)
        self.update_color_preview()

        self.start_btn = ctk.CTkButton(self.root, text="Start Processing", command=self.start_processing)
        self.start_btn.pack(pady=10)

        # Open output folder button (initially hidden)
        self.open_folder_btn = ctk.CTkButton(self.root, text="Open Output Folder", command=self.open_output_folder)
        self.open_folder_btn.pack(pady=5)
        self.open_folder_btn.pack_forget()  # Hide initially

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.root, width=400)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        # Progress label
        self.progress_label = ctk.CTkLabel(self.root, text="")
        self.progress_label.pack(pady=5)

        self.status_label = ctk.CTkLabel(self.root, text="")
        self.status_label.pack(pady=10)

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, folder)
            # Count images in the input folder
            image_count = self.count_images(folder)
            self.total_images = image_count
            self.status_label.configure(text=f"Input: {folder} ({image_count} images found)")
            self.progress_bar.set(0)
            self.progress_label.configure(text="")

    def on_input_path_change(self, event):
        """Handle manual input path changes"""
        path = self.input_entry.get().strip()
        if path and os.path.isdir(path):
            self.input_folder = path
            image_count = self.count_images(path)
            self.total_images = image_count
            self.status_label.configure(text=f"Input: {path} ({image_count} images found)")
            self.progress_bar.set(0)
            self.progress_label.configure(text="")
        elif path:
            self.status_label.configure(text="Invalid input path")
        else:
            self.input_folder = ""
            self.total_images = 0

    def count_images(self, folder_path):
        """Count the number of image files in the folder"""
        count = 0
        try:
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    count += 1
        except Exception:
            count = 0
        return count

    def choose_color(self):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title="Choose Background Color", initialcolor=self.background_color)
        if color[0]:  # color[0] is RGB tuple, color[1] is hex string
            self.background_color = tuple(int(c) for c in color[0])
            self.update_color_preview()
            self.update_hex_entry()

    def apply_hex_color(self):
        """Apply color from hex code entry"""
        self.on_hex_enter(None)

    def on_hex_enter(self, event):
        """Handle hex code entry when Enter is pressed or focus is lost"""
        hex_code = self.hex_entry.get().strip()
        if self.is_valid_hex(hex_code):
            try:
                # Remove # if present and convert to RGB
                hex_code = hex_code.lstrip('#')
                self.background_color = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
                self.update_color_preview()
            except ValueError:
                messagebox.showerror("Invalid Color", "Please enter a valid hex color code (e.g., #FF0000 or FF0000)")
        elif hex_code:  # Only show error if something was entered
            messagebox.showerror("Invalid Color", "Please enter a valid hex color code (e.g., #FF0000 or FF0000)")

    def is_valid_hex(self, hex_code):
        """Check if the hex code is valid"""
        if not hex_code:
            return False
        
        # Remove # if present
        hex_code = hex_code.lstrip('#')
        
        # Check if it's exactly 6 characters and all are valid hex digits
        if len(hex_code) == 6:
            try:
                int(hex_code, 16)
                return True
            except ValueError:
                return False
        return False

    def update_hex_entry(self):
        """Update hex entry field with current color"""
        hex_color = "#{:02x}{:02x}{:02x}".format(*self.background_color)
        self.hex_entry.delete(0, "end")
        self.hex_entry.insert(0, hex_color)

    def update_color_preview(self):
        """Update the color preview label"""
        # Convert RGB to hex for display
        hex_color = "#{:02x}{:02x}{:02x}".format(*self.background_color)
        self.color_preview.configure(fg_color=hex_color, text="")

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)
            self.status_label.configure(text=f"Output: {folder}")

    def on_output_path_change(self, event):
        """Handle manual output path changes"""
        path = self.output_entry.get().strip()
        if path and os.path.isdir(path):
            self.output_folder = path
            self.status_label.configure(text=f"Output: {path}")
        elif path:
            self.status_label.configure(text="Invalid output path")
        else:
            self.output_folder = ""

    def start_processing(self):
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Error", "Please select both input and output folders")
            return

        self.status_label.configure(text="Processing started...")
        self.start_btn.configure(state="disabled")
        self.processed_images = 0
        self.progress_bar.set(0)
        self.update_progress_label()
        # Hide the open folder button when starting new processing
        self.open_folder_btn.pack_forget()

        # Start background processing in a thread
        self.worker_thread = threading.Thread(target=self.process_images)
        self.worker_thread.start()

        # Check thread status periodically
        self.root.after(500, self.check_thread)

    def update_progress_label(self):
        """Update the progress label with current progress"""
        if self.total_images > 0:
            percentage = (self.processed_images / self.total_images) * 100
            self.progress_label.configure(text=f"Progress: {self.processed_images}/{self.total_images} images ({percentage:.1f}%)")
        else:
            self.progress_label.configure(text="")

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        if self.output_folder and os.path.exists(self.output_folder):
            try:
                # Cross-platform folder opening
                if platform.system() == "Windows":
                    os.startfile(self.output_folder)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", self.output_folder])
                else:  # Linux and other Unix-like systems
                    subprocess.run(["xdg-open", self.output_folder])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Output folder not found or not set")

    def process_images(self):
        try:
            for file_name in os.listdir(self.input_folder):
                if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    input_path = os.path.join(self.input_folder, file_name)
                    output_path = os.path.join(self.output_folder, os.path.splitext(file_name)[0] + ".jpg")

                    with open(input_path, "rb") as inp:
                        input_bytes = inp.read()

                    # Remove background
                    result = remove(input_bytes)

                    # Save temporary PNG with transparency
                    temp_path = os.path.join(self.output_folder, "temp.png")
                    with open(temp_path, "wb") as out:
                        out.write(result)

                    # Composite on selected background color
                    img = Image.open(temp_path).convert("RGBA")
                    colored_bg = Image.new("RGBA", img.size, (*self.background_color, 255))
                    final_img = Image.alpha_composite(colored_bg, img)
                    final_img.convert("RGB").save(output_path, "JPEG")

                    os.remove(temp_path)  # Cleanup temp file

                    # Update progress
                    self.processed_images += 1
                    if self.total_images > 0:
                        progress_value = self.processed_images / self.total_images
                        # Update UI in main thread
                        self.root.after(0, lambda: self.progress_bar.set(progress_value))
                        self.root.after(0, self.update_progress_label)

            self.root.after(0, lambda: self.status_label.configure(text="Processing completed 🎉"))
            # Show the open folder button when processing is complete
            self.root.after(0, lambda: self.open_folder_btn.pack(pady=5))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.start_btn.configure(state="normal"))

    def check_thread(self):
        if self.worker_thread.is_alive():
            self.root.after(500, self.check_thread)
        else:
            self.status_label.configure(text="Done ✅")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = BackgroundRemoverApp(root)
    root.mainloop()