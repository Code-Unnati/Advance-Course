import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
# 1. Load the dataset
df = pd.read_excel("customer_segmentation.xlsx")
# 2. Select only the behavioral features used for clustering.
# CustomerID is an identifier, not a feature, and must be excluded, or KMeans would cluster on customer number rather than purchasing behavior.
X = df[["AnnualIncome", "SpendingScore"]]
 
# 3. Scale the features before clustering
# KMeans groups points by Euclidean distance. AnnualIncome (roughly 18-150) and SpendingScore (roughly 5-100) sit on different numeric ranges; without scaling, whichever column happens to have the larger spread would dominate the distance calculation and skew the clusters.
# Bundling the scaler and the clustering model together in a Pipeline also means app.py automatically applies the exact same scaling at prediction time - it cannot forget to.
model = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("kmeans", KMeans(n_clusters=3, random_state=42, n_init=10)),
])
 
# 4. Fit the pipeline
model.fit(X)
 
# 5. Save the trained pipeline (scaler + clustering model)
joblib.dump(model, "customer_segment_model.pkl")
print("Model Saved Successfully")