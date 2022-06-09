import joblib
from tensorflow import keras

model_name = "4-320-1_e:20000_b:100"
model = keras.models.load_model(f'MLP/MODELS/{model_name}.h5')
scaler = joblib.load("MLP/MLP.scaler.gz")
