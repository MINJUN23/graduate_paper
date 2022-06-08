import joblib
from tensorflow import keras

model_name = "5-160-1_e:10000_b:100"
model = keras.models.load_model(f'MLP/MODELS/{model_name}.h5')
scaler = joblib.load("MLP/MLP.scaler.gz")
