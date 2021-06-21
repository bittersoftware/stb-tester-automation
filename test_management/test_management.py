import logging

logger = logging.getLogger(__file__)


class GetTestScope:
    """Class that implements test management methods for a client.

    Returns:
        list: list of tests with test_case objects
        Ex:
        test_1 = {"tc_id": "TC-1", "summary": "Test 1 summary"}
        test_2 = {"tc_id": "TC-2", "summary": "Test 2 summary"}

        test_scope = [test_1, test_2]
    """

    @staticmethod
    def get_test_scope(test_request):
        """Method that receives a test request from Unique

        Args:
            test_request (dict): object with test type and text fields from UI
            Ex:
            test_request = {"type": 1, "query": "file.xls"}
            test_request = {"type": 2, "tc_id": "TC-1", "repeat": 2}

        Returns:
            list: list of tests with test_case objects
        """
        if test_request["type"] == 1:
            return GetTestScope.scope(test_request)
        elif test_request["type"] == 2:
            return GetTestScope.loop(test_request)

    @staticmethod
    def scope(test_request):
        """Method with example that access test management tool or file to retreive tests

        Args:
            test_request (dict): object with test type and text fields from UI
            Ex:
            test_request = {"type": 1, "query": "file.xls"}

        Returns:
            list: list of tests with test_case objects
        """
        query = test_request["query"]
        logger.info(f"Test Entry: Query: {query}")  # noqa: E999

        # Mock implementation of a test fetch request
        # Mock reads from local file
        # Implement customer solution with Jira for instance
        import csv
        import os

        path = os.path.dirname(__file__)
        file_name = f"{path}/test_plan_mock.csv"  # noqa: E999

        with open(file_name, "r") as csv_file:
            reader = csv.reader(csv_file)

            test_scope = []
            for line in reader:
                test_object = {}
                test_object["tc_id"] = line[0]
                test_object["summary"] = line[1]
                test_scope.append(test_object)
        # End of mock implementation

        if len(test_scope) == 0:
            logger.error("No tests fetched")
            return None
        else:
            return GetTestScope.validate(test_scope)

    @staticmethod
    def loop(test_request):
        """Method with example that access test management tool or file to retreive tests

        Args:
            test_request (dict): object with test type and text fields from UI
            Ex:
            test_request = {"type": 2, "tc_id": "TC-1", "repeat": 2}

        Returns:
            list: list of tests with test_case objects
        """
        repeat = int(test_request["repeat"])
        test_case_id = test_request["test"]
        logger.info(f"Test Entry: TC: {test_case_id}, Repeat: {repeat}")  # noqa: E999

        # Mock implementation of a test fetch request
        # Mock reads from local file
        # Implement customer solution with Jira for instance
        import csv
        import os

        path = os.path.dirname(__file__)
        file_name = f"{path}/test_plan_mock.csv"  # noqa: E999

        with open(file_name, "r") as csv_file:
            reader = csv.reader(csv_file)

            test_scope = []
            test_object = {}
            for line in reader:
                if line[0] == test_case_id:
                    test_object["tc_id"] = line[0]
                    test_object["summary"] = line[1]
                    break
        # End of mock implementation

        if not test_object:
            logger.error("No tests fetched")
            return None
        else:
            test_scope = [test_object.copy() for _ in range(repeat)]

            return GetTestScope.validate(test_scope)

    @staticmethod
    def validate(test_scope):
        """Validates that mandatory keys are in the objects from test list"""
        keys = ["tc_id", "summary"]
        for test_case in test_scope:
            if not all(key in test_case for key in keys):
                logger.error("Tests feched does not follow the expected")
                logger.error("Expected list of test case objects:")
                logger.error("{{'id': 'TC-2', 'summary': 'Test 2 summary'}}")
                logger.error(f"Got: {test_scope}")  # noqa: E999
                return None

        return test_scope
