# How to Run: Regression and Prediction of Concrete Strength (Q1.1)

This program fits Linear, Quadratic, Logarithmic and Exponential regression models to the concrete cube
test data (curing age vs compressive strength), compares them, and predicts strength at t = 10 and 35 days.

## Files

| File | Purpose |
|---|---|
| `regression_analysis.py` | Main program (data, four models, metrics, plots) |
| `verify.py` | Optional independent check using plain Python formulas (no numpy) |

## What the program produces

All outputs are saved in the **same folder as the script**:

- `fig1_fits.png` – data and the four fitted curves
- `fig2_residuals.png` – residual plots
- `fig3_predictions.png` – predictions at t = 10 d and 35 d
- `results.json` – all coefficients, metrics and predictions
- A summary printed in the terminal (equations, R², RMSE, predictions)

Plots are saved as image files, so no plot window opens.

## Requirements

- Python 3.9 or newer (3.10+ recommended)
- Packages: `numpy`, `scipy`, `matplotlib`

`verify.py` needs only Python (no extra packages).

---

## Option A: Run in Windows PowerShell

1. **Check Python is installed.** Open PowerShell and run:
   ```powershell
   python --version
   ```
   If this fails, try `py --version`. If both fail, install Python from https://www.python.org/downloads/
   and tick **"Add python.exe to PATH"** during installation. Then reopen PowerShell.
   (If `py` works but `python` does not, use `py` in place of `python` in every command below.)

2. **Go to the folder containing the script.** Replace the path with your own:
   ```powershell
   cd "C:\Users\YourName\Documents\ConcreteRegression"
   ```
   Check that the file is there:
   ```powershell
   dir
   ```

3. **(Recommended) Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   If PowerShell says *"running scripts is disabled on this system"*, run this once and try again:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```
   When active, the prompt starts with `(venv)`.

4. **Install the packages:**
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install numpy scipy matplotlib
   ```

5. **Run the program:**
   ```powershell
   python regression_analysis.py
   ```

6. **Open the results.** The terminal prints the table of models and predictions. To view the figures:
   ```powershell
   start fig1_fits.png
   start fig2_residuals.png
   start fig3_predictions.png
   ```

7. **(Optional) Run the independent check:**
   ```powershell
   python verify.py
   ```
   Its R², RMSE, f(10 d) and f(35 d) values should match the main program.

---

## Option B: Run in VS Code

1. **Install the tools** (once): VS Code (https://code.visualstudio.com), Python, and the **Python extension**
   by Microsoft (Extensions icon on the left sidebar, search "Python", click Install).

2. **Open the folder.** `File > Open Folder...` and choose the folder containing `regression_analysis.py`.
   Open the file from the Explorer panel.

3. **Select the interpreter.** Press `Ctrl+Shift+P`, type **Python: Select Interpreter**, and choose your
   Python (or the `venv` one if you created it).

4. **Open the terminal inside VS Code:** `Terminal > New Terminal` (or ``Ctrl+` ``). It opens in the project folder.

5. **Install the packages** in that terminal:
   ```powershell
   python -m pip install numpy scipy matplotlib
   ```
   (If you made a virtual environment, activate it first with `.\venv\Scripts\Activate.ps1`.)

6. **Run the program** using either method:
   - Click the **Run** triangle at the top right of the editor, or
   - Type in the terminal:
     ```powershell
     python regression_analysis.py
     ```

7. **View the figures:** the three `.png` files appear in the Explorer panel. Click one to preview it in VS Code.

---

## Expected output (check your run against this)

| Model | Equation (f in MPa, t in days) | R² | f(10 d) MPa | f(35 d) MPa |
|---|---|---|---|---|
| Linear | f = 17.577 + 0.7210 t | 0.9389 | 24.79 | 42.81 |
| Quadratic | f = 13.862 + 1.4639 t − 0.02411 t² | 0.9900 | 26.09 | 35.57 |
| Logarithmic | f = 7.904 + 8.3746 ln t | 0.9935 | 27.19 | 37.68 |
| Exponential | f = 18.278 exp(0.02723 t) | 0.8811 | 24.00 | 47.41 |

The first printed line should read `Area = 22500 mm^2; 385 kN -> 17.111 MPa`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `'python' is not recognized` | Install Python with "Add to PATH", or use `py` instead of `python` |
| `ModuleNotFoundError: No module named 'numpy'` (or scipy / matplotlib) | Run `python -m pip install numpy scipy matplotlib` in the same terminal/interpreter you use to run the script |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again |
| VS Code runs a different Python than the terminal | `Ctrl+Shift+P`, **Python: Select Interpreter**, pick the one where you installed the packages |
| Figures not found | They are saved next to `regression_analysis.py`, not in the folder where you opened PowerShell from |
| `PermissionError` when saving | Close any image viewer holding the old `.png` open, or move the folder out of OneDrive/read-only locations |

## Changing the data

Edit the `age` and `load` arrays near the top of `regression_analysis.py` (section "1. DATA") and the
prediction ages in `T_PRED` (and the `pred10` / `pred35` calls if you want different times), then run again.
