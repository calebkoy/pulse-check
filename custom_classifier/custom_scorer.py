def average_correct_predictions(y_true, y_predictions):
  correct_predictions = (y_predictions == y_true)    
  return correct_predictions.astype(int).mean()