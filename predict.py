# predict.py
import joblib

# Load model and scaler (done only once when app starts)
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

def predict(data):
    """
    Scales the data and makes predictions using the trained model.
    
    Args:
        data (pd.DataFrame or np.array): Preprocessed feature matrix.
        
    Returns:
        tuple: (predictions, anomaly scores)
    """
    scaled_data = scaler.transform(data)
    predictions = model.predict(scaled_data)
    scores = model.decision_function(scaled_data)
    
    return predictions, scores
