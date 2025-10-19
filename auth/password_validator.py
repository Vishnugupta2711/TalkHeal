"""
Password Strength Validator Module
Implements NIST SP 800-63B password guidelines and strength calculation
"""

import re
from typing import Tuple, Dict, List
import os

class PasswordValidator:
    """
    Password strength validator following NIST guidelines
    """

    # NIST recommended minimum and maximum lengths
    MIN_LENGTH = 8
    MAX_LENGTH = 64

    # Common weak passwords (top 100 most common)
    COMMON_PASSWORDS = {
        'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', '1234567',
        'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou', 'master', 'sunshine',
        'ashley', 'bailey', 'passw0rd', 'shadow', '123123', '654321', 'superman',
        'qazwsx', 'michael', 'football', 'password1', 'welcome', 'jesus', 'ninja',
        'mustang', 'password123', 'admin', 'hello', 'starwars', 'whatever', 'donald',
        'batman', 'zaq1zaq1', 'solo', 'jennifer', 'jordan', 'hunter', 'flower',
        'hottie', 'loveme', 'ranger', 'charlie', 'robert', 'freedom', 'madison',
        'andrew', 'golfer', 'cookie', 'matthew', 'cheese', 'princess', 'jessica',
        'summer', 'taylor', 'thomas', 'hannah', 'michelle', 'daniel', 'lauren',
        'bailey', 'harley', 'michelle', 'soccer', 'natasha', 'chicken', 'winter',
        'purple', 'internet', 'service', 'canada', 'hello', 'ranger', 'shadow',
        'american', 'rainbow', 'john', 'pepper', 'qwerty123', 'superman', 'pass',
        'google', 'freedom', 'whatever', 'iceman', 'blahblah', 'diamond', 'killer',
        'pussy', 'computer', 'hannah', 'nicole', 'fuckyou', 'thomas', 'victoria'
    }

    # Keyboard patterns
    KEYBOARD_PATTERNS = [
        'qwerty', 'asdfgh', 'zxcvbn', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
        '1234567890', 'abcdefgh', '12345', 'qwert', 'yuiop'
    ]

    @staticmethod
    def calculate_strength(password: str) -> Dict[str, any]:
        """
        Calculate password strength and return detailed metrics

        Args:
            password: Password string to validate

        Returns:
            Dictionary containing:
                - score: int (0-100)
                - strength: str (Weak, Fair, Good, Strong, Very Strong)
                - feedback: List[str] - suggestions for improvement
                - checks: Dict - individual requirement checks
        """
        checks = {
            'length': len(password) >= PasswordValidator.MIN_LENGTH,
            'max_length': len(password) <= PasswordValidator.MAX_LENGTH,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digit': bool(re.search(r'[0-9]', password)),
            'special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password)),
            'not_common': password.lower() not in PasswordValidator.COMMON_PASSWORDS,
            'no_sequential': not PasswordValidator._has_sequential_chars(password),
            'no_repeated': not PasswordValidator._has_repeated_chars(password),
            'no_keyboard_pattern': not PasswordValidator._has_keyboard_pattern(password)
        }

        # Calculate score (0-100)
        score = 0

        # Length score (0-30 points)
        if len(password) >= 8:
            score += 15
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 5

        # Character variety (0-40 points)
        if checks['uppercase']:
            score += 10
        if checks['lowercase']:
            score += 10
        if checks['digit']:
            score += 10
        if checks['special']:
            score += 10

        # Pattern checks (0-30 points)
        if checks['not_common']:
            score += 10
        if checks['no_sequential']:
            score += 10
        if checks['no_repeated']:
            score += 5
        if checks['no_keyboard_pattern']:
            score += 5

        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
            color = "#6BCF7F"
        elif score >= 60:
            strength = "Strong"
            color = "#A8E6CF"
        elif score >= 40:
            strength = "Good"
            color = "#FFD93D"
        elif score >= 20:
            strength = "Fair"
            color = "#FFA500"
        else:
            strength = "Weak"
            color = "#FF6B6B"

        # Generate feedback
        feedback = PasswordValidator._generate_feedback(checks, len(password))

        return {
            'score': score,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'checks': checks
        }

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password against NIST guidelines

        Args:
            password: Password string to validate

        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if len(password) < PasswordValidator.MIN_LENGTH:
            return False, f"Password must be at least {PasswordValidator.MIN_LENGTH} characters long"

        if len(password) > PasswordValidator.MAX_LENGTH:
            return False, f"Password must not exceed {PasswordValidator.MAX_LENGTH} characters"

        # Check for at least one letter
        if not re.search(r'[A-Za-z]', password):
            return False, "Password must contain at least one letter"

        # Check against common passwords
        if password.lower() in PasswordValidator.COMMON_PASSWORDS:
            return False, "This password is too common. Please choose a stronger password"

        # Check for sequential characters
        if PasswordValidator._has_sequential_chars(password):
            return False, "Password contains sequential characters (e.g., 12345, abcde). Please choose a stronger password"

        # Check for repeated characters
        if PasswordValidator._has_repeated_chars(password):
            return False, "Password contains too many repeated characters. Please choose a stronger password"

        # Check for keyboard patterns
        if PasswordValidator._has_keyboard_pattern(password):
            return False, "Password contains keyboard patterns (e.g., qwerty). Please choose a stronger password"

        return True, "Valid password"

    @staticmethod
    def _has_sequential_chars(password: str, min_length: int = 4) -> bool:
        """Check for sequential characters (numbers or letters)"""
        password_lower = password.lower()

        # Check for sequential numbers
        for i in range(len(password) - min_length + 1):
            substr = password[i:i + min_length]
            if substr.isdigit():
                nums = [int(c) for c in substr]
                if all(nums[j] + 1 == nums[j + 1] for j in range(len(nums) - 1)):
                    return True
                if all(nums[j] - 1 == nums[j + 1] for j in range(len(nums) - 1)):
                    return True

        # Check for sequential letters
        for i in range(len(password_lower) - min_length + 1):
            substr = password_lower[i:i + min_length]
            if substr.isalpha():
                chars = [ord(c) for c in substr]
                if all(chars[j] + 1 == chars[j + 1] for j in range(len(chars) - 1)):
                    return True
                if all(chars[j] - 1 == chars[j + 1] for j in range(len(chars) - 1)):
                    return True

        return False

    @staticmethod
    def _has_repeated_chars(password: str, max_repeat: int = 3) -> bool:
        """Check for repeated characters (e.g., aaaa, 1111)"""
        for i in range(len(password) - max_repeat + 1):
            if len(set(password[i:i + max_repeat])) == 1:
                return True
        return False

    @staticmethod
    def _has_keyboard_pattern(password: str) -> bool:
        """Check for common keyboard patterns"""
        password_lower = password.lower()
        for pattern in PasswordValidator.KEYBOARD_PATTERNS:
            if pattern in password_lower or pattern[::-1] in password_lower:
                return True
        return False

    @staticmethod
    def _generate_feedback(checks: Dict[str, bool], length: int) -> List[str]:
        """Generate helpful feedback for password improvement"""
        feedback = []

        if not checks['length']:
            feedback.append(f"Add {PasswordValidator.MIN_LENGTH - length} more characters")

        if not checks['uppercase']:
            feedback.append("Add uppercase letters (A-Z)")

        if not checks['lowercase']:
            feedback.append("Add lowercase letters (a-z)")

        if not checks['digit']:
            feedback.append("Add numbers (0-9)")

        if not checks['special']:
            feedback.append("Add special characters (!@#$%^&*)")

        if not checks['not_common']:
            feedback.append("This is a common password - choose something unique")

        if not checks['no_sequential']:
            feedback.append("Avoid sequential characters (123, abc)")

        if not checks['no_repeated']:
            feedback.append("Avoid repeated characters (aaa, 111)")

        if not checks['no_keyboard_pattern']:
            feedback.append("Avoid keyboard patterns (qwerty)")

        if not feedback:
            feedback.append("Great! Your password is strong and secure")

        return feedback


def get_password_strength(password: str) -> Dict[str, any]:
    """
    Convenience function to get password strength

    Args:
        password: Password string to analyze

    Returns:
        Dictionary with strength metrics
    """
    return PasswordValidator.calculate_strength(password)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Convenience function to validate password

    Args:
        password: Password string to validate

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    return PasswordValidator.validate_password(password)
