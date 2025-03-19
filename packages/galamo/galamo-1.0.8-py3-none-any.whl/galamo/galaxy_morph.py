import tensorflow as tf
import numpy as np
import cv2
import os
import warnings
import joblib
import matplotlib.pyplot as plt

class GalaxyMorph:
    def __init__(self, target_size=(128, 128)):
        """
        Initialize the model and label encoder.
        """
        self.target_size = target_size
        package_dir = os.path.dirname(__file__)  # Get package directory
        
        # Load model
        self.model_path = os.path.join(package_dir, "model.keras")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        self.model = tf.keras.models.load_model(self.model_path)

        # Load label encoder
        self.encoder_path = os.path.join(package_dir, "encoder.pkl")
        if os.path.exists(self.encoder_path):
            self.label_encoder = joblib.load(self.encoder_path)
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

    def preprocess_image(self, image):
        """Preprocess an image for model input."""
        if isinstance(image, str):
            if not os.path.exists(image):
                raise FileNotFoundError(f"Image file not found: {image}")
            image = cv2.imread(image)

        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image input. Provide a valid file path or a NumPy array.")

        if len(image.shape) == 2:  # Convert grayscale to RGB
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # Convert RGBA to RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        else:
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
