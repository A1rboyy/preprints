import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression

# CSV laden
df = pd.read_csv(
    "output/full_dataset.csv",
    sep=";"
)

print(df.head())

plt.figure(figsize=(8, 5))

plt.scatter(
    df["gunning_fog"],
    df["citation_count"]
)

plt.xlabel("Gunning Fog")
plt.ylabel("Citation Count")
plt.title("Complexity vs Citations")

plt.savefig("output/q1_complexity_vs_citations.png")

# ==========================================
# QUESTION 2
# Sind Papers mit kürzeren Sätzen erfolgreicher?
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

plt.xlabel("Average Sentence Length")
plt.ylabel("Citation Count")
plt.title("Sentence Length vs Citations")

plt.savefig("output/q2_sentence_length_vs_citations.png")

# ==========================================
# QUESTION 3
# Sind veröffentlichte Papers einfacher?
# ==========================================

print("\n=================================")
print("QUESTION 3")
print("Published vs Complexity")
print("=================================\n")

# published = alles außer preprint

df["published"] = df["type"] != "preprint"

published_mean = df.groupby("published")[
    "gunning_fog"
].mean()

print(published_mean)

# Balkendiagramm

plt.figure(figsize=(6, 5))

published_mean.plot(kind="bar")

plt.ylabel("Average Gunning Fog")
plt.title("Published vs Complexity")

plt.savefig("output/q3_published_vs_complexity.png")

# ==========================================
# SIMPLE REGRESSION
# ==========================================

print("\n=================================")
print("LINEAR REGRESSION")
print("=================================\n")

X = df[["gunning_fog"]]
y = df["citation_count"]

model = LinearRegression()
model.fit(X, y)

print("Intercept:", model.intercept_)
print("Coefficient:", model.coef_[0])

print("\nAnalysis finished.")