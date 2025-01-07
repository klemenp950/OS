class Recommender:
    def __init__(self, predictor):
        self.predictor = predictor
    
    def fit(self, X):
        self.predictor.fit(X)

    def recommend(self, user_id, n=10, rec_seen=False):
        predictions = self.predictor.predict(user_id, rec_seen)
        sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        return {k: v for k, v in sorted_predictions[:n]}