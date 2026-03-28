from sklearn.metrics import accuracy_score, classification_report

def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)

    report = classification_report(y_test, preds,zero_division=0)

    return {
        "accuracy": acc,
        "report": report
    }