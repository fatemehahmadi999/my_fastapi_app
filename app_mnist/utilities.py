# import io
# import PIL.Image as Image
import keras
import numpy as np
import cv2

async def read_img_from_bytes(file):
    image = await file.read()

    # img = Image.open(io.BytesIO(image_bytes))

    image = np.fromstring(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    image = image / 255

    # (1, 28, 28, 1)

    image = np.expand_dims(image, 0)
    image = np.expand_dims(image, -1)

    return image

def load_model(paths_to_weights="model/mnist.keras"):
    model = keras.saving.load_model(paths_to_weights)
    model.steps_per_execution = 1  # Fixes the TypeError
    model.summary()
    return model

def decode_prediction(prediction):
    predictions = prediction[0]

    max_value = np.max(predictions)

    max_value_index = np.where(predictions == max_value)

    return int(max_value_index[0][0])

async def predict_digit(file):

    image = await read_img_from_bytes(file)

    model = load_model()

    pred = model.predict(image)

    dec_pred = decode_prediction(pred)

    print(pred)
    print(dec_pred)

    return list(pred), dec_pred

