# Komodo Tuner & Picker

A specialized configuration wizard and tuner for the **Komodo Chess Engine**. This tool was specifically designed to streamline the "Monte Carlo Tree Search" (MCTS) workflow and was built to complement the **Repertoire Generator** project.

## 🧠 About the Engine & Tuner
The **Komodo Chess Engine** (originally authored by Don Dailey and GM Larry Kaufman) is now owned by **Chess.com**. 

While many modern engines struggle with MCTS implementation, Larry Kaufman's work on Komodo remains the gold standard for providing a truly powerful, "human-like" Monte Carlo search without the typical configuration headaches.

*I have attempted: Rybka, Toga, Fruit, Rebel IV, Gambit Fruit, Various NNUE Engines, LC0, CERES (a rabbit hole of Cudnn Nvida Dev), MONTE - The intended MCTS Komodo Successor (another rabbit, shockingly its a rust build with abismul speed, performance, and crashes).* 

I may create a 'Universal Tuner' for these engines later. However; the purpose of this project was to generate a modern 'Reperitoire'; Or to capture 'engine response likeness' my Rerperitoire tool does just that, and will work on 95% of UCI engine builds.

But the Komodo engine, has a Custom UCI. And I had to then build a *Custom reperitoire generator tool just for Komodo*.  
Therefore;  I decided why stop there and created *this engine tuner* just for the komodo engine. 


### **Presets & Research**
The settings and presets within this tuner are not just random defaults. They are the result of:
* **Historical Analysis:** Deep evaluation of Larry Kaufman’s public discussions and engine development insights over the years.
* **Hardware Validation:** Extensive self-tournament play across various hardware architectures and specifications to ensure optimal resource allocation (RAM/Threads).
* **Standard Compliance:** Rigorous research into UCI protocols and Computer Chess Engine development best practices.

## 🚀 Installation & Usage

### **Windows Users**
The easiest way to run the Tuner is to download the `KomodoPicker.exe` from the **Releases** section.
* **Requirements:** You must have **Python** installed. We recommend the version available on the **Windows Store**.
* **No Install:** Simply launch the `.exe` and follow the wizard.

### **Linux Users**
Linux users are encouraged to run the provided binary or compile from source to match their specific distribution's `glibc` version.

---

## 🛠️ Developer & Build Info

If you wish to compile the source code yourself, ensure you have the following requirements:

### **Requirements / Repository Dependencies**
* Python 3.10+
* PyQt6
* PyInstaller

### **Build Command**
To create the standalone "Silent" executable (no console window), use the following command:

Open Terminal : ```bash
py -m PyInstaller --onefile --noconsole --collect-all PyQt6 --name "KomodoTuner" komodoPicker.py
