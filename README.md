# my_fastapi_app

This repo is for **learning FastAPI** with two small servers you can run on your machine. You do not need a front end for the APIs: use **Postman** to send requests and read responses. For `**GET /`** on the main app you can still use a browser if you like.


| Part | Folder           | What it does                                                                  | Default port |
| ---- | ---------------- | ----------------------------------------------------------------------------- | ------------ |
| A    | `**app/**`       | Hello page on `/`, plus simple **form** vs **JSON** profile routes            | **8000**     |
| B    | `**app_mnist/`** | Upload an image; the server runs an **MNIST** model and returns a digit guess | **3050**     |


Open `**app/asgi.py`** and `**app_mnist/asgi.py**` and read the comments in the code—they explain what each piece is doing.

---

## 1. Install packages

Use **Python 3**.

### Packages for `**app/`** (hello + profiles)

```bash
pip install fastapi
pip install uvicorn
pip install python-multipart
```

`python-multipart` is needed when you use **form** data or **file uploads** with FastAPI. **Pydantic** still comes in automatically with FastAPI (used for the JSON profile body).

### Packages for `**app_mnist/`** (digit recognition)

Install the `**app/**` packages above first (FastAPI server and file uploads). Then add the ML and image stack:

```bash
pip install tensorflow
pip install keras
pip install opencv-python
```

On PyPI, OpenCV is the package `**opencv-python**`; in Python you still `import cv2`. **TensorFlow** is a large download and may pull in **NumPy** and other dependencies automatically. Only install this block if you are working on the digit-recognition part.

---

## 2. Run the main app (`app/`)

From the **root** of this repository (the folder that contains `app/`):

```bash
python app/asgi.py
```

**Tip:** Start this from the **repo root** so imports like `app.asgi` work.

```bash
uvicorn app.asgi:app --host 0.0.0.0 --port 8000
```

### Testing the `**app/**` APIs in Postman

Create requests against base URL `**http://127.0.0.1:8000**` (or `http://localhost:8000`).


| What         | Method | URL                                  | Postman settings                                                                                  |
| ------------ | ------ | ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| Home (GET)   | GET    | `http://127.0.0.1:8000/`             | No body. Send and read the HTML response.                                                         |
| Home (POST)  | POST   | `http://127.0.0.1:8000/`             | No body (unless you add one for practice).                                                        |
| Form profile | POST   | `http://127.0.0.1:8000/profile/form` | **Body** → **x-www-form-urlencoded**. Keys: `**name`** (Text), `**age**` (Text, integer as text). |
| JSON profile | POST   | `http://127.0.0.1:8000/profile/json` | **Body** → **raw** → **JSON**. Example: `{"name":"Ada","age":30}`.                                |


If you send bad JSON or `age` as a string, you may get **422**—validation failed; fix the body and send again.

---

## 3. Run the MNIST app (`app_mnist/`)

The model path in code is `**model/mnist.keras`** relative to your **current working directory**. Run from **inside** `app_mnist/`:

```bash
cd app_mnist
python asgi.py
```

Base URL for Postman: `**http://127.0.0.1:3050**`

### Testing `**POST /recog_digit**` in Postman

1. Method **POST**, URL `**http://127.0.0.1:3050/recog_digit`**.
2. Open **Body** → select **form-data** (multipart form, not URL-encoded).
3. Add a row: **Key** `**file`** (exact spelling—must match the route parameter). Hover the type on the right and set it to **File** (not Text).
4. **Choose Files** and pick a small digit image (try anything under `**app_mnist/test_images/`** in this repo).
5. Send. The response body is a **string** that looks like a dict: predicted digit plus probability list.

### How the image flows through the code (upload → model → response)

Follow this path in order; each step matches a function in `**app_mnist/asgi.py`** or `**app_mnist/utilities.py**`.

1. `**predict()**` in `**asgi.py**` (FastAPI route)
  Postman sends `**POST /recog_digit**` with a **multipart** body. FastAPI wraps the uploaded bytes in an `**UploadFile`** named `**file**`. The route is `**async**` so it can `**await**` the pipeline. It calls `**await predict_digit(file)**` and returns `**str({...})**` with keys `**prediction**` (digit 0–9) and `**probabilities**` (10 scores).
2. `**predict_digit()**` in `**utilities.py**` (orchestrator)
  Runs: **decode bytes → shape for the model → forward pass → pick digit**. It calls `**read_img_from_bytes`**, `**load_model**`, `**model.predict**`, and `**decode_prediction**`, then returns `**pred**` and `**dec_pred**`. `**print**` lines help you watch values in the server terminal.
3. `**read_img_from_bytes()**` in `**utilities.py**` (bytes → model input)
  - `**await file.read()**` — raw upload bytes from Postman.  
  - `**np.fromstring(..., np.uint8)**` — byte buffer for the decoder.  
  - `**cv2.imdecode(..., IMREAD_GRAYSCALE)**` — decoded 2-D grayscale image (MNIST-sized patch).  
  - `**image / 255**` — pixels roughly in **[0, 1]**.  
  - `**np.expand_dims`** twice — shape `**(1, 28, 28, 1)**` (batch, H, W, channels) for `**model.predict**`.
4. `**load_model()**` in `**utilities.py**`
  `**keras.saving.load_model("model/mnist.keras")**` loads weights relative to **cwd** (why you `**cd app_mnist`** first). `**steps_per_execution = 1**` avoids a known `**TypeError**`. `**model.summary()**` prints to the server log; this sample reloads the model **every request** (easy to learn, slow in production).
5. `**model.predict(image)`**
  Output includes a row of **10** class scores (digits **0–9**).
6. `**decode_prediction()`** in `**utilities.py**`
  `**prediction[0]**`, find **max** score, `**np.where`** → index **0–9** = `**dec_pred`**.
7. **Back in `predict()`** in `**asgi.py**`
  Builds the small **dict**, `**str(...)`**, returned as the HTTP body Postman shows.

---

## 4. Things to notice while you read the code

- **Same URL, different method:** `GET /` and `POST /` are different routes because the HTTP method is different.
- **Form vs JSON:** `/profile/form` vs `/profile/json` is the same *idea* (name + age), but the **body type** in Postman must match (**form-urlencoded** vs **raw JSON**).
- **Two functions named `read_root`:** FastAPI registered both routes at import time. Clearer names in your own projects help readers.

---

