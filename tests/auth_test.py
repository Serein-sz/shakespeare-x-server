import unittest
from src.entity.user import hash_password, verify_password

class TestPasswordHashing(unittest.TestCase):

    def setUp(self):
        """测试前置设置"""
        self.password = "SecureP@ssw0rd123!"
        self.wrong_password = "WrongP@ssw0rd!"
        self.hashed_password = hash_password(self.password)
    
    def test_verify_correct_password(self):
        """测试正确密码验证通过"""
        result = verify_password(self.password, self.hashed_password)
        self.assertTrue(result)
