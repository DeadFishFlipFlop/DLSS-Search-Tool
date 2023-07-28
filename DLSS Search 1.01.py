import os
import platform
import win32api
import tkinter as tk
from tkinter import messagebox
from tqdm import tqdm

def find_file(file_name, search_path='C:\\'):
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def get_product_version(file_path):
    try:
        version_info = win32api.GetFileVersionInfo(file_path, "\\")
        ms = version_info['ProductVersionMS']
        ls = version_info['ProductVersionLS']
        product_version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
        return product_version

    except Exception as e:
        return None

def convert_bytes_to_mb(bytes_size):
    mb_size = bytes_size / (1024 * 1024)
    return "{:.2f}".format(mb_size)  # Format to two decimal places

if __name__ == "__main__":
    file_to_find = 'nvngx_dlss.dll'
    found_files = []

    # Search drives C: through Z: with tqdm progress indicator
    drives = [chr(drive_letter) + ':\\' for drive_letter in range(ord('C'), ord('Z') + 1)]
    for drive in tqdm(drives, desc="Searching Drives for DLSS"):
        file_path = find_file(file_to_find, drive)
        if file_path:
            file_size = os.path.getsize(file_path)
            file_size_mb = convert_bytes_to_mb(file_size)
            found_files.append((file_path, get_product_version(file_path), file_size_mb))

    if found_files:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        results_str = "Search Results:\n\n"
        for file_path, product_version, file_size_mb in found_files:
            results_str += f"File: {file_path}\nProduct Version: {product_version}\nSize: {file_size_mb} MB\n\n"

        # Display results in a dialog box
        messagebox.showinfo("DLSS Search Results", results_str)
    else:
        messagebox.showinfo("DLSS Search Results", f"{file_to_find} not found on any drive (C: through Z:).")
