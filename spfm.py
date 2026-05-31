import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os
import shutil


# ========== COLOR THEME ==========
# bg #2a214a (dark purple)
# mg #303078 (medium blue-purple)
# other #0055ff (bright blue)
# important #ffc800 (gold/yellow)

# Set appearance mode and colors
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Custom color mappings
BG_COLOR = "#2a214a"
MG_COLOR = "#303078"
OTHER_COLOR = "#0055ff"
IMPORTANT_COLOR = "#ffc800"


# ========== HANDWRITE PATH FINDER ==========
def get_handwrite_path():
    """Find handwrite executable anywhere on the system"""

    # Method 1: Check if it's in PATH (most common)
    handwrite_in_path = shutil.which('handwrite')
    if handwrite_in_path:
        return handwrite_in_path

    # Method 2: Search common locations
    search_paths = [
        os.path.expanduser('~/Desktop/sp-font-maker/.venv/bin/handwrite'),
        os.path.expanduser('~/Desktop/sp-font-maker/venv/bin/handwrite'),
        './.venv/bin/handwrite',
        './venv/bin/handwrite',
        '../.venv/bin/handwrite',
        '../venv/bin/handwrite',
        '/usr/local/bin/handwrite',
        '/opt/homebrew/bin/handwrite',
    ]

    for path in search_paths:
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded) and os.access(expanded, os.X_OK):
            return expanded

    raise FileNotFoundError(
        "❌ Could not find 'handwrite' executable.\n\n"
        "Please install SP Font Maker first:\n"
        "  cd ~/Desktop/sp-font-maker\n"
        "  pip install -e .[dev]"
    )


# ========== CUSTOM WORDS INPUT CLASS ==========
class CustomWordsInput:
    def __init__(self, parent, user_image_path, num_slots=25):
        self.parent = parent
        self.num_slots = num_slots
        self.slot_entries = []

        # Configure parent window colors
        parent.configure(fg_color=BG_COLOR)

        # Create scrollable frame with custom colors
        self.canvas = ctk.CTkScrollableFrame(
            parent,
            width=1000,
            height=600,
            fg_color=BG_COLOR,
            border_color=MG_COLOR,
            border_width=2
        )
        self.canvas.pack(pady=10, padx=10, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            self.canvas,
            text="o nimi e nimi sin sina",
            font=("DIN Alternate", 20, "bold"),
            text_color=IMPORTANT_COLOR
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Instructions
        instructions = ctk.CTkLabel(
            self.canvas,
            text="o lukin e lipu SINA lon poka pilin e lipu nanpa lon poka ante.\n o nimi e nimi sin e sitelen sina. o nimi ala e ijo weka. ona li kama _.",
            font=("DIN Alternate", 12),
            wraplength=900,
            text_color=OTHER_COLOR
        )
        instructions.grid(row=1, column=0, columnspan=2, pady=5)

        # === LEFT COLUMN: User's scanned image (CROPPED TO BOTTOM) ===
        user_frame = ctk.CTkFrame(
            self.canvas,
            fg_color=MG_COLOR,
            border_color=OTHER_COLOR,
            border_width=2
        )
        user_frame.grid(row=2, column=0, padx=10, pady=10, sticky="n")

        user_label_title = ctk.CTkLabel(
            user_frame,
            text="nimi sina",
            font=("DIN Alternate", 14, "bold"),
            text_color=IMPORTANT_COLOR
        )
        user_label_title.pack(pady=5)

        try:
            user_img = Image.open(user_image_path)

            # Crop to bottom 2/5 of the image (40% from bottom)
            width, height = user_img.size
            crop_top = int(height * 0.6)  # Start at 60% down (keep bottom 40%)
            crop_bottom = height
            cropped_img = user_img.crop((0, crop_top, width, crop_bottom))

            # Resize for display
            cropped_img.thumbnail((450, 300))
            user_ctk_img = ctk.CTkImage(light_image=cropped_img, dark_image=cropped_img,
                                        size=(cropped_img.width, cropped_img.height))
            user_image_label = ctk.CTkLabel(user_frame, image=user_ctk_img, text="")
            user_image_label.pack(pady=5)
            user_image_label.image = user_ctk_img

        except Exception as e:
            error_label = ctk.CTkLabel(user_frame, text=f"Could not load image: {e}")
            error_label.pack()

        # === RIGHT COLUMN: Numbered reference image ===
        ref_frame = ctk.CTkFrame(
            self.canvas,
            fg_color=MG_COLOR,
            border_color=OTHER_COLOR,
            border_width=2
        )
        ref_frame.grid(row=2, column=1, padx=10, pady=10, sticky="n")

        ref_label_title = ctk.CTkLabel(
            ref_frame,
            text="nimi pona",
            font=("DIN Alternate", 14, "bold"),
            text_color=IMPORTANT_COLOR
        )
        ref_label_title.pack(pady=5)

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ref_img_path = os.path.join(script_dir, "numbered_custom_slots.png")
            if os.path.exists(ref_img_path):
                ref_img = Image.open(ref_img_path)
                ref_img.thumbnail((450, 450))
                ref_ctk_img = ctk.CTkImage(light_image=ref_img, dark_image=ref_img,
                                           size=(ref_img.width, ref_img.height))
                ref_image_label = ctk.CTkLabel(ref_frame, image=ref_ctk_img, text="")
                ref_image_label.pack(pady=5)
                ref_image_label.image = ref_ctk_img
            else:
                missing_label = ctk.CTkLabel(
                    ref_frame,
                    text="⚠️ numbered_custom_slots.png not found\n\nPlease place this file in the app folder.",
                    text_color="red"
                )
                missing_label.pack()
        except Exception as e:
            error_label = ctk.CTkLabel(ref_frame, text=f"Error loading reference: {e}")
            error_label.pack()

        # === INPUT GRID (below both images) ===
        input_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        input_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")

        input_title = ctk.CTkLabel(
            input_frame,
            text="o pana e nimi pi nimi sin lon lipu:",
            font=("DIN Alternate", 16, "bold"),
            text_color=IMPORTANT_COLOR
        )
        input_title.pack()

        # Custom layout: right-aligned rows
        slot_layout = [
            [1, 2],
            [3, 4, 5, 6, 7, 8, 9, 10, 11],
            [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        ]

        grid_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        grid_container.pack(pady=10)

        for row_slots in slot_layout:
            row_frame = ctk.CTkFrame(grid_container, fg_color="transparent")
            row_frame.pack(anchor="e", pady=1)

            for slot_num in row_slots:
                slot_frame = ctk.CTkFrame(
                    row_frame,
                    width=75,
                    height=70,
                    fg_color=MG_COLOR,
                    border_color=OTHER_COLOR,
                    border_width=1
                )
                slot_frame.pack(side="left", padx=0, pady=0)
                slot_frame.pack_propagate(False)

                num_label = ctk.CTkLabel(
                    slot_frame,
                    text=f"{slot_num}",
                    font=("DIN Alternate", 14, "bold"),
                    text_color=IMPORTANT_COLOR
                )
                num_label.pack(pady=1)

                entry = ctk.CTkEntry(
                    slot_frame,
                    width=70,
                    placeholder_text="nimi",
                    fg_color=BG_COLOR,
                    border_color=OTHER_COLOR,
                    text_color="white"
                )
                entry.pack(pady=1)
                self.slot_entries.append(entry)

    def get_other_words_string(self):
        """Build the --other-words string from user inputs"""
        words = []
        for entry in self.slot_entries:
            word = entry.get().strip()
            words.append(word if word else "_")
        return " ".join(words)


# ========== MAIN APP CLASS ==========
class SPFontMaker:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("lipu - SP Font Maker")
        self.window.geometry("800x900")
        self.window.configure(fg_color=BG_COLOR)

        # Variables
        self.image_path = None
        self.custom_words_string = None

        # Title
        title = ctk.CTkLabel(
            self.window,
            text="lipu SPFM",
            font=("DIN Alternate", 32, "bold"),
            text_color=IMPORTANT_COLOR
        )
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(
            self.window,
            text="tan jan Maku",
            font=("DIN Alternate", 14),
            text_color=OTHER_COLOR
        )
        subtitle.pack()

        # Import Button
        self.import_btn = ctk.CTkButton(
            self.window,
            text="o luka e lipu nimi sina",
            command=self.import_image,
            height=50,
            font=("DIN Alternate", 16),
            fg_color=OTHER_COLOR,
            hover_color=MG_COLOR,
            text_color="white"
        )
        self.import_btn.pack(pady=20)

        # Image Preview
        self.preview_label = ctk.CTkLabel(
            self.window,
            text="sitelen li lon ala",
            fg_color=MG_COLOR,
            corner_radius=10,
            width=147,
            height=200
        )
        self.preview_label.pack(pady=10)

        # Font Name
        name_label = ctk.CTkLabel(
            self.window,
            text="Font Name:",
            text_color=IMPORTANT_COLOR
        )
        name_label.pack()
        self.font_name = ctk.CTkEntry(
            self.window,
            width=400,
            placeholder_text="nimi nasin",
            fg_color=MG_COLOR,
            border_color=OTHER_COLOR,
            text_color="white"
        )
        self.font_name.pack(pady=5)

        # Designer Name
        designer_label = ctk.CTkLabel(
            self.window,
            text="Designer:",
            text_color=IMPORTANT_COLOR
        )
        designer_label.pack()
        self.designer = ctk.CTkEntry(
            self.window,
            width=400,
            placeholder_text="nimi mama",
            fg_color=MG_COLOR,
            border_color=OTHER_COLOR,
            text_color="white"
        )
        self.designer.pack(pady=5)

        # License
        self.license_var = ctk.StringVar(value="OFL")
        license_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        license_frame.pack(pady=10)
        ctk.CTkLabel(
            license_frame,
            text="License:",
            text_color=IMPORTANT_COLOR
        ).pack(side="left", padx=10)
        ctk.CTkRadioButton(
            license_frame,
            text="OFL (Open Font License)",
            variable=self.license_var,
            value="OFL",
            fg_color=OTHER_COLOR,
            hover_color=MG_COLOR
        ).pack(side="left", padx=5)
        ctk.CTkRadioButton(
            license_frame,
            text="CC0 (Public Domain)",
            variable=self.license_var,
            value="CC0",
            fg_color=OTHER_COLOR,
            hover_color=MG_COLOR
        ).pack(side="left", padx=5)

        # Map Custom Words Button
        self.map_btn = ctk.CTkButton(
            self.window,
            text="o nimi e nimi sin",
            command=self.show_custom_input,
            height=40,
            font=("DIN Alternate", 14),
            fg_color=OTHER_COLOR,
            hover_color=MG_COLOR,
            text_color="white"
        )
        self.map_btn.pack(pady=10)

        # Generate Button
        self.generate_btn = ctk.CTkButton(
            self.window,
            text="o pali e nasin!",
            command=self.generate_font,
            height=50,
            font=("DIN Alternate", 18),
            fg_color=IMPORTANT_COLOR,
            hover_color=OTHER_COLOR,
            text_color=BG_COLOR
        )
        self.generate_btn.pack(pady=20)

        # Progress Text Box
        self.progress = ctk.CTkTextbox(
            self.window,
            height=150,
            width=700,
            fg_color=MG_COLOR,
            border_color=OTHER_COLOR,
            border_width=2,
            text_color="white"
        )
        self.progress.pack(pady=10)

        self.window.mainloop()

    def import_image(self):
        path = filedialog.askopenfilename(
            title="Select your scanned template",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if path:
            self.image_path = path
            self.progress.insert("end", f"✅ Loaded: {os.path.basename(path)}\n")
            self.progress.see("end")

            # Show preview
            try:
                img = Image.open(path)
                img.thumbnail((147, 200))
                ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(147, 200))
                self.preview_label.configure(image=ctk_image, text="")
                self.preview_label.image = ctk_image
            except:
                self.preview_label.configure(text="Preview not available")

    def show_custom_input(self):
        """Show the window for mapping custom words"""
        if not self.image_path:
            messagebox.showinfo("Info", "Please import an image first!")
            return

        # Create new window
        input_window = ctk.CTkToplevel(self.window)
        input_window.title("o nimi e nimi sin")
        input_window.geometry("1200x800")
        input_window.configure(fg_color=BG_COLOR)

        # Create the input grid with user's image path
        self.custom_input = CustomWordsInput(input_window, self.image_path, num_slots=25)

        # Save button
        save_btn = ctk.CTkButton(
            input_window,
            text="o awen e nimi o pini e lipu",
            command=lambda: self.save_custom_words(input_window),
            height=40,
            fg_color=IMPORTANT_COLOR,
            hover_color=OTHER_COLOR,
            text_color=BG_COLOR
        )
        save_btn.pack(pady=10)

    def save_custom_words(self, input_window):
        """Save custom words and close window"""
        other_words = self.custom_input.get_other_words_string()
        self.custom_words_string = other_words
        input_window.destroy()
        self.progress.insert("end", f"✅ nimi sin li awen.\n")
        self.progress.insert("end", f"📝 nimi sin: {other_words}\n")

    def generate_font(self):
        if not self.image_path:
            messagebox.showerror("Error", "nanpa wan la o pana e sitelen!")
            return

        name = self.font_name.get()
        designer = self.designer.get()

        if not name:
            name = "MyFont"
        if not designer:
            designer = "Unknown"

        license_map = {"OFL": "ofl", "CC0": "cc0"}
        license_val = license_map.get(self.license_var.get(), "ofl")

        handwrite_path = get_handwrite_path()

        cmd = [
            handwrite_path,
            self.image_path,
            os.path.expanduser("~/Desktop"),
            "--filename", name,
            "--designer", designer,
            "--license", license_val,
            "--not-new"
        ]

        # Use custom words from input if available
        if self.custom_words_string:
            cmd.extend(["--other-words", self.custom_words_string])

        self.progress.insert("end", f"\n🔨 mi pali e nasin '{name}'...\n")
        self.progress.see("end")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout:
                self.progress.insert("end", result.stdout)
            if result.stderr:
                self.progress.insert("end", f"⚠️ {result.stderr}\n")
            self.progress.insert("end", f"\n✅ Font saved to Desktop as {name}.ttf\n")
            self.progress.see("end")
            messagebox.showinfo("Success", f"Font '{name}' created on your Desktop!")
        except Exception as e:
            self.progress.insert("end", f"❌ Error: {e}\n")
            messagebox.showerror("Error", f"Generation failed: {e}")


# Run the app
if __name__ == "__main__":
    app = SPFontMaker()