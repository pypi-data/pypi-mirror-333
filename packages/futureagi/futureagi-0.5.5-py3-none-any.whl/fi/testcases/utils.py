from typing import List, Union

from fi.testcases.conversational_test_case import ConversationalTestCase
from fi.testcases.llm_test_case import LLMTestCase
from fi.testcases.mllm_test_case import MLLMTestCase


def check_valid_test_cases_type(
    test_cases: Union[
        List[Union[LLMTestCase, MLLMTestCase]], List[ConversationalTestCase]
    ]
):
    llm_test_case_count = 0
    conversational_test_case_count = 0
    for test_case in test_cases:
        if isinstance(test_case, LLMTestCase) or isinstance(test_case, MLLMTestCase):
            llm_test_case_count += 1
        else:
            conversational_test_case_count += 1

    if llm_test_case_count > 0 and conversational_test_case_count > 0:
        raise ValueError(
            "You cannot supply a mixture of `LLMTestCase`/`MLLMTestCase`(s) and `ConversationalTestCase`(s) as the list of test cases."
        )
