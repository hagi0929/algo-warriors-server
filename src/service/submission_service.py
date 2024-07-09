import json
import os
import time
from src.repos.submission_repos import SubmissionRepos
import http.client
import ssl
import certifi

class SubmissionService:
    @staticmethod
    def submit_code(code, problem_id: int, programming_language: int):
        testcases = SubmissionRepos.get_input_output(problem_id)

        def submit_batch(submissions):
            payload = json.dumps({"submissions": submissions})

            headers = {
                'x-rapidapi-key': os.environ.get("API_KEY"),
                'x-rapidapi-host': os.environ.get("API_HOST"),
                'Content-Type': "application/json"
            }

            conn.request("POST", "/submissions/batch?base64_encoded=false", payload, headers)
            res = conn.getresponse()
            raw_data = res.read()
            data = json.loads(raw_data)
            
            if res.status != 201:
                conn.close()
                raise Exception(f"Error submitting batch: {data}")
            
            return [val["token"] for val in data]

        def get_results(tokens):
            print("Getting results for tokens")
            tokens_param = "%2C".join(tokens)

            headers = {
                'x-rapidapi-key': os.environ.get("API_KEY"),
                'x-rapidapi-host': os.environ.get("API_HOST"),
                'Content-Type': "application/json"
            }

            poll_interval = 3  # seconds
            max_attempts = 10

            for attempt in range(max_attempts):
                conn.request("GET", f"/submissions/batch?tokens={tokens_param}&base64_encoded=false&fields=*", headers=headers)
                res = conn.getresponse()
                raw_data = res.read()
                result = json.loads(raw_data)
                if res.status != 200:
                    conn.close()
                    raise Exception(f"Error fetching results: {result}")

                all_done = all((submission["status"]["id"] != 1 and submission["status"]["id"]!= 2) for submission in result["submissions"])
                if all_done:
                    return result["submissions"]

                time.sleep(poll_interval)

            conn.close()
            raise TimeoutError("Submission results not ready after polling for a while")

        conn = http.client.HTTPSConnection(os.environ.get("API_HOST"), context=ssl.create_default_context(cafile=certifi.where()))

        # Step 1: Submit the code in batches
        tokens = []
        for i in range(0, len(testcases), 20):
            batch = testcases[i:i + 20]
            submissions = [{
                "language_id": programming_language,
                "source_code": code,
                "stdin": testcase["input"],
                "expected_output": testcase["output"]
            } for testcase in batch]
            tokens.extend(submit_batch(submissions))

        # Step 2: Get the results of the submission in batches
        results = []
        for i in range(0, len(tokens), 20):
            batch_tokens = tokens[i:i + 20]
            results.extend(get_results(batch_tokens))

        conn.close()
        return results
    
    @staticmethod
    def get_available_languages():

        conn = http.client.HTTPSConnection(os.environ.get("API_HOST"), context=ssl.create_default_context(cafile=certifi.where()))

        headers = {
            'x-rapidapi-key': os.environ.get("API_KEY"),
            'x-rapidapi-host': os.environ.get("API_HOST")
        }

        conn.request("GET", "/languages", headers=headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")