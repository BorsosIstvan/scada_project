# 🖥️ SCADA Project

**Een zelfgebouwde, gratis SCADA-app in Python, met live communicatie via Modbus RTU.**  
Je kan objecten op het scherm plaatsen, realtime communiceren met een PLC (zoals een Arduino met OpenPLC), en zelfs tijdens de simulatie objecten toevoegen!

---

### 🚀 Features

- ✅ Realtime Modbus RTU communicatie
- ✅ Simulatie starten en stoppen met een klik
- ✅ Objecten toevoegen tijdens simulatie
- ✅ Registers uitlezen en terugschrijven naar de PLC
- ✅ Alles gemaakt zonder commerciële licentie

---

### 🔧 Hoe werkt het?

1. **Start het programma**
2. **Plaats objecten** (zoals knoppen, lampen, meters)
3. **Verbind met een PLC** via COM-poort
4. **Start simulatie** vanuit het menu
5. **Bekijk live data** uit registers (HR, Coils, etc.)
6. **Schrijf waarden terug** naar de PLC door objecten aan te passen

---

### ⚙️ Installatie

1. Clone de repo:
   ```bash
   git clone https://github.com/BorsosIstvan/scada_project.git
2. Installeer de vereisten:
   ```bash
   pip install -r requirements.txt
3. Start de app:
   ```bash
   python main.py

---

### 🧪 Gebruikte technologieën

🐍 Python 3

📦 PyModbus

🎨 Tkinter

🧱 PyInstaller (voor .exe bundel)

---

### 💡 Toekomstige uitbreidingen

- ✅ Objecten kunnen gewisseld worden

- ✅ Com-poort keuze via menu

- ✅ IP (Modbus TCP) ondersteuning

- ✅ Nieuwe objecttypes: lamp, meter, button

- ✅ Logische condities toevoegen (als temp > 60 → alarm)

- ✅ Projecten opslaan en laden

---

### 👨‍🔧 Gemaakt door
István – elektricien, maker, en liefhebber van slimme systemen
🇭🇺 Hongaars, 🇷🇴 Roemeens, werkt in 🇳🇱 Nederland

