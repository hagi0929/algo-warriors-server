import json
import random
from datetime import datetime, timedelta

# Function to generate random datetime in ISO format
def generate_random_datetime(start, end):
    return (start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))).isoformat()

# Initialize the parameters
num_problems = 165
num_discussions = 400
num_users = 300
start_date = datetime(2024, 6, 19, 10, 0, 0)
end_date = datetime(2024, 6, 30, 10, 0, 0)
lorem_ipsum = "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Facere, voluptates alias incidunt nihil labore praesentium quod sed quo voluptatibus, eaque laudantium amet reprehenderit asperiores aspernatur perspiciatis quis! Nisi, maxime harum."

# Generate discussions
discussions = []
for i in range(num_discussions):
    discussion_id = i + 1
    problem_id = random.randint(1, num_problems)
    user_id = random.randint(1, num_users)
    parentdiscussion_id = random.choice(
        [None] + [d["discussion_id"] for d in discussions if d["problem_id"] == problem_id and d["discussion_id"] < discussion_id]
    )
    created_at = generate_random_datetime(start_date, end_date)

    titleDescr = None;
    if(parentdiscussion_id == None):
        titleDescr = "Discussion " + str(discussion_id)

    discussion = {
        "discussion_id": discussion_id,
        "problem_id": problem_id,
        "parentdiscussion_id": parentdiscussion_id,
        "user_id": user_id,
        "title": titleDescr,
        "content": lorem_ipsum,
        "created_at": created_at,
        "updated_at": created_at
    }
    discussions.append(discussion)

# Write to a JSON file
with open('discussions.json', 'w') as f:
    json.dump(discussions, f, indent=4)

print("discussions.json file has been created with 400 discussions.")

