
# Breast Cancer Detection API

This project provides a Flask-based API for breast cancer detection using a machine learning model.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/breast_cancer_detection.git
   ```
2. Navigate to the project directory:
   ```sh
   cd breast_cancer_detection
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Training the Model
Run the following command to train the model:
```sh
python train_model.py
```

## Running the Application
To start the Flask server, run:
```sh
python run.py
```

## API Endpoints
- `POST /auth/login` - User authentication
- `POST /predict/` - Make a prediction by sending feature data

