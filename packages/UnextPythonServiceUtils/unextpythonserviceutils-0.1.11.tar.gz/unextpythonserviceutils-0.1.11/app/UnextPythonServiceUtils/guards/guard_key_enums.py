from enum import StrEnum


class RateLimiterGuardKeys(StrEnum):
    AGENT_LLM_CALL_GUARD = "AGENT_LLM_CALL_GUARD"
    TEST_KEY = "TEST_KEY"
