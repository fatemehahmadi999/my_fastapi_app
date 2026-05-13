# Helpers for the MNIST FastAPI app: turn an uploaded file into a tensor, run Keras, read the digit.
# import io
# import PIL.Image as Image
import keras
import numpy as np
import cv2


async def read_img_from_bytes(file):
    """Turn an UploadFile from FastAPI into a (1, 28, 28, 1) float array for the model."""
    # Read the whole HTTP body as bytes (JPEG/PNG/etc. bytes, not raw MNIST pixels yet).
    image = await file.read()

    # img = Image.open(io.BytesIO(image_bytes))

    # Treat bytes as a 1-D uint8 stream OpenCV can decode.
    image = np.fromstring(image, np.uint8)
    # Decode file bytes into a 2-D grayscale image (single channel height × width).
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    # Neural nets usually expect inputs scaled to roughly [0, 1] when pixels were 0–255.
    image = image / 255

    # Model expects a batch dimension and a channel dimension: (batch, height, width, channels).
    # (1, 28, 28, 1)

    image = np.expand_dims(image, 0)
    image = np.expand_dims(image, -1)

    return image


def load_model(paths_to_weights="model/mnist.keras"):
    """Load saved Keras weights from disk (path is relative to where you started the server)."""
    model = keras.saving.load_model(paths_to_weights)
    # Some TensorFlow/Keras builds error without this line; keep it unless you know you do not need it.
    model.steps_per_execution = 1  # Fixes the TypeError
    model.summary()
    return model


def decode_prediction(prediction):
    """Pick the digit 0–9 with the highest score from the model's softmax row."""
    predictions = prediction[0]

    max_value = np.max(predictions)

    max_value_index = np.where(predictions == max_value)

    return int(max_value_index[0][0])


async def predict_digit(file):
    """Full pipeline: bytes → tensor → predict → winning digit index."""
    image = await read_img_from_bytes(file)

    model = load_model()

    # `pred` shape is like (1, 10): one row of scores for digits 0 through 9.
    pred = model.predict(image)

    dec_pred = decode_prediction(pred)

    print(pred)
    print(dec_pred)

    return list(pred), dec_pred
