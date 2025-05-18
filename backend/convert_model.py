import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the legacy .h5 model
model = load_model("plantl.h5")

# Save it in the modern .keras format
model.save("plantl_fixed.keras", save_format="keras")

print("Model successfully converted to 'plantl_fixed.keras'")
