import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Fetch data
usdinr = yf.download("INR=X", start="2023-01-01", end="2024-12-31")
crude = yf.download("CL=F", start="2023-01-01", end="2024-12-31")

usdinr = usdinr[["Close"]].rename(columns={"Close": "USD_INR"})
crude = crude[["Close"]].rename(columns={"Close": "Crude_Oil"})

df = pd.merge(usdinr, crude, left_index=True, right_index=True)
df.columns = ["USD_INR", "Crude_Oil"]

df["USD_INR_MA30"] = df["USD_INR"].rolling(window=30).mean()
df["Crude_MA30"] = df["Crude_Oil"].rolling(window=30).mean()

correlation = df["USD_INR"].corr(df["Crude_Oil"])
print(f"Correlation: {correlation:.4f}")

# Key macro events with colors
events = {
    "2023-02-01": ("Fed +25bps", "#FF6B6B"),
    "2023-06-14": ("Fed Pause", "#FFD93D"),
    "2023-10-04": ("OPEC Cut\n(Crude peaks)", "#6BCB77"),
    "2024-03-20": ("Fed holds\n5.25%", "#FF6B6B"),
    "2024-09-18": ("Fed cuts\n-50bps", "#4D96FF"),
}

# Dark mode style
plt.style.use("dark_background")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True)
fig.patch.set_facecolor("#0D1117")
ax1.set_facecolor("#161B22")
ax2.set_facecolor("#161B22")

fig.suptitle("USD/INR vs Crude Oil: Does the Correlation Hold? (2023–2024)",
             fontsize=15, fontweight="bold", color="white", y=0.98)

# USD/INR
ax1.plot(df.index, df["USD_INR"], color="#4D96FF", linewidth=1, alpha=0.5, label="USD/INR")
ax1.plot(df.index, df["USD_INR_MA30"], color="#00D4FF", linewidth=2.5, label="30-Day MA")
ax1.set_ylabel("USD/INR Rate", color="white", fontsize=11)
ax1.tick_params(colors="white")
ax1.legend(loc="upper left", facecolor="#0D1117", edgecolor="gray", labelcolor="white")
ax1.grid(True, alpha=0.15, color="gray")
for spine in ax1.spines.values():
    spine.set_edgecolor("#30363D")

# Correlation box
ax1.annotate(f"Pearson Correlation: {correlation:.4f}\nWeak negative — crude & INR\nless linked than assumed",
             xy=(0.02, 0.12), xycoords="axes fraction",
             fontsize=9, color="white",
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#FF6B6B", alpha=0.3, edgecolor="#FF6B6B"))

# Crude Oil
ax2.plot(df.index, df["Crude_Oil"], color="#FFD93D", linewidth=1, alpha=0.5, label="Crude Oil (USD)")
ax2.plot(df.index, df["Crude_MA30"], color="#FF9F1C", linewidth=2.5, label="30-Day MA")
ax2.set_ylabel("Crude Oil Price (USD)", color="white", fontsize=11)
ax2.set_xlabel("Date", color="white", fontsize=11)
ax2.tick_params(colors="white")
ax2.legend(loc="upper right", facecolor="#0D1117", edgecolor="gray", labelcolor="white")
ax2.grid(True, alpha=0.15, color="gray")
for spine in ax2.spines.values():
    spine.set_edgecolor("#30363D")

# Event markers
for date_str, (label, color) in events.items():
    date = pd.Timestamp(date_str)
    if date > df.index[0] and date < df.index[-1]:
        ax1.axvline(x=date, color=color, linestyle="--", linewidth=1.5, alpha=0.9)
        ax2.axvline(x=date, color=color, linestyle="--", linewidth=1.5, alpha=0.9)
        ax2.text(date, df["Crude_Oil"].min() + 0.5, label,
                fontsize=8, color=color, ha="center", va="bottom", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#0D1117", edgecolor=color, alpha=0.9))

# Footer
fig.text(0.99, 0.01, "Data: Yahoo Finance | Built with Python (yfinance, pandas, matplotlib)",
         ha="right", fontsize=8, color="gray")

ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45, color="white")
plt.tight_layout()
plt.savefig("forex_crude_analysis.png", dpi=150, bbox_inches="tight", facecolor="#0D1117")
plt.show()

print("\nChart saved!")


