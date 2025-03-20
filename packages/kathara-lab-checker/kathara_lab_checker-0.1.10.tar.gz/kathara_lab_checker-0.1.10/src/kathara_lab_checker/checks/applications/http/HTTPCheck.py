import re
from Kathara.exceptions import MachineNotRunningError
from ...AbstractCheck import AbstractCheck
from ....model.CheckResult import CheckResult
from ....utils import get_output

class HTTPCheck(AbstractCheck):
    """
    Execute HTTP checks using curl on the remote device.
    """

    def check(self, device_name: str, test_params: dict) -> list[CheckResult]:
        """
        Runs curl on the device with the given parameters:
          {
            "url": "<required>",
            "method": "<optional, default=GET>",
            "status_code": 200,
            "regex_body": "<regex to match>",
            "body_contains": "<literal substring>"
          }
        Returns one or more CheckResult objects.
        """
        results = []
        url = test_params.get("url")
        if not url:
            desc = f"HTTP Check on {device_name} missing 'url'"
            return [CheckResult(desc, False, "No 'url' provided")]

        desc = f"HTTP check '{url}' on {device_name}"

        method = test_params.get("method", "GET").upper()

        # Use curl to output both body and HTTP code separated by a unique delimiter.
        delimiter = "===CURL_STATUS==="
        curl_cmd = f"curl -s -X {method} -w '{delimiter}%{{http_code}}' '{url}'"

        try:
            exec_output = self.kathara_manager.exec(
                machine_name=device_name,
                command=curl_cmd,
                lab_hash=self.lab.hash
            )
        except MachineNotRunningError as e:
            return [CheckResult(desc, False, str(e))]

        combined_output = get_output(exec_output).strip()
        if delimiter in combined_output:
            body, code_str = combined_output.rsplit(delimiter, 1)
        else:
            body = combined_output
            code_str = ""

        expected_code = test_params.get("status_code", 200)
        if not code_str.isdigit():
            results.append(CheckResult(desc, False, f"curl output did not contain a valid status code: '{code_str}'"))
        else:
            actual_code = int(code_str)
            if actual_code == expected_code:
                results.append(CheckResult(f"{desc} status", True, f"HTTP {actual_code} == {expected_code}"))
            else:
                results.append(CheckResult(f"{desc} status", False,
                    f"Expected HTTP {expected_code}, got {actual_code}"))

        if "regex_body" in test_params or "body_contains" in test_params:
            if "regex_body" in test_params:
                regex = test_params["regex_body"]
                regex_desc = f"{desc} body regex /{regex}/"
                if re.search(regex, body):
                    results.append(CheckResult(regex_desc, True, "OK"))
                else:
                    results.append(CheckResult(regex_desc, False, "Body does not match regex"))
            
            if "body_contains" in test_params:
                substr = test_params["body_contains"]
                substr_desc = f"{desc} body substring '{substr}'"
                if substr in body:
                    results.append(CheckResult(substr_desc, True, "OK"))
                else:
                    results.append(CheckResult(substr_desc, False, "Substring not found in body"))
        
        return results

    def run(self, device_http_tests: dict[str, list[dict]]) -> list[CheckResult]:
        """
        device_http_tests = {
          "device_name": [
            { "url": "<required>", "method": "GET", "status_code": 200, "regex_body": "foo|bar" },
            { "url": "<another_url>", "body_contains": "hello world" }
          ],
          ...
        }
        """
        all_results = []
        for device_name, checks in device_http_tests.items():
            self.logger.info(f"Performing HTTP checks on {device_name}...")
            for check_params in checks:
                results = self.check(device_name, check_params)
                all_results.extend(results)
        return all_results
