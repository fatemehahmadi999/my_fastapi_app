# MNIST digit recognition API (FastAPI).
#
# Before you start the server: open a terminal, cd into this folder (app_mnist), then run
#   python asgi.py
# The model path in utilities.load_model is relative to your current working directory.
#
# In Postman: POST http://127.0.0.1:3050/recog_digit → Body → form-data → key "file" → type File.
import uvicorn
from fastapi import FastAPI, UploadFile

from utilities import predict_digit

app = FastAPI()


@app.post("/recog_digit")
async def predict(file: UploadFile = None):
    # `file` is the uploaded image from the client (multipart). The form field name must be "file".
    # `msg` is only for you to read in the debugger later—you could log it or return it if you want.
    msg = "upload successfull!" if file else "Unsuccessfull!"

    # All heavy steps (decode image, load model, predict) live in utilities.predict_digit.
    pred, dec_pred = await predict_digit(file)

    # Returning str(dict) is a quick classroom shortcut; for a real API you would return a dict
    # or a Pydantic model and let FastAPI send proper JSON.
    return str(
        {
            "prediction": dec_pred,
            "probabilities": pred,
        }
    )


if __name__ == "__main__":
    # Port 3050 is chosen so you can run the other lesson app on 8000 at the same machine.
    uvicorn.run(app, host="0.0.0.0", port=3050)
