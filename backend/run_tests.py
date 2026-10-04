from safety import check_safety
from test_cases import TEST_CASES


def run_tests():
    passed = 0

    print("\n=== AI SAFETY TEST RESULTS ===\n")

    for test in TEST_CASES:
        result = check_safety(test["message"])

        expected = test["expected_category"]
        detected = result["category"]

        if expected == detected:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"

        print(f"Test: {test['name']}")
        print(f"Expected: {expected}")
        print(f"Detected: {detected}")
        print(f"Result: {status}")
        print("-" * 40)

    print(f"\nPassed: {passed}/{len(TEST_CASES)}")


if __name__ == "__main__":
    run_tests()