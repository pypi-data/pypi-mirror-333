import json
import os
import re
from typing import Any, Callable
from .data import JsonPathExpression, SnippetData
from .result import AssertionResult, Op


class Check:
    def __init__(
        self,
        name: str,
        description: str | None = None,
        data: SnippetData | None = None
    ):
        self.name = name
        self.description = description

        if data is None:
            try:
                path = os.environ["LUNAR_BUNDLE_PATH"]
                data = SnippetData(path)
            except KeyError:
                raise ValueError(
                    "LUNAR_BUNDLE_PATH is not set"
                )
            except ValueError as e:
                raise ValueError(
                    "invalid LUNAR_BUNDLE_PATH"
                ) from e
            except FileNotFoundError:
                raise ValueError(
                    f"LUNAR_BUNDLE_PATH does not exist: {path}"
                )

        if not isinstance(data, SnippetData):
            raise ValueError(
                f"Data must be a SnippetData instance, got {data}"
            )
        self.data = data

        self._accessed_paths = []
        self._used_vars = []
        self._results = []
        self._submitted = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.submit()

    def submit(self):
        if not self._submitted:
            output = {
                "name": self.name,
                "assertions": [
                    result.toJson()
                    for result in self._results
                ]
            }

            if len(self._accessed_paths) > 0:
                output["paths"] = self._accessed_paths

            if self.description is not None:
                output["description"] = self.description

            print(json.dumps(output), end="")

            self._submitted = True

    def _make_assertion(
        self,
        op: Op,
        check_fn: Callable[[Any], bool],
        value: Any,
        failure_message: str
    ) -> AssertionResult:
        actual_value = value

        if isinstance(value, str) and value.startswith("."):
            try:
                jsonPath = JsonPathExpression(value)
            except ValueError:
                actual_value = value
            else:
                self._accessed_paths.append(value)
                actual_value = self.data.get(jsonPath)

        ok = check_fn(actual_value)
        self._results.append(
            AssertionResult(
                op=op,
                args=[actual_value],
                ok=ok,
                failure_message=failure_message if not ok else None,
            )
        )

    def get(self, path: str) -> Any | None:
        try:
            jsonPath = JsonPathExpression(path)
        except ValueError as e:
            raise ValueError(f"Invalid JSON path: {path}") from e

        self._accessed_paths.append(path)
        return self.data.get(jsonPath)

    def assert_true(
        self,
        value: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.TRUE,
            lambda v: v is True,
            value,
            failure_message or f"{value} is not true"
        )

    def assert_false(
        self,
        value: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.FALSE,
            lambda v: v is False,
            value,
            failure_message or f"{value} is not false"
        )

    def assert_equals(
        self,
        value: Any,
        expected: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.EQUALS,
            lambda v: v == expected,
            value,
            failure_message or f"{value} is not equal to {expected}"
        )

    def assert_contains(
        self,
        value: Any,
        expected: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.CONTAINS,
            lambda v: expected in v,
            value,
            failure_message or f"{value} does not contain {expected}"
        )

    def assert_greater(
        self,
        value: Any,
        expected: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.GREATER,
            lambda v: v > expected,
            value,
            failure_message or f"{value} is not greater than {expected}"
        )

    def assert_greater_or_equal(
        self,
        value: Any,
        expected: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.GREATER_OR_EQUAL,
            lambda v: v >= expected,
            value,
            failure_message or
            f"{value} is not greater than or equal to {expected}"
        )

    def assert_less(
        self,
        value: Any,
        expected: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.LESS,
            lambda v: v < expected,
            value,
            failure_message or f"{value} is not less than {expected}"
        )

    def assert_less_or_equal(
        self,
        value: Any,
        expected: Any,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.LESS_OR_EQUAL,
            lambda v: v <= expected,
            value,
            failure_message or
            f"{value} is not less than or equal to {expected}"
        )

    def assert_match(
        self,
        value: Any,
        pattern: str,
        failure_message: str | None = None
    ):
        self._make_assertion(
            Op.MATCH,
            lambda v: re.match(pattern, v) is not None,
            value,
            failure_message or f"{value} does not match {pattern}"
        )
