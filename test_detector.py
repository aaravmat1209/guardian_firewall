#!/usr/bin/env python3
"""
Quick test script to verify the Guardian detector is working
"""

import sys
import os
sys.path.append('backend')

from backend.risk.whole_detector import get_detector

def test_detector():
    print("🛡️ Testing Guardian Detector...")

    # Get detector instance
    try:
        detector = get_detector()
        print("✅ Detector loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load detector: {e}")
        return

    # Test messages
    test_cases = [
        {
            "message": "Hey, want to join my team?",
            "expected": "LOW"
        },
        {
            "message": "You are so mature for your age",
            "expected": "MEDIUM"
        },
        {
            "message": "Can you send me a photo?",
            "expected": "HIGH"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{test['message']}'")

        try:
            result = detector.analyze_message(test["message"])

            print(f"   Risk Level: {result.final_level}")
            print(f"   Score: {result.final_score:.3f}")
            print(f"   LLM Risk: {result.llm_risk} (confidence: {result.llm_confidence:.3f})")
            print(f"   HF Score: {result.hf_score:.3f}")
            print(f"   Action: {result.action}")
            print(f"   Explanations: {result.explanations}")

            if result.final_level == test["expected"]:
                print("   ✅ PASSED")
            else:
                print(f"   ⚠️ Expected {test['expected']}, got {result.final_level}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_detector()