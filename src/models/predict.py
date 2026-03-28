def predict(model, sample_df):
    preds = model.predict(sample_df)
    return preds