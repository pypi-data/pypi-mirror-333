from galaxy_morph import GalaxyMorph

# Initialize model with local paths
morph = GalaxyMorph(
    model_path="model.keras",  # Ensure the file exists
    encoder_path="../encoder.pkl"  # Ensure the file exists
)

# Test with a sample image
test_image_path = "test.jpg"  # Replace with an actual image path

try:
    prediction = morph.predict(test_image_path)
    print("Prediction:", prediction)
except Exception as e:
    print("Error:", e)
