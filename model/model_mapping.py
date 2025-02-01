import pandas as pd


def RuleBasedSymptomAlgorithm(input_data):
    dataset = pd.read_csv("data/Combined_Dataset(1).csv")
    input_keywords = [word.strip().lower() for word in input_data.split()]
    results = []

    for index, row in dataset.iterrows():
        comment = row["Comment"].lower()
        total_words = len(comment.split())
        matching_keywords = sum(1 for word in input_keywords if word in comment)

        if matching_keywords > 0:
            density_score = (matching_keywords / total_words) * 100  # Normalize the score
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
        print(f"Specialist: {result['Specialist']}, Score: {result['Score']:.2f}, Condition: {result['Comment']}")
    return seen_specialists
