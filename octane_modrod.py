import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import sys
import zipfile
import requests
import shutil


class Cars2ModdingTool:
    def __init__(self, root):
        self.decode_textures = None
        self.encode_textures = None
        self.pack_folder = None
        self.encode_output = None
        self.decode_output = None
        self.tabs = None
        self.notebook = None
        self.output_text = None
        self.unluac_entry = None
        self.decrypt_input = None
        self.pack_name = None
        self.encode_input = None
        self.decode_input = None
        self.root = root
        self.root.geometry("800x600")
        self.unluac_path = ""
        self.offsetting_path = ""
        self.load_config()
        if not self.check_initial_setup():
            self.show_install_ui()
        else:
            self.show_main_ui()

    def load_config(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("unluac_path="):
                        self.unluac_path = line.strip().split("=", 1)[1]
                        print(f"Loaded unluac_path: {self.unluac_path}")
        else:
            print("No config.txt found, starting fresh setup")

    def save_config(self):
        with open("config.txt", "w") as f:
            f.write(f"unluac_path={self.unluac_path}\n")
            f.write(f"offsetting_path={self.offsetting_path}\n")
            print(f"Saved config: unluac_path={self.unluac_path}, offsetting_path={self.offsetting_path}")

    def check_initial_setup(self):
        try:
            import c2ditools
            print("c2ditools module found")
            unluac_exists = os.path.exists(self.unluac_path)
            print(f"Checking unluac_path: {self.unluac_path} exists={unluac_exists}")
            return unluac_exists and "c2ditools" in sys.modules
        except ImportError:
            print("c2ditools module not found")
            return False

    def show_install_ui(self):
        self.root.title("Cars 2 Modding Tool - Setup")
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Welcome! Let's set up the modding tools.", font=("Arial", 14)).pack(pady=20)
        tk.Label(self.root, text="Select unluac.jar location:").pack(pady=5)
        self.unluac_entry = tk.Entry(self.root, width=50)
        self.unluac_entry.pack(pady=5)
        unluac_button_frame = ttk.Frame(self.root)
        unluac_button_frame.pack(pady=5)
        ttk.Button(unluac_button_frame, text="Browse", command=self.browse_unluac).pack(side=tk.LEFT, padx=5)
        ttk.Button(unluac_button_frame, text="Install", command=self.install_unluac).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.root, text="Install c2ditools", command=self.install_c2ditools).pack(pady=20)
        ttk.Button(self.root, text="Install Offsetting", command=self.install_offsetting).pack(pady=20)
        ttk.Button(self.root, text="Finish Setup", command=self.finish_setup).pack(pady=20)
        tk.Label(self.root, text="unluac.jar can be installed automatically using the 'Install' buttons above.",
                                wraplength=600).pack(pady=10)
        print("Install UI displayed")


    def browse_unluac(self):
        filename = filedialog.askopenfilename(filetypes=[("JAR files", "*.jar")], title="Select unluac.jar")
        if filename:
            self.unluac_entry.delete(0, tk.END)
            self.unluac_entry.insert(0, filename)
            print(f"Selected unluac.jar: {filename}")


    def install_unluac(self):
        url = "https://github.com/Gh0styTongue/public-api/raw/refs/heads/main/C2/unluac.jar"
        jar_filename = "unluac.jar"
        print(f"Starting download of unluac.jar from {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            dest_path = os.path.join(script_dir, jar_filename)
            with open(dest_path, "wb") as f:
                f.write(response.content)
            self.unluac_entry.delete(0, tk.END)
            self.unluac_entry.insert(0, dest_path)
            print(f"Downloaded and placed unluac.jar at {dest_path}")
            messagebox.showinfo("Success", "unluac.jar downloaded and installed successfully!")
            print("unluac.jar installation completed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download unluac.jar: {str(e)}")
            print(f"unluac.jar download failed: {str(e)}")

    def install_c2ditools(self):
        print("Starting c2ditools installation")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "git+https://github.com/TKFRvisionOfficial/Cars2TheVideoGameModding.git"],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", "c2ditools installed successfully!")
                print("c2ditools installed successfully")
            else:
                messagebox.showerror("Error", f"Failed to install c2ditools:\n{result.stderr}")
                print(f"c2ditools installation failed: {result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run pip: {str(e)}")
            print(f"pip execution failed: {str(e)}")

    def install_offsetting(self):
        url = "https://github.com/offsetting/offsetting/releases/latest/download/offsetting_windows.exe"
        exe_path = os.path.join(os.getcwd(), "offsetting_windows.exe")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(exe_path, "wb") as f:
                f.write(response.content)
            self.offsetting_path = exe_path
            self.save_config()
            messagebox.showinfo("Success", "Offsetting installed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install offsetting: {str(e)}")

    def finish_setup(self):
        self.unluac_path = self.unluac_entry.get()
        print(f"Finishing setup with unluac_path={self.unluac_path}")
        if not os.path.exists(self.unluac_path):
            messagebox.showerror("Error", "Please select or install a valid unluac.jar file.")
            print(f"Invalid unluac_path: {self.unluac_path} does not exist")
            return
        try:
            import c2ditools
            print("c2ditools import successful")
        except ImportError:
            messagebox.showerror("Error", "c2ditools is not installed. Please click 'Install c2ditools' first.")
            print("c2ditools not installed")
            return
        self.save_config()
        self.show_main_ui()
        print("Setup completed, transitioning to main UI")

    def restart_setup(self):
        """Restarts the setup process by clearing the UI and showing the install screen."""
        self.show_install_ui()
        print("Restarting setup process")

    def show_main_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Cars 2 Modding Tool")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        self.tabs = {
            "Decode": ttk.Frame(self.notebook),
            "Encode": ttk.Frame(self.notebook),
            "Pack .zip": ttk.Frame(self.notebook),
            "Decrypt .lua": ttk.Frame(self.notebook),
            "Offsetting Decode": ttk.Frame(self.notebook),
            "Offsetting Encode": ttk.Frame(self.notebook)
        }
        for tab_name, tab_frame in self.tabs.items():
            self.notebook.add(tab_frame, text=tab_name)
        self.output_text = tk.Text(self.root, height=10, width=80)
        self.output_text.pack(pady=10)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Check Dependencies", command=self.check_dependencies).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Restart Setup", command=self.restart_setup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        self.setup_decode_tab()
        self.setup_encode_tab()
        self.setup_pack_zip_tab()
        self.setup_lua_decrypt_tab()
        self.setup_offsetting_decode_tab()
        self.setup_offsetting_encode_tab()
        print("Main UI displayed")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        print("Output cleared")

    def browse_file(self, entry, filetypes=[("All files", "*.*")]):
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)
            print(f"Browsed and selected file: {filename}")

    def browse_directory(self, entry):
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)
            print(f"Browsed and selected directory: {directory}")

    def run_command(self, command, shell=False):
        print(f"Running command: {' '.join(command) if not shell else command}")
        try:
            print(f"Running command: {command}")
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Command failed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Execution failed: {str(e)}")

    def check_dependencies(self):
        self.clear_output()
        messages = []
        print("Checking dependencies")
        try:
            import c2ditools
            self.output_text.insert(tk.END, "c2ditools: Installed\n")
            print("c2ditools check: Installed")
        except ImportError:
            messages.append("c2ditools is missing. Install it from the setup screen.")
            self.output_text.insert(tk.END, "c2ditools: Not installed\n")
            print("c2ditools check: Not installed")
        try:
            subprocess.run(["java", "-version"], capture_output=True, text=True, check=True)
            self.output_text.insert(tk.END, "Java: Installed\n")
            print("Java check: Installed")
        except subprocess.CalledProcessError:
            messages.append("Java is missing. Install Java to use Unluac for .lua decryption.")
            self.output_text.insert(tk.END, "Java: Not installed\n")
            print("Java check: Not installed")
        if os.path.exists(self.unluac_path):
            self.output_text.insert(tk.END, f"unluac.jar: Found at {self.unluac_path}\n")
            print(f"unluac.jar check: Found at {self.unluac_path}")
        else:
            messages.append("unluac.jar location is invalid. Re-run setup.")
            self.output_text.insert(tk.END, f"unluac.jar: Not found at {self.unluac_path}\n")
            print(f"unluac.jar check: Not found at {self.unluac_path}")
        if os.path.exists(self.offsetting_path):
            self.output_text.insert(tk.END, f"offsetting: Found at {self.offsetting_path}\n")
            print(f"offsetting: Found at {self.offsetting_path}")
        else:
            messages.append("Offsetting_Windows.exe location is invalid. Re-run setup")
            self.output_text.insert(tk.END, f"Offsetting_Windows.exe: Not found at {self.offsetting_path}\n")
            print(f"Offsetting_Windows.exe check: Not found at {self.offsetting_path}")
        if messages:
            messagebox.showwarning("Missing Dependencies", "\n\n".join(messages))
            print("Dependencies check completed with issues")
        else:
            messagebox.showinfo("Dependencies", "All required tools are installed!")
            print("Dependencies check completed successfully")

    def setup_decode_tab(self):
        frame = self.tabs["Decode"]
        tk.Label(frame, text="Input OCT File:").grid(row=0, column=0, padx=5, pady=5)
        self.decode_input = tk.Entry(frame, width=50)
        self.decode_input.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.decode_input)).grid(row=0, column=2, padx=5)
        tk.Label(frame, text="Output XML File:").grid(row=1, column=0, padx=5, pady=5)
        self.decode_output = tk.Entry(frame, width=50)
        self.decode_output.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.decode_output)).grid(row=1, column=2, padx=5)
        tk.Label(frame, text="Textures Directory:").grid(row=2, column=0, padx=5, pady=5)
        self.decode_textures = tk.Entry(frame, width=50)
        self.decode_textures.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_directory(self.decode_textures)).grid(row=2, column=2, padx=5)
        ttk.Button(frame, text="Decode", command=self.decode_oct).grid(row=3, column=1, pady=10)
        print("Decode tab setup completed")

    def decode_oct(self):
        print("Starting decode operation")
        try:
            import c2ditools
            command = ["python", "-m", "c2ditools", "scene_dec", self.decode_input.get(), self.decode_output.get(), "-t", self.decode_textures.get()]
            self.run_command(command)
            print("Decode operation completed")
        except ImportError:
            messagebox.showerror("Error", "c2ditools is not installed. Check setup.")
            self.output_text.insert(tk.END, "c2ditools not installed for decode\n")
            print("Decode failed: c2ditools not installed")

    def setup_encode_tab(self):
        frame = self.tabs["Encode"]
        tk.Label(frame, text="Input XML File:").grid(row=0, column=0, padx=5, pady=5)
        self.encode_input = tk.Entry(frame, width=50)
        self.encode_input.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.encode_input)).grid(row=0, column=2, padx=5)
        tk.Label(frame, text="Output OCT File:").grid(row=1, column=0, padx=5, pady=5)
        self.encode_output = tk.Entry(frame, width=50)
        self.encode_output.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.encode_output)).grid(row=1, column=2, padx=5)
        tk.Label(frame, text="Textures Directory:").grid(row=2, column=0, padx=5, pady=5)
        self.encode_textures = tk.Entry(frame, width=50)
        self.encode_textures.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_directory(self.encode_textures)).grid(row=2, column=2, padx=5)
        ttk.Button(frame, text="Encode", command=self.encode_xml).grid(row=3, column=1, pady=10)
        print("Encode tab setup completed")

    def encode_xml(self):
        print("Starting encode operation")
        try:
            import c2ditools
            command = ["python", "-m", "c2ditools", "scene_enc", self.encode_input.get(), self.encode_output.get(), "-t", self.encode_textures.get()]
            self.run_command(command)
            print("Encode operation completed")
        except ImportError:
            messagebox.showerror("Error", "c2ditools is not installed. Check setup.")
            self.output_text.insert(tk.END, "c2ditools not installed for encode\n")
            print("Encode failed: c2ditools not installed")

    def setup_offsetting_decode_tab(self):
        frame = self.tabs["Offsetting Decode"]
        tk.Label(frame, text="Input OCT File:").grid(row=0, column=0, padx=5, pady=5)
        self.decode_input = tk.Entry(frame, width=50)
        self.decode_input.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse",
                   command=lambda: self.browse_file(self.decode_input, [("OCT files", "*.oct")])).grid(row=0, column=2)
        ttk.Button(frame, text="Decode", command=self.offsetting_decode_oct).grid(row=1, column=1, pady=10)

    def offsetting_decode_oct(self):
        input_path = self.decode_input.get()
        output_path = input_path.replace(".oct", ".json")
        command = [self.offsetting_path, "oct", "decode", "-t", input_path, output_path]
        self.run_command(command)

    # def offsetting_indctive(self):
    #     input_path = self.decode_input.get()
    #     command = [self.offsetting_path, "dct", "unpack", self.decode_input.get(), self.decode_output.get()]


    def setup_offsetting_encode_tab(self):
        frame = self.tabs["Offsetting Encode"]
        tk.Label(frame, text="Input JSON File:").grid(row=0, column=0, padx=5, pady=5)
        self.encode_input = tk.Entry(frame, width=50)
        self.encode_input.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse",
                   command=lambda: self.browse_file(self.encode_input, [("JSON files", "*.json")])).grid(row=0,
                                                                                                         column=2)
        ttk.Button(frame, text="Encode", command=self.encode_json).grid(row=1, column=1, pady=10)

    def encode_json(self):
        input_path = self.encode_input.get()
        output_path = input_path.replace(".json", ".oct")
        command = [self.offsetting_path, "oct", "encode", "-t", input_path, output_path]
        self.run_command(command)

# New zip packing method
    def setup_pack_zip_tab(self):
        frame = self.tabs["Pack .zip"]
        tk.Label(frame, text="Output name:").grid(row=0, column=0, padx=5, pady=5)
        self.pack_name = tk.Entry(frame, width=50)
        self.pack_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Input Folder:").grid(row=1, column=0, padx=5, pady=5)
        self.pack_folder = tk.Entry(frame, width=50)  # Changed from pack_zip to pack_folder
        self.pack_folder.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_folder).grid(row=1, column=2, padx=5)

        ttk.Button(frame, text="Pack .zip", command=self.execute_pack_zip).grid(row=2, column=1, pady=10)
        print("Pack .zip tab setup completed")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.pack_folder.delete(0, tk.END)
            self.pack_folder.insert(0, folder_selected)

    def execute_pack_zip(self):
        print("Starting .zip packing operation")
        input_folder = self.pack_folder.get()
        output_file = self.pack_name.get().strip()

        if not input_folder:
            messagebox.showerror("Error", "Please select an input folder.")
            return
        if not output_file:
            messagebox.showerror("Error", "Please enter a name for the output file.")
            return

        output_zip = f"{output_file}.zip"

        try:
            command = ["python", "-m", "c2ditools", "why", input_folder, output_zip]
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", f"Packed {output_zip} successfully.")
            print(".zip packing operation completed")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to pack zip: {e}")
            print(f".zip packing failed: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "c2ditools is not installed or not found.")
            print(".zip packing failed: c2ditools not found")

# end of c2ditools .zip packing functions
# -----------------------------------------------------------------------------------------------------

    def setup_lua_decrypt_tab(self):
        frame = self.tabs["Decrypt .lua"]
        tk.Label(frame, text="Input .lua File:").grid(row=0, column=0, padx=5, pady=5)
        self.decrypt_input = tk.Entry(frame, width=50)
        self.decrypt_input.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.decrypt_input, [("LUA files", "*.lua")])).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Decrypt .lua", command=self.decrypt_lua).grid(row=1, column=1, pady=10)
        print(".lua Decryption tab setup completed")

    def decrypt_lua(self):
        print("Starting .lua decryption operation")
        if not os.path.exists(self.unluac_path):
            messagebox.showerror("Error", "unluac.jar path is invalid. Re-run setup.")
            self.output_text.insert(tk.END, f"unluac.jar not found at {self.unluac_path}\n")
            print(f"LUA decrypt failed: unluac.jar not found at {self.unluac_path}")
            return
        input_lua = self.decrypt_input.get()
        lua_dir = os.path.dirname(input_lua)
        base_name = os.path.splitext(os.path.basename(input_lua))[0]
        output_lua = os.path.join(lua_dir, f"{base_name}.dec.lua")
        temp_unluac_path = os.path.join(lua_dir, "unluac.jar")
        original_unluac_path = self.unluac_path
        print(f"Copying unluac.jar from {self.unluac_path} to {temp_unluac_path}")
        try:
            shutil.copy2(self.unluac_path, temp_unluac_path)
            self.output_text.insert(tk.END, f"Copied unluac.jar to {temp_unluac_path}\n")
            self.unluac_path = temp_unluac_path
            print(f"Temporarily set unluac_path to {self.unluac_path}")
            self.output_text.insert(tk.END, f"Output will be saved to {output_lua}\n")
            print(f"Output will be saved to {output_lua}")
            command = ["java", "-jar", self.unluac_path, input_lua, ">", output_lua]
            self.run_command(command, shell=True)
            print(".lua decryption operation completed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed during LUA decryption: {str(e)}")
            self.output_text.insert(tk.END, f"Decryption error: {str(e)}\n")
            print(f".lua decryption failed: {str(e)}")
        finally:
            self.unluac_path = original_unluac_path
            print(f"Reverted unluac_path to {self.unluac_path}")
            if os.path.exists(temp_unluac_path):
                os.remove(temp_unluac_path)
                self.output_text.insert(tk.END, f"Removed temporary unluac.jar from {temp_unluac_path}\n")
                print(f"Removed temporary unluac.jar from {temp_unluac_path}")
            else:
                print(f"Temporary unluac.jar not found at {temp_unluac_path}, no removal needed")

if __name__ == "__main__":
    root = tk.Tk()
    app = Cars2ModdingTool(root)
    root.mainloop()