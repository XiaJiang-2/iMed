import numpy as np
from tensorflow.keras.models import load_model
model_15 = load_model('imedbot_model_five_input_15.h5')
input = [[0,0,0,0,0]]# why we need to use [[0,0,0,0,0]] not [0,0,0,0,0]
input = np.array(input)
print(input)
res = model_15.predict(input)
print(res)