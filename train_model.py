import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("=================================")
print("AI Compression Model Training")
print("=================================")

# ----------------------------
# Load Dataset
# ----------------------------
print("\nLoading dataset...")

df = pd.read_csv("training_data.csv")

print("Dataset loaded successfully!")
print("Total Rows:", len(df))
print(df.head())

# ----------------------------
# Feature Selection
# ----------------------------
print("\nSelecting Features...")

X = df[["size", "entropy", "unique_bytes"]]
y = df["best_method"]

# ----------------------------
# Encode Labels
# ----------------------------
print("\nEncoding Labels...")

le = LabelEncoder()
y_encoded = le.fit_transform(y)

print("Available Compression Methods:", list(le.classes_))

# ----------------------------
# Train Test Split
# ----------------------------
print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42
)

print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ----------------------------
# Train Model
# ----------------------------
print("\nTraining RandomForest Model...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model Training Completed!")

# ----------------------------
# Evaluate Model
# ----------------------------
print("\nEvaluating Model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=le.classes_,
    zero_division=0
))

# ----------------------------
# Save Model (JOBLIB)
# ----------------------------
print("\nSaving Model...")

joblib.dump(model, "compression_model.joblib")
joblib.dump(le, "label_encoder.joblib")

print("Model saved → compression_model.joblib")
print("Encoder saved → label_encoder.joblib")

print("\n✅ Training Pipeline Completed Successfully")