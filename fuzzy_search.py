import sys
import json
from rapidfuzz import process, fuzz
import time

# Sample FAQ data (replace with your actual FAQ data)
faqs = [
    {"question": "What is the process for admission into Saras AI Institute?", "answer": "The admission process..."},
    {"question": "How do I apply for a course?", "answer": "You can apply for a course by..."},
    {"question": "What is the curriculum structure at Saras AI?", "answer": "The curriculum consists of..."},
    # Add more FAQs as needed
]

def rapidfuzz_search_with_threshold(query, faqs, threshold=0.7):
    questions = [faq['question'] for faq in faqs]

    # Get top matches using RapidFuzz
    matches = process.extract(query, questions, scorer=fuzz.ratio)

    # Calculate the highest match score
    max_score = matches[0][1] if matches else 0  # matches[0][1] is the score of the top match

    # Retrieve full FAQ data for matches meeting the threshold
    results = []
    for match_text, score, idx in matches:
        if score >= max_score * threshold:  # Include matches within 70% of the highest score
            results.append({
                "question": faqs[idx]['question'],
                "answer": faqs[idx]['answer'],
                "score": score
            })

    # Sort results in descending order of score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results

# Main entry point for receiving the query from Node.js
if __name__ == "__main__":
    # Receive the query from Node.js (via command-line argument)
    query = sys.argv[1]
    
    # Run the search
    start_time = time.time()
    result = rapidfuzz_search_with_threshold(query, faqs, threshold=0.7)
    
    # Print the results as JSON for Node.js to process
    print(json.dumps(result))

    # Optionally print the time taken
    end_time = time.time()
    print(f"Time Taken: {end_time - start_time:.2f} seconds", file=sys.stderr)
