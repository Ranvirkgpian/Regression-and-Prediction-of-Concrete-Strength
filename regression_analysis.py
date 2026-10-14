"""
Q1.1  Regression and Prediction of Concrete Strength
Curing age (days) vs compressive strength of 150 mm cubes.
Models: Linear, Quadratic, Logarithmic, Exponential.
Run:  python regression_analysis.py
Outputs: figures (PNG) + results.json in the same folder as this script.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- 1. DATA ----------------
age = np.array([3, 7, 14, 21, 28], dtype=float)                     # days
load = np.array([[385, 395, 400],
                 [525, 535, 545],
                 [655, 665, 680],
                 [740, 755, 760],
                 [800, 815, 830]], dtype=float)                      # kN
AREA = 150.0 * 150.0                                                 # mm^2 (cube face)
stress = load * 1e3 / AREA                                           # N/mm^2 = MPa
t = np.repeat(age, 3)                                                # 15 observations
f = stress.flatten()
n = len(f)
T_PRED = np.array([10.0, 35.0])

# ---------------- 2. MODELS ----------------
def r2(y, yh):  return 1 - np.sum((y - yh) ** 2) / np.sum((y - y.mean()) ** 2)
def adj(r, n, p): return 1 - (1 - r) * (n - 1) / (n - p - 1)       # p = predictors

models = {}

# Linear: f = a + b t
b1, a1 = np.polyfit(t, f, 1)
models["Linear"] = dict(fn=lambda x, a=a1, b=b1: a + b * x, p=1,
                        eq=f"f = {a1:.3f} + {b1:.4f} t", coef=dict(a=a1, b=b1))

# Quadratic: f = a + b t + c t^2
c2, b2, a2 = np.polyfit(t, f, 2)
models["Quadratic"] = dict(fn=lambda x, a=a2, b=b2, c=c2: a + b * x + c * x ** 2, p=2,
                           eq=f"f = {a2:.3f} + {b2:.4f} t {c2:+.5f} t^2", coef=dict(a=a2, b=b2, c=c2))

# Logarithmic: f = a + b ln t
b3, a3 = np.polyfit(np.log(t), f, 1)
models["Logarithmic"] = dict(fn=lambda x, a=a3, b=b3: a + b * np.log(x), p=1,
                             eq=f"f = {a3:.3f} + {b3:.4f} ln(t)", coef=dict(a=a3, b=b3))

# Exponential: f = A e^(k t)  -> ln f = ln A + k t (linearised least squares)
k4, lnA4 = np.polyfit(t, np.log(f), 1)
A4 = np.exp(lnA4)
models["Exponential"] = dict(fn=lambda x, A=A4, k=k4: A * np.exp(k * x), p=1,
                             eq=f"f = {A4:.3f} exp({k4:.5f} t)", coef=dict(A=A4, k=k4))

# ---------------- 3. METRICS ----------------
results = {}
for name, m in models.items():
    yh = m["fn"](t)
    res = f - yh
    R2 = r2(f, yh)
    sse = float(np.sum(res ** 2))
    dof = n - (m["p"] + 1)
    # leave-one-age-out CV (drop all 3 cubes of one age, refit, predict them)
    cv_err = []
    for ag in age:
        tr = t != ag
        tt, ff = t[tr], f[tr]
        if name == "Linear":       c = np.polyfit(tt, ff, 1);           pr = np.polyval(c, ag)
        elif name == "Quadratic":  c = np.polyfit(tt, ff, 2);           pr = np.polyval(c, ag)
        elif name == "Logarithmic":c = np.polyfit(np.log(tt), ff, 1);   pr = np.polyval(c, np.log(ag))
        else:                      c = np.polyfit(tt, np.log(ff), 1);   pr = np.exp(np.polyval(c, ag))
        cv_err.extend(f[t == ag] - pr)
    results[name] = dict(
        equation=m["eq"], coef={k: float(v) for k, v in m["coef"].items()},
        R2=float(R2), adjR2=float(adj(R2, n, m["p"])),
        SSE=sse, RMSE=float(np.sqrt(sse / n)), SE=float(np.sqrt(sse / dof)),
        MAE=float(np.mean(np.abs(res))), CV_RMSE=float(np.sqrt(np.mean(np.square(cv_err)))),
        pred10=float(m["fn"](10.0)), pred35=float(m["fn"](35.0)),
        pred28=float(m["fn"](28.0)),
        residuals=[float(x) for x in res])

# ---------------- 4. VALIDATION CHECKS ----------------
checks = {}
# (a) polyfit vs explicit normal equations for the linear model
X = np.c_[np.ones(n), t]
beta = np.linalg.solve(X.T @ X, X.T @ f)
checks["linear_normal_eq_vs_polyfit"] = [float(beta[0]), float(a1), float(beta[1]), float(b1)]
# (b) true nonlinear LSQ for exponential, compared with linearised version
popt, _ = curve_fit(lambda x, A, k: A * np.exp(k * x), t, f, p0=[A4, k4])
yh_nl = popt[0] * np.exp(popt[1] * t)
checks["exp_nonlinear"] = dict(A=float(popt[0]), k=float(popt[1]), R2=float(r2(f, yh_nl)),
                               pred10=float(popt[0] * np.exp(popt[1] * 10)),
                               pred35=float(popt[0] * np.exp(popt[1] * 35)))
# (c) hand checks on the raw data
mean_strength = stress.mean(axis=1)
checks["mean_strength_by_age"] = [float(x) for x in mean_strength]
checks["ratio_to_28d"] = [float(x) for x in mean_strength / mean_strength[-1]]
checks["unit_check_385kN"] = float(385e3 / AREA)
checks["quad_vertex_t"] = float(-b2 / (2 * c2)) if c2 != 0 else None
# (d) supplementary saturating model (not requested; used only for discussion)
sat, _ = curve_fit(lambda x, fi, k: fi * (1 - np.exp(-k * x)), t, f, p0=[45, 0.1])
yh_sat = sat[0] * (1 - np.exp(-sat[1] * t))
checks["saturating_extra"] = dict(finf=float(sat[0]), k=float(sat[1]), R2=float(r2(f, yh_sat)),
                                  pred10=float(sat[0] * (1 - np.exp(-sat[1] * 10))),
                                  pred35=float(sat[0] * (1 - np.exp(-sat[1] * 35))))

json.dump(dict(results=results, checks=checks,
               data=dict(age=age.tolist(), load=load.tolist(), stress=stress.tolist())),
          open(os.path.join(OUT, "results.json"), "w"), indent=2)

# ---------------- 5. PLOTS ----------------
colors = {"Linear": "tab:blue", "Quadratic": "tab:green", "Logarithmic": "tab:red", "Exponential": "tab:purple"}
tt = np.linspace(1, 40, 400)

fig, ax = plt.subplots(figsize=(8, 5.2))
ax.scatter(t, f, c="k", s=28, zorder=5, label="Experimental (15 cubes)")
ax.scatter(age, mean_strength, marker="D", facecolor="none", edgecolor="k", s=70, zorder=5, label="Mean at each age")
for nm, m in models.items():
    ax.plot(tt, m["fn"](tt), color=colors[nm], lw=1.8, label=f"{nm} (R² = {results[nm]['R2']:.4f})")
ax.axvspan(28, 40, color="0.92", zorder=0); ax.text(28.6, 3, "extrapolation\nbeyond data", fontsize=8, color="0.4")
for tp, ls in zip(T_PRED, [":", ":"]): ax.axvline(tp, color="0.5", ls=ls, lw=0.9)
ax.set_xlabel("Curing age, t (days)"); ax.set_ylabel("Compressive strength, f (N/mm² = MPa)")
ax.set_title("Compressive strength vs curing age: four regression models")
ax.set_xlim(0, 40); ax.set_ylim(0, None); ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig1_fits.png"), dpi=200); plt.close(fig)

fig, axs = plt.subplots(2, 2, figsize=(8, 5.6), sharex=True, sharey=True)
for ax, (nm, m) in zip(axs.flat, models.items()):
    ax.axhline(0, color="k", lw=0.8); ax.scatter(t, results[nm]["residuals"], color=colors[nm], s=26)
    ax.set_title(f"{nm}  (RMSE = {results[nm]['RMSE']:.2f} MPa)", fontsize=9); ax.grid(alpha=0.3)
for ax in axs[1]: ax.set_xlabel("Curing age, t (days)")
for ax in axs[:, 0]: ax.set_ylabel("Residual, f − f_fit (MPa)")
fig.suptitle("Residuals of the four models", fontsize=11); fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig2_residuals.png"), dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.6))
names = list(models); w = 0.38; x = np.arange(len(names))
b_a = ax.bar(x - w / 2, [results[n_]["pred10"] for n_ in names], w, label="t = 10 d", color="tab:cyan")
b_b = ax.bar(x + w / 2, [results[n_]["pred35"] for n_ in names], w, label="t = 35 d", color="tab:orange")
for bars in (b_a, b_b):
    for r in bars: ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 0.5, f"{r.get_height():.1f}", ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("Predicted strength (MPa)")
ax.set_title("Predictions at t = 10 d and t = 35 d"); ax.grid(axis="y", alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig3_predictions.png"), dpi=200); plt.close(fig)

# ---------------- 6. CONSOLE SUMMARY ----------------
print(f"Area = {AREA:.0f} mm^2; 385 kN -> {385e3/AREA:.3f} MPa")
print("Mean strength by age (MPa):", np.round(mean_strength, 2))
for nm, r in results.items():
    print(f"{nm:12s} {r['equation']:48s} R2={r['R2']:.4f} adjR2={r['adjR2']:.4f} "
          f"RMSE={r['RMSE']:.3f} CV_RMSE={r['CV_RMSE']:.3f} f(10)={r['pred10']:.2f} f(35)={r['pred35']:.2f}")
print("Checks:", json.dumps(checks, indent=1))
