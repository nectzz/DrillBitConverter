import sys
import os
import tkinter as tk
from tkinter import ttk
from fractions import Fraction
from PIL import Image, ImageTk

def resource_path(relative_path):
    """Get absolute resource path, compatible with PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --- Drill size table ---
drills = [
    ("1/64", 0.0156, 0.3969), ("1/32", 0.0312, 0.7938), ("3/64", 0.0469, 1.1906),
    ("1/16", 0.0625, 1.5875), ("5/64", 0.0781, 1.9844), ("3/32", 0.0938, 2.3813),
    ("7/64", 0.1094, 2.7781), ("1/8", 0.1250, 3.1750), ("9/64", 0.1406, 3.5719),
    ("5/32", 0.1562, 3.9688), ("11/64", 0.1719, 4.3656), ("3/16", 0.1875, 4.7625),
    ("13/64", 0.2031, 5.1594), ("7/32", 0.2188, 5.5563), ("15/64", 0.2344, 5.9531),
    ("1/4", 0.2500, 6.3500), ("17/64", 0.2656, 6.7469), ("9/32", 0.2812, 7.1438),
    ("19/64", 0.2969, 7.5406), ("5/16", 0.3125, 7.9375), ("21/64", 0.3281, 8.3344),
    ("11/32", 0.3438, 8.7313), ("23/64", 0.3594, 9.1281), ("3/8", 0.3750, 9.5250),
    ("25/64", 0.3906, 9.9219), ("13/32", 0.4062, 10.3188), ("27/64", 0.4219, 10.7156),
    ("7/16", 0.4375, 11.1125), ("29/64", 0.4531, 11.5094), ("15/32", 0.4688, 11.9063),
    ("31/64", 0.4844, 12.3031), ("1/2", 0.5000, 12.7000),
    ("33/64", 0.5156, 13.0969), ("17/32", 0.5312, 13.4938), ("35/64", 0.5469, 13.8906),
    ("9/16", 0.5625, 14.2875), ("37/64", 0.5781, 14.6844), ("19/32", 0.5938, 15.0813),
    ("39/64", 0.6094, 15.4781), ("5/8", 0.6250, 15.8750), ("41/64", 0.6406, 16.2719),
    ("21/32", 0.6562, 16.6688), ("43/64", 0.6719, 17.0656), ("11/16", 0.6875, 17.4625),
    ("45/64", 0.7031, 17.8594), ("23/32", 0.7188, 18.2563), ("47/64", 0.7344, 18.6531),
    ("3/4", 0.7500, 19.0500), ("49/64", 0.7656, 19.4469), ("25/32", 0.7812, 19.8438),
    ("51/64", 0.7969, 20.2406), ("13/16", 0.8125, 20.6375), ("53/64", 0.8281, 21.0344),
    ("27/32", 0.8438, 21.4313), ("55/64", 0.8594, 21.8281), ("7/8", 0.8750, 22.2250),
    ("57/64", 0.8906, 22.6219), ("29/32", 0.9062, 23.0188), ("59/64", 0.9219, 23.4156),
    ("15/16", 0.9375, 23.8125), ("61/64", 0.9531, 24.2094), ("31/32", 0.9688, 24.6063),
    ("63/64", 0.9844, 25.0031), ("1", 1.0000, 25.4000),
]

def find_approximations(inches):
    lower = None
    upper = None
    exact = None

    for i, (_, value, _) in enumerate(drills):
        if value == inches:
            exact = drills[i]
            lower = drills[i - 1] if i > 0 else None
            upper = drills[i + 1] if i < len(drills) - 1 else None
            break
        elif value < inches:
            lower = drills[i]
        elif value > inches:
            upper = drills[i]
            break

    return lower, upper, exact

# --- Create main window ---
root = tk.Tk()
root.title("Drill Size Converter")
root.geometry("500x500")
root.configure(bg="white")

# Use ttk theme
style = ttk.Style(root)
style.theme_use("clam")

# --- Fonts ---
title_font = ("Segoe UI", 16, "bold")
normal_font = ("Segoe UI", 12)
button_font = ("Segoe UI", 12, "bold")
result_font = ("Segoe UI", 12, "bold")

# --- Widgets ---
frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Drill Size Converter", font=title_font).pack(pady=(0, 10))

ttk.Label(frame, text="Enter size:", font=normal_font).pack(pady=(10, 5))
entry = ttk.Entry(frame, width=20, font=normal_font)
entry.pack()

unit_var = tk.StringVar(value="fraction")
options = ttk.OptionMenu(frame, unit_var, "fraction", "fraction", "in", "mm")
options.config(width=10)
options.pack(pady=5)

result_label = ttk.Label(frame, text="", justify="left", font=result_font, background="white")
result_label.pack(pady=10, fill="x")

def convert(event=None):
    input_value = entry.get().strip()
    unit = unit_var.get()
    try:
        if unit == "fraction":
            inches = float(Fraction(input_value))
        elif unit == "mm":
            inches = float(input_value) / 25.4
        elif unit == "in":
            inches = float(input_value)
        else:
            raise ValueError

        millimeters = inches * 25.4
        lower, upper, exact = find_approximations(inches)

        text = f"Decimal inches: {inches:.4f}\nMillimeters: {millimeters:.3f} mm\n"

        idx = None
        if exact:
            idx = drills.index(exact)
            lowers = []
            for i in range(idx - 2, idx):
                if i >= 0:
                    lowers.append(drills[i])
            if lowers:
                text += "\n🔽 Lower sizes:"
                for l in lowers:
                    text += f"\n• {l[0]} ({l[1]:.4f} in / {l[2]:.2f} mm)"
            text += f"\n\n🎯 Exact size: {exact[0]} ({exact[1]:.4f} in / {exact[2]:.2f} mm)\n"
            uppers = []
            for i in range(idx + 1, idx + 3):
                if i < len(drills):
                    uppers.append(drills[i])
            if uppers:
                text += "\n🔼 Upper sizes:"
                for u in uppers:
                    text += f"\n• {u[0]} ({u[1]:.4f} in / {u[2]:.2f} mm)"
        else:
            approx = None
            if lower and upper:
                dist_lower = abs(inches - lower[1])
                dist_upper = abs(inches - upper[1])
                approx = lower if dist_lower <= dist_upper else upper
            elif lower:
                approx = lower
            elif upper:
                approx = upper
            else:
                approx = None

            if approx:
                diff_mm = abs(millimeters - approx[2])
                idx = drills.index(approx)
                lowers = []
                for i in range(idx - 2, idx):
                    if i >= 0:
                        lowers.append(drills[i])
                if lowers:
                    text += "\n🔽 Lower sizes:"
                    for l in lowers:
                        text += f"\n• {l[0]} ({l[1]:.4f} in / {l[2]:.2f} mm)"
                text += f"\n\n📏 Approximate size: {approx[0]} ({approx[1]:.4f} in / {approx[2]:.2f} mm)"
                text += f"\n   Difference: {diff_mm:.3f} mm\n"
                uppers = []
                for i in range(idx + 1, idx + 3):
                    if i < len(drills):
                        uppers.append(drills[i])
                if uppers:
                    text += "\n🔼 Upper sizes:"
                    for u in uppers:
                        text += f"\n• {u[0]} ({u[1]:.4f} in / {u[2]:.2f} mm)"

        result_label.config(text=text)
        entry.delete(0, tk.END)
    except Exception:
        result_label.config(text="⚠️ Invalid input")
        entry.delete(0, tk.END)

def copy_result():
    root.clipboard_clear()
    root.clipboard_append(result_label.cget("text"))
    root.update()
    result_label.config(text=result_label.cget("text") + "\n📋 Copied to clipboard.")

ttk.Button(frame, text="Convert", command=convert, style="Accent.TButton").pack(pady=10)
ttk.Button(frame, text="📋 Copy result", command=copy_result).pack(pady=5)

entry.bind("<Return>", convert)  # Allow Enter to convert

root.mainloop()
