import tensorflow as tf
import numpy as np
import cv2
import joblib
import os
import requests
import warnings
from sklearn.preprocessing import LabelEncoder

class GalaxyMorph:
    def __init__(self, 
                 model_url=None, 
                 model_path="../model.keras", 
                 encoder_path="../encoder.pkl", 
                 target_size=(128, 128)):
        """
        Initialize the model and label encoder.

        Parameters:
        - model_url (str): URL to download the model if not found.
        - model_path (str): Local path to the saved model file.
        - encoder_path (str): Local path to the label encoder file.
        - target_size (tuple): Target size for image preprocessing.
        """
        self.target_size = target_size
        self.model_path = model_path
        self.encoder_path = encoder_path

        # Ensure model is downloaded
        if not os.path.exists(model_path):
            self._download_file(model_url, model_path, "model")

        # Load the trained model
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {model_path}: {e}")

        # Load the label encoder (optional)
        if os.path.exists(encoder_path):
            self.label_encoder = joblib.load(encoder_path)
            if not isinstance(self.label_encoder, LabelEncoder):
                raise ValueError("Error: encoder.pkl is not a valid LabelEncoder object.")
        else:
            self.label_encoder = None
            warnings.warn("Label encoder not found. Predictions will be returned as class indices.")

    def _download_file(self, url, save_path, file_type):
        """Download a file (model or encoder) from a given URL."""
        print(f"Downloading {file_type} from {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"{file_type.capitalize()} download complete!")
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download {file_type} from {url}: {e}")

    def preprocess_image(self, image):
        """Preprocess an image (file path or NumPy array) for model input."""
        if isinstance(image, str):  # Load from file path
            if not os.path.exists(image):
                raise FileNotFoundError(f"Error: Image not found at {image}")
            image = cv2.imread(image)
            if image is None:
                raise ValueError(f"Error: Could not load image from {image}")
        elif not isinstance(image, np.ndarray):
            raise TypeError("Input must be a file path or a NumPy array.")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, self.target_size)
        image = image / 255.0  # Normalize
        return np.expand_dims(image, axis=0)

    def predict(self, image):
        """Predict galaxy morphology."""
        processed_image = self.preprocess_image(image)
        prediction = self.model.predict(processed_image)

        if self.label_encoder:
            try:
                return self.label_encoder.inverse_transform([np.argmax(prediction)])[0]
            except ValueError:
                warnings.warn("Warning: Unable to decode prediction. Returning class index instead.")
        
        return np.argmax(prediction)
