import tensorflow as tf
import numpy as np
import cv2
import warnings
import joblib
import importlib.resources as pkg_resources
import galaxy_morph  # Import package for resource handling
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

class GalaxyMorph:
    def __init__(self, target_size=(128, 128)):
        """
        Initialize the model and label encoder.
        """
        self.target_size = target_size
        
        # Load model from package resources
        try:
            with pkg_resources.files("galaxy_morph").joinpath("model.keras") as model_path:
                self.model = tf.keras.models.load_model(str(model_path))
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

        # Load label encoder
        try:
            with pkg_resources.path(galaxy_morph, "encoder.pkl") as encoder_path:
                self.label_encoder = joblib.load(str(encoder_path))
        except Exception:
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

    def preprocess_image(self, image):
        """Preprocess an image for model input."""
        if isinstance(image, str):
            image = cv2.imread(image)
            if image is None:
                raise ValueError("Error: Could not load image")
        elif not isinstance(image, np.ndarray):
            raise TypeError("Input must be a file path or a NumPy array.")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, self.target_size)
        image = image / 255.0
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
        predicted_class, galaxy_type, subclass, confidence = self.predict(image_path)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image)
        plt.title(f"Galaxy Type: {galaxy_type} \n\n Subclass: {subclass} \n Confidence: {confidence:.2f}", fontsize=14)
        plt.axis('off')
        plt.show()
