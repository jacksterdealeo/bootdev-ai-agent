import unittest
from functions.get_files_info import get_files_info


class SimpleTest(unittest.TestCase):
    def test_get_calc_dir(self):
        test_string = """Result for current directory:
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=44 bytes, is_dir=True
 - main.py: file_size=576 bytes, is_dir=False"""
        self.assertEqual(get_files_info("calculator", "."), test_string)

    def test_get_calc_pkg_dir(self):
        test_string = """Result for 'pkg' directory:
 - calculator.py: file_size=1738 bytes, is_dir=False
 - render.py: file_size=767 bytes, is_dir=False"""
        self.assertEqual(get_files_info("calculator", "pkg"), test_string)

    def test_outside_working_dir_err(self):
        test_string = """Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory"""
        self.assertEqual(get_files_info("calculator", "/bin"), test_string)

    def test_up_from_working_directory(self):
        test_string = """Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory"""
        self.assertEqual(get_files_info("calculator", "../"), test_string)


if __name__ == "__main__":
    unittest.main()
