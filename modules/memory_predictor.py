import numpy as np
from sklearn.linear_model import LinearRegression


class MemoryPredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train_and_predict(self, history_usage, future_steps=5):
        """
        :param history_usage: List of RAM percentages over time, e.g., [45, 48, 50, 52, 55]
        :param future_steps: Number of future intervals to forecast
        """
        if len(history_usage) < 3:
            return "Need at least 3 historical points to predict."

        X = np.array(range(len(history_usage))).reshape(-1, 1)
        y = np.array(history_usage)

        self.model.fit(X, y)

        future_X = np.array(range(len(history_usage), len(history_usage) + future_steps)).reshape(-1, 1)
        predictions = self.model.predict(future_X)
        
        # Clip predictions between 0% and 100%
        predictions = np.clip(predictions, 0, 100)
        return [round(p, 2) for p in predictions]


if __name__ == "__main__":
    ram_data = [30.5, 32.0, 35.1, 40.2, 42.8, 45.0, 49.3]
    predictor = MemoryPredictor()
    next_preds = predictor.train_and_predict(ram_data, future_steps=3)
    print("Historical RAM:", ram_data)
    print("Next 3 Predicted RAM Usage (%):", next_preds)