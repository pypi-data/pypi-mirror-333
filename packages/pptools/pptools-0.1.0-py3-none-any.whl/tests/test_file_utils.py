import os
import json
import unittest
from unittest.mock import patch, mock_open, MagicMock
from file.file_utils import FileUtils


class TestFileUtils(unittest.TestCase):
    """测试FileUtils类的功能"""

    def setUp(self):
        """测试前的准备工作"""
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """测试后的清理工作"""
        # 如果测试目录存在，则删除
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    @patch('builtins.open', new_callable=mock_open, read_data='test content')
    def test_read_text(self, mock_file):
        """测试read_text方法"""
        content = FileUtils.read_text('test.txt')
        mock_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')
        self.assertEqual(content, 'test content')

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_text_success(self, mock_file, mock_makedirs):
        """测试write_text方法成功的情况"""
        result = FileUtils.write_text('test.txt', 'test content')
        mock_makedirs.assert_called_once()
        mock_file.assert_called_once_with('test.txt', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with('test content')
        self.assertTrue(result)

    @patch('os.makedirs')
    @patch('builtins.open')
    def test_write_text_failure(self, mock_file, mock_makedirs):
        """测试write_text方法失败的情况"""
        mock_file.side_effect = IOError()
        result = FileUtils.write_text('test.txt', 'test content')
        mock_makedirs.assert_called_once()
        self.assertFalse(result)

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_json(self, mock_file):
        """测试read_json方法"""
        with patch('json.load', return_value={'key': 'value'}):
            data = FileUtils.read_json('test.json')
            mock_file.assert_called_once_with('test.json', 'r', encoding='utf-8')
            self.assertEqual(data, {'key': 'value'})

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_json_success(self, mock_file, mock_makedirs):
        """测试write_json方法成功的情况"""
        with patch('json.dump') as mock_json_dump:
            result = FileUtils.write_json('test.json', {'key': 'value'})
            mock_makedirs.assert_called_once()
            mock_file.assert_called_once_with('test.json', 'w', encoding='utf-8')
            mock_json_dump.assert_called_once()
            self.assertTrue(result)

    @patch('os.makedirs')
    @patch('builtins.open')
    def test_write_json_failure(self, mock_file, mock_makedirs):
        """测试write_json方法失败的情况"""
        mock_file.side_effect = IOError()
        result = FileUtils.write_json('test.json', {'key': 'value'})
        mock_makedirs.assert_called_once()
        self.assertFalse(result)

    def test_real_file_operations(self):
        """测试实际的文件操作"""
        test_file = os.path.join(self.test_dir, 'test.txt')
        test_content = 'This is a test content.'
        
        # 测试写入文本文件
        self.assertTrue(FileUtils.write_text(test_file, test_content))
        
        # 测试读取文本文件
        self.assertEqual(FileUtils.read_text(test_file), test_content)
        
        # 测试写入JSON文件
        test_json_file = os.path.join(self.test_dir, 'test.json')
        test_json_data = {'name': 'test', 'value': 123}
        self.assertTrue(FileUtils.write_json(test_json_file, test_json_data))
        
        # 测试读取JSON文件
        read_json_data = FileUtils.read_json(test_json_file)
        self.assertEqual(read_json_data, test_json_data)


if __name__ == '__main__':
    unittest.main()