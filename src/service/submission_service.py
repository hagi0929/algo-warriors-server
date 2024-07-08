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

        # Step 1: Submit the code
        conn = http.client.HTTPSConnection(os.environ.get("API_HOST"), context=ssl.create_default_context(cafile=certifi.where()))
        submissions = []

        for testcase in testcases:
            submission = {
                "language_id": programming_language,
                "source_code": code,
                "stdin": testcase["input"],
                "expected_output": testcase["output"]
            }
            submissions.append(submission)

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
            return data

        # Step 2: Get the results of the submission
        tokens = []
        tokens = [val["token"] for val in data]
        tokens_param = "%2C".join(tokens)

        # Polling for the results
        poll_interval = 5  # seconds
        max_attempts = 20

        for attempt in range(max_attempts):
            conn.request("GET", f"/submissions/batch?tokens={tokens_param}&base64_encoded=false&fields=*", headers=headers)
            res = conn.getresponse()
            raw_data = res.read()
            result = json.loads(raw_data)
            if res.status != 200:
                conn.close()
                raise result

            all_done = all(submission["status"]["id"] != 1 for submission in result["submissions"])
            if all_done:
                conn.close()
                return result

            time.sleep(poll_interval)

        conn.close()
        raise TimeoutError("Submission results not ready after polling for a while")
    
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