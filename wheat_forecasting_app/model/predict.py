class GRUPredictor:
    def __init__(self, model, feature_scaler, target_scaler, feature_columns):
        self.model = model
        self.feature_scaler = feature_scaler
        self.target_scaler = target_scaler
        self.feature_columns = feature_columns

    def prepare_sequence(self, df):
        df = df[self.feature_columns]
        seq = df.tail(24)
        seq_scaled = self.feature_scaler.transform(seq)
        seq_scaled = seq_scaled.reshape(1, 24, len(self.feature_columns))
        return seq_scaled

    def predict(self, df):
        X_input = self.prepare_sequence(df)
        scaled_pred = self.model.predict(X_input, verbose=0)
        pred_return = self.target_scaler.inverse_transform(scaled_pred)[0, 0]
        last_price = df["india_price"].iloc[-1]
        next_price = last_price * (1 + pred_return)
        return {
            "predicted_return": pred_return,
            "predicted_price": next_price,
        }