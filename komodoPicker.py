import sys
import traceback

# --- CRASH GUARD ---
try:
    from PyQt6.QtWidgets import (
        QApplication, QWizard, QWizardPage, QVBoxLayout, QRadioButton,
        QButtonGroup, QLabel, QComboBox, QSpinBox, QFormLayout,
        QTextEdit, QPushButton, QMessageBox, QGroupBox, QWidget, QCheckBox,
        QToolTip
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont, QPalette, QColor, QCursor
except Exception as e:
    with open("crash_log.txt", "w") as f:
        f.write(f"CRASH ON IMPORT:\n{traceback.format_exc()}")
    sys.exit(1)

# --- THEME: KOMODO DRAGON (REFINED) ---
STYLESHEET = """
    QWizard, QWizardPage, QWidget { background-color: #121212; color: #ffffff; }
    
    /* Labels */
    QLabel { background-color: transparent; color: #e0e0e0; font-size: 14px; font-family: 'Segoe UI', sans-serif; }
    QLabel#Header { color: #ff3333; font-size: 16px; font-weight: bold; margin-top: 10px; }
    QLabel#Explanation { color: #b0b0b0; font-style: italic; margin-left: 10px; margin-bottom: 5px; }
    QLabel#Warning { color: #F6AB3A; font-weight: bold; font-size: 13px; }

    /* Group Box */
    QGroupBox { border: 1px solid #444; border-radius: 6px; margin-top: 20px; padding-top: 15px; background-color: #1a1a1a; }
    QGroupBox::title { 
        color: #ff3333;
        subcontrol-origin: margin; left: 10px; padding: 0 5px; font-weight: bold; background-color: #1a1a1a; 
    }

    /* Radio Buttons */
    QRadioButton {
        color: #e0e0e0; font-size: 14px; font-family: 'Segoe UI', sans-serif;
        padding: 5px;
    }
    QRadioButton:hover {
        color: #F6AB3A;
    }
    QRadioButton::indicator:checked {
        border: 2px solid #ff3333; background: #ff0000; border-radius: 9px; width: 14px; height: 14px;
    }
    QRadioButton::indicator:unchecked {
        border: 2px solid #555; background: #222; border-radius: 9px; width: 14px; height: 14px;
    }

    /* Inputs */
    QComboBox, QSpinBox { 
        background-color: #313131;
        color: #b0b0b0;
        border: 1px solid #99121D;
        padding: 6px; border-radius: 4px; 
    }
    QComboBox:hover, QSpinBox:hover { border: 1px solid #F6AB3A; }
    QComboBox::drop-down { border: none; background: #313131; }
    QComboBox QAbstractItemView {
        background-color: #313131;
        color: #b0b0b0;
        border: 1px solid #99121D;
        selection-background-color: #ff3333;
        selection-color: #ffffff;
    }

    /* Tooltips */
    QToolTip { 
        color: #e0e0e0;
        background-color: #313131;
        border: 2px solid #99121D;
        padding: 5px; font-weight: bold;
        font-family: 'Segoe UI', sans-serif; font-size: 13px;
    }

    /* Buttons */
    QPushButton { background-color: #b30000; color: #ffffff; border: 1px solid #ff3333; padding: 8px 20px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #ff0000; border: 1px solid #F6AB3A; }
    
    /* Output Text Area */
    QTextEdit { background-color: #000000; color: #00ff00; font-family: 'Consolas', monospace; border: 1px solid #ff3333; }
    
    /* Checkbox */
    QCheckBox { color: #e0e0e0; font-size: 14px; font-family: 'Segoe UI', sans-serif; }
    QCheckBox:hover { color: #F6AB3A; }
"""

class KomodoPicker(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Komodo Dragon Smart Consultant")
        self.resize(800, 700)
        self.setStyleSheet(STYLESHEET)
        
        # Shared Data Container
        self.data = {
            "ram_gb": 16, "workers": 4, 
            "mode": "standard", "submode": "nnue",
            "personality": "Default",
            "contempt": 0, "king_safety": 83, "dynamism": 100,
            "uci_options": {}
        }

        # Page Sequence
        self.setPage(1, HardwarePage(self.data))
        self.setPage(2, ModePage(self.data))
        self.setPage(3, StylePage(self.data))
        self.setPage(4, InternalsPage(self.data))
        self.setPage(5, OutputPage(self.data))
        self.setStartId(1)

# --- PAGE 1: HARDWARE ---
class HardwarePage(QWizardPage):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setTitle("Hardware Initialization")
        self.setSubTitle("Tell me about your system so I can calculate safe limits.")
        
        layout = QFormLayout()
        layout.setVerticalSpacing(20)

        self.ram_spin = QSpinBox()
        self.ram_spin.setRange(4, 512)
        self.ram_spin.setValue(16)
        self.ram_spin.setSuffix(" GB")
        self.create_row(layout, "Total System RAM:", self.ram_spin, "How much physical RAM does this computer have?")

        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 128)
        self.workers_spin.setValue(4)
        self.create_row(layout, "Number of Workers:", self.workers_spin, "How many engine instances will you run simultaneously?")

        self.status_lbl = QLabel("Calculated Safe Limit: ...")
        self.status_lbl.setObjectName("Warning")
        layout.addRow(self.status_lbl)
        
        self.ram_spin.valueChanged.connect(self.update_calc)
        self.workers_spin.valueChanged.connect(self.update_calc)
        self.setLayout(layout)
        self.update_calc()

    def create_row(self, layout, label, widget, tooltip):
        lbl = QLabel(label); lbl.setObjectName("Header")
        widget.setToolTip(tooltip)
        layout.addRow(lbl, widget)

    def update_calc(self):
        total_ram = self.ram_spin.value() * 1024 # MB
        workers = self.workers_spin.value()
        # Reserve 4GB for Windows/Apps
        avail_ram = max(1024, total_ram - 4096)
        safe_per_worker = int(avail_ram / workers)
        self.status_lbl.setText(f"Safe RAM per Worker: {safe_per_worker} MB (Hash + MCTS Hash)")

    def validatePage(self):
        self.data["ram_gb"] = self.ram_spin.value()
        self.data["workers"] = self.workers_spin.value()
        return True
    def nextId(self): return 2

# --- PAGE 2: MISSION PROFILE ---
class ModePage(QWizardPage):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setTitle("Mission Profile")
        self.setSubTitle("Select the operational parameter.")
        layout = QVBoxLayout()
        self.group = QButtonGroup(self)
        
        self.add_op(layout, 0, "Standard (NNUE)", "standard", "Default Super GM strength.\nBEST FOR: Verification.")
        self.add_op(layout, 1, "Deep Truth (MCTS)", "mcts", "Monte Carlo Search.\nBEST FOR: Complex positions where engine is blind.")
        self.add_op(layout, 2, "Human Repertoire", "human", "Unlocks Personality sliders.\nBEST FOR: Opening Books.")
        
        # Armageddon Sub-Selection
        self.arm_group = QGroupBox("Armageddon (Must Win)")
        
        arm_layout = QVBoxLayout()
        self.arm_nnue = QRadioButton("NNUE Armageddon (Max Strength)")
        self.arm_human = QRadioButton("Human Armageddon (Tal Style)")
        self.arm_nnue.setChecked(True)
        
        self.arm_nnue.setToolTip("Max strength Must-Win mode. Uses NNUE eval.")
        self.arm_human.setToolTip("Human-like Must-Win mode. Unlocks personality sliders.")

        arm_layout.addWidget(self.arm_nnue)
        arm_layout.addWidget(self.arm_human)
        self.arm_group.setLayout(arm_layout)
        layout.addWidget(self.arm_group)
        
        self.group.addButton(self.arm_nnue, 3)
        self.group.addButton(self.arm_human, 4)
        
        self.setLayout(layout)

    def add_op(self, layout, id, text, key, tip):
        rb = QRadioButton(text)
        if id == 0: rb.setChecked(True)
        rb.setToolTip(tip)
        rb.setProperty("key", key)
        self.group.addButton(rb, id)
        layout.addWidget(rb)
        layout.addSpacing(10)

    def nextId(self):
        idx = self.group.checkedId()
        if idx == 0: self.data["mode"]="standard"
        elif idx == 1: self.data["mode"]="mcts"
        elif idx == 2: self.data["mode"]="human"
        elif idx == 3: self.data["mode"]="armageddon"; self.data["submode"]="nnue"
        elif idx == 4: self.data["mode"]="armageddon"; self.data["submode"]="human"
        
        if self.data["mode"] == "human" or (self.data["mode"] == "armageddon" and self.data["submode"] == "human"):
            return 3
        return 4

# --- PAGE 3: STYLE ---
class StylePage(QWizardPage):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setTitle("Personality Matrix")
        self.setSubTitle("Hover over inputs for detailed effects.")
        layout = QFormLayout()
        layout.setVerticalSpacing(15)

        self.pers_combo = QComboBox()
        self.pers_combo.addItems(["Aggressive", "Defensive", "Positional", "Active", "Human", "Default"])
        self.create_row(layout, "Base Archetype", self.pers_combo, 
            "Sets baseline weights.\nAggressive: Sacrifices material for initiative.\nPositional: Values structure.")

        self.dynamism = QSpinBox()
        self.dynamism.setRange(0, 300); self.dynamism.setValue(120)
        self.create_row(layout, "Dynamism (Chaos)", self.dynamism, 
            "100 = Standard.\n150 = Tal (Prefers complications/tactics).\n50 = Petrosian (Prefers static safety).")

        self.king_safety = QSpinBox()
        self.king_safety.setRange(0, 200); self.king_safety.setValue(70)
        self.create_row(layout, "King Safety (Paranoia)", self.king_safety, 
            "100 = Standard.\n>100 = Cowardly (Castles early).\n<60 = Suicidal (Attacks with King exposed).")

        self.contempt = QSpinBox()
        self.contempt.setRange(-100, 100); self.contempt.setValue(20)
        self.create_row(layout, "Contempt (Ego)", self.contempt, 
            "0 = Objective Truth.\n20 = Avoids draws against equal foes.\n50 = Will lose rather than draw (risky).")

        self.setLayout(layout)

    def create_row(self, layout, label, widget, tip):
        lbl = QLabel(label); lbl.setObjectName("Header")
        widget.setToolTip(tip)
        layout.addRow(lbl, widget)

    def nextId(self): return 4
    def validatePage(self):
        self.data["personality"] = self.pers_combo.currentText()
        self.data["contempt"] = self.contempt.value()
        self.data["dynamism"] = self.dynamism.value()
        self.data["king_safety"] = self.king_safety.value()
        return True

# --- PAGE 4: INTERNALS ---
class InternalsPage(QWizardPage):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setTitle("Engine Internals")
        self.setSubTitle("Fine-tune the search. Limits based on your hardware.")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.widgets = {}

    def initializePage(self):
        # 1. Clear Visual Layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        # 2. CLEAR MEMORY (Prevents "Zombie Widget" Crash)
        self.widgets = {}

        mode = self.data["mode"]
        
        # Hardware Limits
        total_ram_mb = self.data["ram_gb"] * 1024
        workers = self.data["workers"]
        safe_ram_per_worker = (total_ram_mb - 4096) / workers
        
        # MCTS
        if mode == "mcts":
            self.add_spin("MCTS Explore", 35, 1, 100, 
                "C_PUCT Parameter.\nHigher = Wider Search (Looks at more candidate moves).\nLower = Deeper Search (Focuses on best moves).")
            # Split RAM: 30% Hash, 70% MCTS Hash
            mcts_def = int(safe_ram_per_worker * 0.6)
            self.add_spin("MCTS Hash", mcts_def, 16, 8192, 
                "Dedicated memory for MCTS Tree.\nIf this fills up, search slows down.")
            hash_def = int(safe_ram_per_worker * 0.3)
        else:
            self.add_spin("Selectivity", 150, 10, 250, 
                "Pruning Aggression (Search Width).\nHigher (>150) = Narrower & Deeper (Aggressive pruning, risky).\nLower (<100) = Wider & Shallower (Conservative pruning, safe).")
            hash_def = int(safe_ram_per_worker * 0.8)

        # Standard Options
        self.add_spin("Hash", hash_def, 16, 16384, "Main Transposition Table (MB).")
        self.add_spin("Threads", 1, 1, 64, "Threads PER WORKER.\nFor 4 workers, keep this 1-4.")
        
        self.add_spin("MultiPV", 1, 1, 50, 
            "Analyze multiple variations.\nKeep at 1 for Repertoire Generation or when using multiple workers, as it significantly slows down search.")
        
        self.ponder_chk = QCheckBox("Ponder (Think on opponent time) - OFF for Repertoire Generator")
        self.ponder_chk.setToolTip("Should be OFF for repertoire generation to save resources.")
        self.layout.addRow(QLabel("Ponder:"), self.ponder_chk)

    def add_spin(self, label, default, min_v, max_v, tip):
        spin = QSpinBox(); spin.setRange(min_v, max_v); spin.setValue(default)
        spin.setToolTip(tip)
        lbl = QLabel(label); lbl.setObjectName("Header")
        self.layout.addRow(lbl, spin)
        self.widgets[label] = spin

    def validatePage(self):
        self.data["uci_options"] = {k: v.value() for k, v in self.widgets.items()}
        self.data["uci_options"]["Ponder"] = "true" if self.ponder_chk.isChecked() else "false"
        return True
    def nextId(self): return 5

# --- PAGE 5: OUTPUT ---
class OutputPage(QWizardPage):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setTitle("Configuration Generated")
        self.setSubTitle("Copy the section below.")
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
        
        btn = QPushButton("COPY TO CLIPBOARD")
        btn.clicked.connect(self.copy_to_clip)
        layout.addWidget(btn)
        self.setLayout(layout)

    def initializePage(self):
        mode = self.data["mode"]
        sub = self.data["submode"]
        
        core = {}
        if mode == "mcts":
            core = {"Use MCTS": "true", "Use Regular Eval": "false", "Armageddon": "Off"}
        elif mode == "standard":
            core = {"Use MCTS": "false", "Use Regular Eval": "false", "Armageddon": "Off"}
        elif mode == "human":
            core = {"Use MCTS": "false", "Use Regular Eval": "true", "Armageddon": "Off",
                    "Personality": self.data["personality"], "Contempt": self.data["contempt"],
                    "Dynamism": self.data["dynamism"], "King Safety": self.data["king_safety"]}
        elif mode == "armageddon":
            core = {"Armageddon": "White Must Win", "Use MCTS": "false"}
            if sub == "nnue":
                core["Use Regular Eval"] = "false"
                core["Personality"] = "Default"
            else:
                core["Use Regular Eval"] = "true"
                core["Personality"] = self.data["personality"]

        adv = self.data["uci_options"]

        out = "=== CRITICAL CHANGES (Apply These) ===\n"
        for k, v in core.items(): out += f"{k} = {v}\n"
        out += "\n=== TUNING & HARDWARE ===\n"
        for k, v in adv.items(): out += f"{k} = {v}\n"
        out += "\n=== IGNORE BELOW (Defaults) ===\n"
        out += "Minibatch Size = 256\nLog File = false\n"
        
        self.text_area.setText(out)

    def copy_to_clip(self):
        QApplication.clipboard().setText(self.text_area.toPlainText())
        QMessageBox.information(self, "Copied", "Settings copied!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = KomodoPicker()
    wizard.show()
    sys.exit(app.exec())