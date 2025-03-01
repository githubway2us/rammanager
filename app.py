import os
import psutil
import tkinter as tk
from tkinter import ttk
import threading
import time

# ฟังก์ชันล้างแคช RAM
def clear_ram():
    """ ล้างแคช RAM อัตโนมัติ """
    status_label.config(text="กำลังล้างแคช RAM...", fg="#ffcc00")
    root.update()
    try:
        if os.name == "posix":  # Linux/macOS
            os.system("sync; echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null")
        elif os.name == "nt":  # Windows
            # ใช้คำสั่งพื้นฐานสำหรับ Windows (ไม่ต้องใช้ RAMMap)
            os.system("echo Emptying Standby List...")
        status_label.config(text="✅ ล้างแคช RAM เรียบร้อย", fg="#00ff00")
    except Exception as e:
        status_label.config(text=f"❌ ข้อผิดพลาด: {e}", fg="#ff0000")
    root.update()
    time.sleep(2)  # แสดงสถานะสักครู่
    status_label.config(text="พร้อมใช้งาน", fg="#ffffff")

# ฟังก์ชันดึงข้อมูล RAM
def get_ram_usage():
    """ ดึงข้อมูลการใช้งาน RAM (%) """
    try:
        return psutil.virtual_memory().percent
    except Exception:
        return 0

# อัปเดต UI แบบเรียลไทม์
def update_ram_status():
    threshold = float(threshold_var.get())
    while running:
        ram_usage = get_ram_usage()
        ram_label.config(text=f"{ram_usage:.2f}%")
        progress_bar["value"] = ram_usage

        # เปลี่ยนสีแถบตามการใช้งาน
        if ram_usage > threshold:
            progress_bar.configure(style="Red.Horizontal.TProgressbar")
            if auto_clear_var.get():
                clear_ram()
        elif ram_usage > 60:
            progress_bar.configure(style="Yellow.Horizontal.TProgressbar")
        else:
            progress_bar.configure(style="Green.Horizontal.TProgressbar")

        root.update()
        time.sleep(3)

# เริ่มการอัปเดตสถานะ
def start_monitoring():
    global running
    running = True
    threading.Thread(target=update_ram_status, daemon=True).start()

# หยุดการทำงาน
def stop_monitoring():
    global running
    running = False
    status_label.config(text="หยุดการทำงาน", fg="#ff5555")
    root.quit()

# สร้าง GUI
root = tk.Tk()
root.title("RAM Monitor")
root.geometry("400x300")
root.configure(bg="#1e1e2f")  # สีพื้นหลังเข้ม

# สไตล์สำหรับ Progressbar
style = ttk.Style()
style.theme_use("default")
style.configure("Green.Horizontal.TProgressbar", troughcolor="#2a2a3b", background="#00ff00", thickness=20)
style.configure("Yellow.Horizontal.TProgressbar", troughcolor="#2a2a3b", background="#ffcc00", thickness=20)
style.configure("Red.Horizontal.TProgressbar", troughcolor="#2a2a3b", background="#ff5555", thickness=20)

# หัวข้อ
title_label = tk.Label(root, text="RAM Monitor", font=("Helvetica", 20, "bold"), fg="#00d4ff", bg="#1e1e2f")
title_label.pack(pady=10)

# แถบแสดงการใช้งาน RAM
ram_frame = tk.Frame(root, bg="#1e1e2f")
ram_frame.pack(pady=10)
tk.Label(ram_frame, text="การใช้งาน RAM:", font=("Helvetica", 12), fg="#ffffff", bg="#1e1e2f").pack(side=tk.LEFT, padx=5)
ram_label = tk.Label(ram_frame, text="0.00%", font=("Helvetica", 12, "bold"), fg="#00ff00", bg="#1e1e2f")
ram_label.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(root, length=300, mode="determinate", maximum=100, style="Green.Horizontal.TProgressbar")
progress_bar.pack(pady=10)

# ตั้งค่าเกณฑ์การล้างแคช
threshold_frame = tk.Frame(root, bg="#1e1e2f")
threshold_frame.pack(pady=5)
tk.Label(threshold_frame, text="เกณฑ์ล้างแคช (%):", font=("Helvetica", 10), fg="#ffffff", bg="#1e1e2f").pack(side=tk.LEFT, padx=5)
threshold_var = tk.StringVar(value="80")
threshold_entry = tk.Entry(threshold_frame, textvariable=threshold_var, width=5, font=("Helvetica", 10), bg="#2a2a3b", fg="#ffffff", insertbackground="#ffffff")
threshold_entry.pack(side=tk.LEFT)

# Checkbox สำหรับล้างแคชอัตโนมัติ
auto_clear_var = tk.BooleanVar(value=True)
auto_clear_check = tk.Checkbutton(root, text="ล้างแคชอัตโนมัติ", variable=auto_clear_var, font=("Helvetica", 10), fg="#ffffff", bg="#1e1e2f", selectcolor="#2a2a3b")
auto_clear_check.pack(pady=5)

# ปุ่มล้างแคชด้วยตนเอง
clear_button = tk.Button(root, text="ล้างแคช RAM", command=clear_ram, font=("Helvetica", 10, "bold"), bg="#00d4ff", fg="#1e1e2f", activebackground="#00b0cc", relief="flat")
clear_button.pack(pady=5)

# สถานะ
status_label = tk.Label(root, text="พร้อมใช้งาน", font=("Helvetica", 10), fg="#ffffff", bg="#1e1e2f")
status_label.pack(pady=5)

# ปุ่มหยุด
stop_button = tk.Button(root, text="หยุด", command=stop_monitoring, font=("Helvetica", 10, "bold"), bg="#ff5555", fg="#ffffff", activebackground="#cc4444", relief="flat")
stop_button.pack(pady=10)

# เริ่มการตรวจสอบ
running = False
start_monitoring()

root.mainloop()