# train_model.py
# Functions for training or loading ML models (e.g., U-Net, Random Forest)

def train_rf_classifier(ndvi, blue, veg_mask):
    """
    Train a Random Forest classifier to predict vegetation using NDVI and blue band.
    veg_mask: boolean mask (True = vegetation)
    Returns trained model.
    """
    from sklearn.ensemble import RandomForestClassifier
    X = np.stack([ndvi.ravel(), blue.ravel()], axis=1)
    y = veg_mask.ravel().astype(int)
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    return clf

def save_model(model, path):
    import joblib
    joblib.dump(model, path)

def load_model(path):
    import joblib
    return joblib.load(path)

def predict_vegetation(model, ndvi, blue):
    X = np.stack([ndvi.ravel(), blue.ravel()], axis=1)
    y_pred = model.predict(X)
    return y_pred.reshape(ndvi.shape)

import numpy as np 