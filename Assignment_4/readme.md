# IAS_A4

## `Instructions for Running`
### 1. Expected files in the directory : `train.csv`, `test.csv`, `eval.csv`(required for testing the model from mobileApp.py)
### 2. First, run model.ipynb
### 3. It will generate `model.pkl`
### 4. Next, I created a `.csv` file in which test dataset will be provided for evaluation. I have named it `eval.csv`.
### 5. Next run `server.py` and `mobileApp.py` in two different terminals
### 6. In `mobileApp.py` the predicted result and expected result will be shown simultaneously.

<br />

## `Roles`
### Role 1 (AI Model developer): model.ipynb as model is developed here
### Role 2 (End App Developer): mobileApp.py as this is making the api call.
### Role 4 (AI Production Platform): server.py as model is being deployed here
### Role 5 (End User): inputs entered

<br />

## `Working Flow`
### 1. First, reading input from `eval.csv` and storing it in a pandas dataframe
### 2. Next, passing the dataframe to the server
### 3. Then, invoking the saved model and using it to predict the result.
### 4. Next, passing the result to the mobileApp and showing it in the mobileApp.