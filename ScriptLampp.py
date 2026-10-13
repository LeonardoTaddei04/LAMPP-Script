import subprocess
import tkinter as tk
from tkinter import scrolledtext


def esegui_comando(azione):
  # Mappa le azioni ai comandi XAMPP
  comandi = {
      "Avvia": ["sudo", "/opt/lampp/lampp", "start"],
      "Riavvia": ["sudo", "/opt/lampp/lampp", "restart"],
      "Spegni": ["sudo", "/opt/lampp/lampp", "stop"],
  }

  if azione not in comandi:
    return

  # Pulisce l'area di testo e mostra l'avvio
  area_output.config(state=tk.NORMAL)
  area_output.delete("1.0", tk.END)
  area_output.insert(tk.END, f"Esecuzione: {' '.join(comandi[azione])}...\n")
  area_output.config(state=tk.DISABLED)

  # Esegue il comando in modo asincrono per non bloccare l'interfaccia
  root.after(100, lambda: avvia_processo(comandi[azione]))


def avvia_processo(cmd):
  try:
    # Esegue il comando e cattura l'output
    processo = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    area_output.config(state=tk.NORMAL)

    # Legge l'output in tempo reale
    for linea in iter(processo.stdout.readline, ""):
      area_output.insert(tk.END, linea)
      area_output.see(tk.END)
      root.update_idletasks()

    processo.stdout.close()
    processo.wait()
    area_output.insert(tk.END, "\n--- Operazione completata ---\n")
  except Exception as e:
    area_output.insert(tk.END, f"\nErrore durante l'esecuzione: {e}\n")

  area_output.config(state=tk.DISABLED)


# --- Configurazione Interfaccia Grafica ---
root = tk.Tk()
root.title("XAMPP Manager")
root.geometry("480x360")
root.minsize(400, 300)

# Frame per i pulsanti in alto
frame_pulsanti = tk.Frame(root, padx=10, pady=10)
frame_pulsanti.pack(fill=tk.X)

# Pulsanti minimali
btn_avvia = tk.Button(
    frame_pulsanti,
    text="▶ Avvia",
    bg="#2ecc71",
    fg="white",
    font=("Arial", 10, "bold"),
    command=lambda: esegui_comando("Avvia"),
)
btn_avvia.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

btn_riavvia = tk.Button(
    frame_pulsanti,
    text="🔄 Riavvia",
    bg="#f39c12",
    fg="white",
    font=("Arial", 10, "bold"),
    command=lambda: esegui_comando("Riavvia"),
)
btn_riavvia.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

btn_spegni = tk.Button(
    frame_pulsanti,
    text="⏹ Spegni",
    bg="#e74c3c",
    fg="white",
    font=("Arial", 10, "bold"),
    command=lambda: esegui_comando("Spegni"),
)
btn_spegni.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

# Area di testo per l'output del terminale (con scorrimento automatico)
area_output = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9)
)
area_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
area_output.config(
    state=tk.DISABLED
)  # Impedisce la digitazione manuale nell'output

root.mainloop()