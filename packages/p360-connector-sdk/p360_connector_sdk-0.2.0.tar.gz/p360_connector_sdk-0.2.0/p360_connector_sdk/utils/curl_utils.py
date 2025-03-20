import shlex
import json
import re
import requests


class CurlUtils:
    """
    Utility class for handling cURL commands:
    - Validates if a string is a cURL command.
    - Parses a cURL command into a Python requests call.
    """

    @staticmethod
    def is_valid_curl_command(curl_string):
        """
        Checks if a given string contains a valid cURL command.

        :param curl_string: str - The input string to validate.
        :return: bool - True if it's a valid cURL command, otherwise False.
        """
        # Ensure the string starts with 'curl'
        if not curl_string.strip().startswith("curl"):
            return False

        # Regex to detect a valid URL (http or https)
        url_pattern = r"https?://[^\s]+"  # Matches URLs like http://example.com
        has_url = re.search(url_pattern, curl_string) is not None

        # Check for common cURL flags that indicate a request
        has_method = "-X" in curl_string  # Custom HTTP method
        has_header = "-H" in curl_string  # Headers
        has_data = "-d" in curl_string or "--data" in curl_string  # Data payload

        # A valid cURL should at least have a URL and one of the main flags
        return has_url and (has_method or has_header or has_data)

    @staticmethod
    def parse_curl(curl_command):
        """
        Parses a cURL command string and converts it into a Python requests object.

        :param curl_command: str - cURL command as a string
        :return: dict - Parsed components for a Python requests call
        """
        tokens = shlex.split(curl_command)  # Safely split cURL command
        method = "GET"  # Default method
        url = None
        headers = {}
        data = None
        json_data = None

        i = 0
        while i < len(tokens):
            if tokens[i] == "-X":  # HTTP method
                method = tokens[i + 1]
                i += 2
            elif tokens[i] == "-H":  # Headers
                key, value = tokens[i + 1].split(":", 1)
                headers[key.strip()] = value.strip()
                i += 2
            elif tokens[i] in ("-d", "--data"):  # Data payload
                try:
                    data = json.loads(tokens[i + 1])  # Try parsing as JSON
                    json_data = data  # Store separately for json param
                except json.JSONDecodeError:
                    data = tokens[i + 1]  # Keep as raw string
                i += 2
            elif tokens[i].startswith("http"):  # URL detection
                url = tokens[i]
                i += 1
            else:
                i += 1

        return {
            "method": method,
            "url": url,
            "headers": headers,
            "data": None if json_data else data,  # Use json_data if available
            "json": json_data
        }

    @staticmethod
    def execute_curl_as_request(curl_command):
        """
        Converts a cURL command string to a requests call and executes it.

        :param curl_command: str - The cURL command
        :return: requests.Response - The response from the executed request
        """
        if not CurlUtils.is_valid_curl_command(curl_command):
            raise ValueError("Invalid cURL command")

        parsed_request = CurlUtils.parse_curl(curl_command)

        response = requests.request(
            method=parsed_request["method"],
            url=parsed_request["url"],
            headers=parsed_request["headers"],
            data=parsed_request["data"],
            json=parsed_request["json"]
        )

        return response
