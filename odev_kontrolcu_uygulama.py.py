import tkinter as tk
import cv2
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def odev_tara():
    sonuc.config(text="📷 Ödev taranıyor, bekle...", fg="white")
    pencere.update()

    kamera = cv2.VideoCapture(0)
    start_time = time.time()
    foto = None

    while True:
        ret, cerceve = kamera.read()
        if not ret:
            break

        kalan = 5 - int(time.time() - start_time)
        cv2.putText(cerceve, f"KONTROL: {max(0, kalan)}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Ödev Taraniyor", cerceve)

        if kalan <= 0:
            foto = cerceve.copy()
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    kamera.release()
    cv2.destroyAllWindows()

    if foto is None:
        sonuc.config(text="❌ Foto alınamadı", fg="red")
        return

    gri = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
    metin = pytesseract.image_to_string(gri).strip()

    if len(metin) > 10:
        sonuc.config(text=f"✅ ÖDEV VAR ({len(metin)} karakter)", fg="green")
    elif len(metin) > 0:
        sonuc.config(text="⚠️ ÖDEV EKSİK", fg="yellow")
    else:
        sonuc.config(text="❌ ÖDEV YOK / OKUNAMADI", fg="red")

# ---------- GUI ----------

pencere = tk.Tk()
pencere.title("SametTech – Yapay Zeka Ödev Kontrolcü")
pencere.geometry("550x350")
pencere.configure(bg="#1e1e2f")  # koyu mor-siyah arka plan

tk.Label(pencere, text="📄 Yapay Zeka Ödev Kontrolcü",
         font=("Arial", 18, "bold"), bg="#1e1e2f", fg="#ffcc00").pack(pady=15)

tk.Button(pencere, text="📷 Ödevi Tara", font=("Arial", 14, "bold"),
          bg="#ff6600", fg="white", activebackground="#ffaa33",
          command=odev_tara).pack(pady=20)

sonuc = tk.Label(pencere, text="", font=("Arial", 15, "bold"),
                 bg="#1e1e2f", fg="white")
sonuc.pack(pady=20)

pencere.mainloop()
