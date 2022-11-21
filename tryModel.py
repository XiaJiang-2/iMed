import numpy as np
from tensorflow.keras.models import load_model

model_15 = load_model('imedbot_model_five_input_15.h5')
input = [[0, 0, 0, 0, 0]]  # why we need to use [[0,0,0,0,0]] not [0,0,0,0,0]
input = np.array(input)
print(input)
res = model_15.predict(input)
print(res)

input = [[0,	0	,1	,1	,0	,0	,1	,2	,2	,5	,0	,0	,2	,0	,0	,0	,0	,1]]
model_10 = load_model('model10.h5')
input = np.array(input)
print(input)
res = model_10.predict(input)
print(res)

input = [[0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0]]
model_5 = load_model('model5.h5')
input = np.array(input)
print(input)
res = model_5.predict(input)
print(res)
