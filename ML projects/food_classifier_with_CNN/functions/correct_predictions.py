def correct_predictions(test_batches, predictions):
    correct = 0
    for i, f in enumerate(test_batches.filenames[: len(predictions)]):
        if "slow_food" in f and predictions[i][0] < 0.5:
            correct += 1
        if "fast_food" in f and predictions[i][0] >= 0.5:
            correct += 1

    print("Correct predictions: " + str(correct / len(test_batches.filenames)))
