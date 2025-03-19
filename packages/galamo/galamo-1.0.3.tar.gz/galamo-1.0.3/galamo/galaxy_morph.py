import tensorflow as tf
import numpy as np
import cv2
import joblib
import os
import requests
import warnings
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

class GalaxyMorph:
    def __init__(self, 
                 model_url=None, 
                 model_path="model.keras", 
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
        if not os.path.exists(model_path) and model_url:
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
            warnings.warn("Label encoder not found. Predictions will be class indices.")

        # Class mapping for labels
        self.class_mapping = {
            0: ("Merger Galaxy", "Disturbed Galaxy"),
            1: ("Merger Galaxy", "Merging Galaxy"),
            2: ("Elliptical Galaxy", "Round Smooth Galaxy"),
            3: ("Elliptical Galaxy", "In-between Round Smooth Galaxy"),
            4: ("Elliptical Galaxy", "Cigar Shaped Smooth Galaxy"),
            5: ("Spiral Galaxy", "Barred Spiral Galaxy"),
            6: ("Spiral Galaxy", "Unbarred Tight Spiral Galaxy"),
            7: ("Spiral Galaxy", "Unbarred Loose Spiral Galaxy"),
            8: ("Spiral Galaxy", "Edge-on Galaxy without Bulge"),
            9: ("Spiral Galaxy", "Edge-on Galaxy with Bulge")
        }

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

        predicted_class_index = np.argmax(prediction)
        confidence = np.max(prediction)

        galaxy_type, subclass = self.class_mapping.get(predicted_class_index, ("Unknown", "Unknown"))

        return predicted_class_index, galaxy_type, subclass, confidence

    def display_prediction(self, image_path):
        """Display the image with predicted galaxy classification."""
        if not os.path.exists(image_path):
            print(f"Error: Image not found at {image_path}")
            return
        
        predicted_class, galaxy_type, subclass, confidence = self.predict(image_path)

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        plt.imshow(image)
        plt.title(f"Galaxy Type: {galaxy_type} \n\n Subclass: {subclass} \n Confidence: {confidence:.2f}", fontsize=14, pad=20)
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )

    if image_path:
        galaxy_classifier = GalaxyMorph()
        galaxy_classifier.display_prediction(image_path)
    else:
        print("No image selected.")
