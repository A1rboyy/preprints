import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LinearRegression

# ==========================================
# CSV LADEN
# ==========================================

df = pd.read_csv(
    "output/full_dataset.csv",
    sep=";"
)

print(df.head())

# ==========================================
# QUESTION 1
# Complexity vs Citations
# ==========================================

print("\n=================================")
print("QUESTION 1")
print("Complexity vs Citation Count")
print("=================================\n")

corr = df["gunning_fog"].corr(
    df["citation_count"]
)

print(
    f"Correlation Complexity vs Citations: {corr}"
)

plt.figure(figsize=(8, 5))

plt.scatter(
    df["gunning_fog"],
    df["citation_count"]
)

# Regressionslinie

x = df["gunning_fog"]
y = df["citation_count"]

z = np.polyfit(x, y, 1)
p = np.poly1d(z)

plt.plot(x, p(x), color="red")

plt.xlabel("Gunning Fog")
plt.ylabel("Citation Count")
plt.title("Complexity vs Citations")

plt.savefig(
    "output/q1_complexity_vs_citations.png"
)

plt.show()

# ==========================================
# QUESTION 2
# Sentence Length vs Citations
# ==========================================

print("\n=================================")
print("QUESTION 2")
print("Sentence Length vs Citation Count")
print("=================================\n")

corr_sentence = df["avg_sentence_length"].corr(
    df["citation_count"]
)

print(
    f"Correlation Sentence Length vs Citations: {corr_sentence}"
)

plt.figure(figsize=(8, 5))

plt.scatter(
    df["avg_sentence_length"],
    df["citation_count"]
)

# Regressionslinie

x = df["avg_sentence_length"]
y = df["citation_count"]

z = np.polyfit(x, y, 1)
p = np.poly1d(z)

plt.plot(x, p(x), color="green")

plt.xlabel("Average Sentence Length")
plt.ylabel("Citation Count")
plt.title("Sentence Length vs Citations")

plt.savefig(
    "output/q2_sentence_length_vs_citations.png"
)

plt.show()

# ==========================================
# QUESTION 3
# Figure Count vs Citations
# ==========================================

print("\n=================================")
print("QUESTION 3")
print("Figure Count vs Citation Count")
print("=================================\n")

# Ausreißer entfernen

df_fig = df[
    df["figure_count"] < 150
]

corr_fig = df_fig["figure_count"].corr(
    df_fig["citation_count"]
)

print(
    f"Correlation Figure Count vs Citations: {corr_fig}"
)

plt.figure(figsize=(8, 5))

plt.scatter(
    df_fig["figure_count"],
    df_fig["citation_count"]
)

# Regressionslinie

x = df_fig["figure_count"]
y = df_fig["citation_count"]

z = np.polyfit(x, y, 1)
p = np.poly1d(z)

plt.plot(x, p(x), color="orange")

plt.xlabel("Figure Count")
plt.ylabel("Citation Count")
plt.title("Figure Count vs Citations")

plt.savefig(
    "output/q3_figure_count_vs_citations.png"
)

plt.show()

# ==========================================
# QUESTION 4
# Published vs Complexity
# ==========================================

print("\n=================================")
print("QUESTION 4")
print("Published vs Complexity")
print("=================================\n")

# OpenAlex type verwenden

df["published_flag"] = (
    df["type"] == "article"
).astype(int)

print(
    df["published_flag"].value_counts()
)

published_mean = df.groupby(
    "published_flag"
)["gunning_fog"].mean()

print(published_mean)

# Balkendiagramm

plt.figure(figsize=(6, 5))

published_mean.plot(kind="bar")

plt.ylabel("Average Gunning Fog")
plt.title("Published vs Complexity")

plt.savefig(
    "output/q4_published_vs_complexity.png"
)

plt.show()

# ==========================================
# MULTIPLE REGRESSION
# ==========================================

print("\n=================================")
print("MULTIPLE LINEAR REGRESSION")
print("=================================\n")

X = df[[
    "gunning_fog",
    "avg_sentence_length",
    "figure_count"
]]

y = df["citation_count"]

model = LinearRegression()

model.fit(X, y)

print("Intercept:", model.intercept_)

for feature, coef in zip(
    X.columns,
    model.coef_
):

    print(feature, ":", coef)

print("\nAnalysis finished.")