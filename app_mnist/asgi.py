import cv2
from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI
import uvicorn

from utilities import read_img_from_bytes, predict_digit

app = FastAPI()

@app.post("/recog_digit")
async def predict(file: UploadFile = None):
    
    msg = "upload successfull!" if file else "Unsuccessfull!"

    pred, dec_pred = await predict_digit(file)

    return str(
        {
            "prediction": dec_pred,
            "probabilities": pred
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3050)
