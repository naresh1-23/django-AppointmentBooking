import pandas as pd


def RuleBasedSymptomAlgorithm(input_data):
    dataset = pd.read_csv("data/balanced_train_dataset.csv")
    input_keywords = [word.strip().lower() for word in input_data.split()]
    results = []

    for index, row in dataset.iterrows():
        comment = row["Comment"].lower()
        total_words = len(comment.split())
        matching_keywords = sum(
            1 for word in input_keywords if word in comment)

        if matching_keywords > 0:
            density_score = (matching_keywords / total_words) * \
                100  # Normalize the score
            results.append({
                "Specialist": row["Specialist"],
                "Score": density_score,
                "Comment": row["Comment"]
            })

    results = sorted(results, key=lambda x: -x["Score"])
    distinct_results = []
    seen_specialists = []

    for result in results:
        if result["Specialist"] not in seen_specialists:
            distinct_results.append(result)
            seen_specialists.append(result["Specialist"])
        if len(distinct_results) >= 3:
            break
    for result in distinct_results:
        print(
            f"Specialist: {result['Specialist']}, Score: {result['Score']:.2f}, Condition: {result['Comment']}")
    return seen_specialists


def evaluate_accuracy(algorithm=RuleBasedSymptomAlgorithm, test_file="data/balanced_test_dataset.csv"):
    test_data = pd.read_csv(test_file)
    correct_predictions = 0

    for index, row in test_data.iterrows():
        input_data = row["Comment"]
        expected_specialists = set(row["Specialist"].split(","))
        predicted_specialists = set(algorithm(input_data))

        # Check for intersection between predicted and expected specialists
        if predicted_specialists & expected_specialists:
            correct_predictions += 1

    total_cases = len(test_data)
    accuracy = (correct_predictions / total_cases) * \
        100 if total_cases > 0 else 0
    print(f"Accuracy: {accuracy:.2f}%")
    return accuracy


def calculate_density_and_keyword_matching(input_data, dataset):
    # Preprocess input keywords
    input_keywords = set(word.strip().lower() for word in input_data.split())

    results = []
    seen_specialists = set()  # Track unique specialists

    for index, row in dataset.iterrows():
        # Preprocess the comment (specialist case) into keywords
        comment_keywords = set(row["Comment"].lower().split())

        # Calculate matching keywords
        matching_keywords = len(input_keywords & comment_keywords)

        # Calculate total keywords in the comment
        total_keywords = len(comment_keywords)

        # Calculate density score
        density_score = (matching_keywords / total_keywords) * \
            100 if total_keywords > 0 else 0

        # Only add distinct specialists with their highest score if density is >= 1%
        if row["Specialist"] not in seen_specialists and matching_keywords > 0:
            results.append({
                "Specialist": row["Specialist"],
                "Matching Keywords": matching_keywords,
                "Total Keywords": total_keywords,
                "Density Score (%)": density_score,
                "Input Symptoms": input_data
            })
            seen_specialists.add(row["Specialist"])

    # Sort results by density score in descending order
    sorted_results = sorted(results, key=lambda x: -x["Density Score (%)"])
    return sorted_results


# Load the dataset from your balanced train dataset
dataset = pd.read_csv("data/high_density_dataset.csv")

# Calculate density and keyword matching
density_results = calculate_density_and_keyword_matching(
    "i am experiencing high cholesterol level are very high for few hours.it seems to worsen after exercising.", dataset)

# if density_results:
# Display the top 5 distinct specialists
#     for result in density_results[:5]:
#         print(f"Input Symptoms: {result['Input Symptoms']}, "
#               f"Specialist: {result['Specialist']}, "
#               f"Matching Keywords: {result['Matching Keywords']}, "
#               f"Total Keywords: {result['Total Keywords']}, "
#               f"Density Score: {result['Density Score (%)']:.2f}%")
# else:
#     print("No specialists found meeting the criteria. Consider lowering the density threshold or adjusting input keywords.")
