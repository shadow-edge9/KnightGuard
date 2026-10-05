from safety import check_safety, redact_sensitive_data
from test_cases import TEST_CASES


def run_tests():

    passed = 0

    print("\n=== SAFETY TESTS ===\n")

    for test in TEST_CASES:

        result = check_safety(test["message"])

        category_ok = (
            result["category"]
            == test["expected_category"]
        )

        decision_ok = (
            result["decision"]
            == test["expected_decision"]
        )

        if category_ok and decision_ok:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"

        print(f"Test: {test['name']}")
        print(f"Category: {result['category']}")
        print(f"Decision: {result['decision']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Result: {status}")
        print("-" * 40)

    print(
        f"\nPassed: {passed}/{len(TEST_CASES)}"
    )


    print("\n=== PRIVACY TEST ===\n")

    message = (
        "My email is test@example.com, "
        "phone is 9876543210 and website is "
        "https://example.com"
    )

    redacted, types = redact_sensitive_data(message)

    print("Original:")
    print(message)

    print("\nSent to external AI:")
    print(redacted)

    print("\nRedacted:")
    print(types)


if __name__ == "__main__":
    run_tests()
