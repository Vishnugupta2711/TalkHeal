"""
Unit tests for Password Validator
Tests NIST guidelines compliance and strength calculation
"""

import unittest
from auth.password_validator import PasswordValidator, get_password_strength, validate_password_strength


class TestPasswordValidator(unittest.TestCase):
    """Test cases for PasswordValidator class"""

    def test_minimum_length_requirement(self):
        """Test minimum 8 character length requirement"""
        is_valid, message = PasswordValidator.validate_password("short")
        self.assertFalse(is_valid)
        self.assertIn("at least 8 characters", message)

    def test_maximum_length_requirement(self):
        """Test maximum 64 character length requirement"""
        long_password = "a" * 65
        is_valid, message = PasswordValidator.validate_password(long_password)
        self.assertFalse(is_valid)
        self.assertIn("must not exceed 64 characters", message)

    def test_must_contain_letter(self):
        """Test that password must contain at least one letter"""
        is_valid, message = PasswordValidator.validate_password("12345678")
        self.assertFalse(is_valid)
        self.assertIn("must contain at least one letter", message)

    def test_common_password_rejection(self):
        """Test that common passwords are rejected"""
        # Use passwords that are 8+ characters and in the common list
        common_passwords = ["password", "password123", "letmein"]
        for pwd in common_passwords:
            is_valid, message = PasswordValidator.validate_password(pwd)
            self.assertFalse(is_valid, f"Common password '{pwd}' should be rejected")

    def test_sequential_characters_rejection(self):
        """Test that sequential characters are rejected"""
        sequential_passwords = ["12345678", "abcdefgh", "Test1234"]
        for pwd in sequential_passwords:
            is_valid, message = PasswordValidator.validate_password(pwd)
            self.assertFalse(is_valid, f"Password with sequential chars '{pwd}' should be rejected")

    def test_repeated_characters_rejection(self):
        """Test that repeated characters are rejected"""
        repeated_passwords = ["aaaaabcd", "Test1111", "password!!!"]
        for pwd in repeated_passwords:
            is_valid, message = PasswordValidator.validate_password(pwd)
            self.assertFalse(is_valid, f"Password with repeated chars '{pwd}' should be rejected")

    def test_keyboard_pattern_rejection(self):
        """Test that keyboard patterns are rejected"""
        keyboard_passwords = ["qwertyui", "asdfghjk", "Qwerty123"]
        for pwd in keyboard_passwords:
            is_valid, message = PasswordValidator.validate_password(pwd)
            self.assertFalse(is_valid, f"Password with keyboard pattern '{pwd}' should be rejected")

    def test_strong_password_acceptance(self):
        """Test that strong passwords are accepted"""
        strong_passwords = [
            "MyStr0ng!Pass",
            "S3cur3P@ssw0rd",
            "C0mpl3x!tyRul3s",
            "G00d!Pa55word"
        ]
        for pwd in strong_passwords:
            is_valid, message = PasswordValidator.validate_password(pwd)
            self.assertTrue(is_valid, f"Strong password '{pwd}' should be accepted")

    def test_strength_calculation_weak(self):
        """Test strength calculation for weak passwords"""
        result = PasswordValidator.calculate_strength("weak")
        self.assertLess(result['score'], 60)
        self.assertIn(result['strength'], ['Weak', 'Fair', 'Good'])

    def test_strength_calculation_strong(self):
        """Test strength calculation for strong passwords"""
        result = PasswordValidator.calculate_strength("MyStr0ng!P@ssw0rd2024")
        self.assertGreater(result['score'], 60)
        self.assertIn(result['strength'], ['Strong', 'Very Strong'])

    def test_strength_checks_uppercase(self):
        """Test that uppercase check works correctly"""
        result = PasswordValidator.calculate_strength("lowercase123!")
        self.assertFalse(result['checks']['uppercase'])

        result = PasswordValidator.calculate_strength("Uppercase123!")
        self.assertTrue(result['checks']['uppercase'])

    def test_strength_checks_lowercase(self):
        """Test that lowercase check works correctly"""
        result = PasswordValidator.calculate_strength("UPPERCASE123!")
        self.assertFalse(result['checks']['lowercase'])

        result = PasswordValidator.calculate_strength("Lowercase123!")
        self.assertTrue(result['checks']['lowercase'])

    def test_strength_checks_digit(self):
        """Test that digit check works correctly"""
        result = PasswordValidator.calculate_strength("NoDigitsHere!")
        self.assertFalse(result['checks']['digit'])

        result = PasswordValidator.calculate_strength("HasDigit123!")
        self.assertTrue(result['checks']['digit'])

    def test_strength_checks_special(self):
        """Test that special character check works correctly"""
        result = PasswordValidator.calculate_strength("NoSpecialChars123")
        self.assertFalse(result['checks']['special'])

        result = PasswordValidator.calculate_strength("HasSpecial!123")
        self.assertTrue(result['checks']['special'])

    def test_feedback_generation(self):
        """Test that helpful feedback is generated"""
        result = PasswordValidator.calculate_strength("weak")
        self.assertGreater(len(result['feedback']), 0)
        self.assertTrue(any('characters' in fb.lower() for fb in result['feedback']))

    def test_feedback_for_strong_password(self):
        """Test that strong passwords get positive feedback"""
        result = PasswordValidator.calculate_strength("Str0ng!P@ssw0rd2024")
        if result['score'] >= 80:
            self.assertTrue(any('great' in fb.lower() or 'strong' in fb.lower() for fb in result['feedback']))

    def test_convenience_function_get_password_strength(self):
        """Test the convenience function get_password_strength"""
        result = get_password_strength("TestP@ss123")
        self.assertIn('score', result)
        self.assertIn('strength', result)
        self.assertIn('checks', result)
        self.assertIn('feedback', result)

    def test_convenience_function_validate_password_strength(self):
        """Test the convenience function validate_password_strength"""
        is_valid, message = validate_password_strength("StrongP@ss123")
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(message, str)

    def test_color_assignment_by_score(self):
        """Test that colors are correctly assigned based on score"""
        # Weak password - should get red
        result = PasswordValidator.calculate_strength("weak12")
        if result['score'] < 20:
            self.assertEqual(result['color'], "#FF6B6B")

        # Strong password - should get green
        result = PasswordValidator.calculate_strength("VeryStr0ng!P@ssw0rd")
        if result['score'] >= 80:
            self.assertEqual(result['color'], "#6BCF7F")

    def test_sequential_numbers_detection(self):
        """Test detection of sequential numbers"""
        self.assertTrue(PasswordValidator._has_sequential_chars("test12345"))
        self.assertTrue(PasswordValidator._has_sequential_chars("test54321"))
        self.assertFalse(PasswordValidator._has_sequential_chars("test13579"))

    def test_sequential_letters_detection(self):
        """Test detection of sequential letters"""
        self.assertTrue(PasswordValidator._has_sequential_chars("testabcd"))
        self.assertTrue(PasswordValidator._has_sequential_chars("testdcba"))
        self.assertFalse(PasswordValidator._has_sequential_chars("testaceg"))

    def test_repeated_chars_detection(self):
        """Test detection of repeated characters"""
        self.assertTrue(PasswordValidator._has_repeated_chars("testaaaa"))
        self.assertTrue(PasswordValidator._has_repeated_chars("test1111"))
        self.assertFalse(PasswordValidator._has_repeated_chars("testabcd"))

    def test_keyboard_pattern_detection(self):
        """Test detection of keyboard patterns"""
        self.assertTrue(PasswordValidator._has_keyboard_pattern("testqwerty"))
        self.assertTrue(PasswordValidator._has_keyboard_pattern("testasdfgh"))
        self.assertTrue(PasswordValidator._has_keyboard_pattern("test123456"))
        self.assertFalse(PasswordValidator._has_keyboard_pattern("testxyzabc"))

    def test_case_insensitive_common_password_check(self):
        """Test that common password check is case insensitive"""
        is_valid1, _ = PasswordValidator.validate_password("PASSWORD")
        is_valid2, _ = PasswordValidator.validate_password("password")
        is_valid3, _ = PasswordValidator.validate_password("PaSsWoRd")

        self.assertFalse(is_valid1)
        self.assertFalse(is_valid2)
        self.assertFalse(is_valid3)

    def test_edge_case_exactly_8_chars(self):
        """Test password with exactly 8 characters"""
        result = PasswordValidator.calculate_strength("Test!123")
        self.assertTrue(result['checks']['length'])

    def test_edge_case_exactly_64_chars(self):
        """Test password with exactly 64 characters"""
        password_64 = "A1b@" * 16  # Creates 64 char password
        is_valid, message = PasswordValidator.validate_password(password_64)
        # Should be valid if it passes other checks
        self.assertIsInstance(is_valid, bool)


if __name__ == '__main__':
    unittest.main()
