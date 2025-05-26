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

# --- U-Net Implementation (Keras) ---
class UNetModel:
    """
    Minimal Keras U-Net for semantic segmentation.
    """
    def __init__(self, input_shape=(128, 128, 3), n_classes=1):
        self.input_shape = input_shape
        self.n_classes = n_classes
        self.model = self.build_unet()

    def build_unet(self):
        from tensorflow.keras import layers, models
        inputs = layers.Input(self.input_shape)
        # Encoder
        c1 = layers.Conv2D(16, 3, activation='relu', padding='same')(inputs)
        c1 = layers.Conv2D(16, 3, activation='relu', padding='same')(c1)
        p1 = layers.MaxPooling2D()(c1)
        c2 = layers.Conv2D(32, 3, activation='relu', padding='same')(p1)
        c2 = layers.Conv2D(32, 3, activation='relu', padding='same')(c2)
        p2 = layers.MaxPooling2D()(c2)
        # Bottleneck
        b = layers.Conv2D(64, 3, activation='relu', padding='same')(p2)
        b = layers.Conv2D(64, 3, activation='relu', padding='same')(b)
        # Decoder
        u1 = layers.UpSampling2D()(b)
        u1 = layers.concatenate([u1, c2])
        c3 = layers.Conv2D(32, 3, activation='relu', padding='same')(u1)
        c3 = layers.Conv2D(32, 3, activation='relu', padding='same')(c3)
        u2 = layers.UpSampling2D()(c3)
        u2 = layers.concatenate([u2, c1])
        c4 = layers.Conv2D(16, 3, activation='relu', padding='same')(u2)
        c4 = layers.Conv2D(16, 3, activation='relu', padding='same')(c4)
        outputs = layers.Conv2D(self.n_classes, 1, activation='sigmoid')(c4)
        model = models.Model(inputs, outputs)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, X, y, epochs=10, batch_size=8):
        """Train the U-Net model on input images X and masks y."""
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)

    def predict(self, X):
        """Run inference on input images X and return predicted masks."""
        preds = self.model.predict(X)
        return (preds > 0.5).astype(np.uint8)

    def save(self, path):
        """Save the trained U-Net model to disk."""
        self.model.save(path)

    @staticmethod
    def load(path):
        from tensorflow.keras.models import load_model
        unet = UNetModel()
        unet.model = load_model(path)
        return unet 