import unittest
import shutil, os
from pylogger import toolshed as ts


class TestToolShed(unittest.TestCase):
    
    def setUp(self):
        self.warehouse = ts.ToolShed('./tests/test_dir')
        
    def tearDown(self):
        self.warehouse.close_all()
        shutil.rmtree('./tests/test_dir')
        
    def test_new(self):
        log = self.warehouse.new('test_log')
        self.assertIn('test_log', self.warehouse.get_logs())
        self.assertEqual(log, self.warehouse.get_logs()['test_log'])
        
    def test_new_existing_log(self):
        self.warehouse.new('test_log')
        with self.assertRaises(RuntimeError):
            self.warehouse.new('test_log')
            
    def test_get_dir(self):
        self.assertEqual(self.warehouse.get_dir(), './tests/test_dir')
        
    def test_get_logs(self):
        self.warehouse.new('test_log')
        self.assertIn('test_log', self.warehouse.get_logs())
        
    def test_get_log(self):
        self.warehouse.new('test_log')
        self.assertEqual(self.warehouse.get_log('test_log'), self.warehouse.get_logs()['test_log'])
        
    def test_get_log_nonexistent(self):
        with self.assertRaises(KeyError):
            self.warehouse.get_log('nonexistent_log')
            
    def test_log_write(self):
        self.warehouse.new('test_log', module='unittest')
        # self.warehouse.get_log('test_log1').open()
        
        self.warehouse.get_log('test_log').write(True, 'Test message')
        self.warehouse.close('test_log')
        
        with open('./tests/test_dir/test_log.txt') as f:
            log_content = f.read()
            
        self.assertIn('Test message', log_content)
        self.assertIn('unittest', log_content)
            
    def test_log_multiple(self):
        test_log1 = self.warehouse.new("test_log1", module='unittest')
        test_log2 = self.warehouse.new("test_log2", module='unittest')
        
        print(str(test_log1))
        print(str(test_log2))
        
        test_log1.write(True, message="Test Message 1", success_str="TEST")
        # self.warehouse.get_log("test_log1").write(True, message="Test Message 2", success_str="TEST")
        
        test_log2.write(True, message="Test Message 1", success_str="TEST")
        # self.warehouse.get_log("test_log2").write(True, message="Test Message 2", success_str="TEST")
        
        self.warehouse.close("test_log1")
        self.warehouse.close("test_log2")
        
        with open("./tests/test_dir/test_log1.txt", 'r') as f1:
            content1 = f1.read()
        with open("./tests/test_dir/test_log2.txt", 'r') as f2:
            content2 = f2.read()
            
        # print(content1, content2)
        
        self.assertIn("TEST", content1)
        # self.assertIn("TEST", content1)
        
        self.assertIn("TEST", content2)
        # self.assertIn("TEST", content2)
        
            
    def test_close_all(self):
        self.warehouse.new('test_log1')
        self.warehouse.new('test_log2')
        self.warehouse.close_all()
        for log in self.warehouse.get_logs().values():
            self.assertFalse(log.is_open())
            
    def test_close(self):
        self.warehouse.new('test_log')
        self.warehouse.close('test_log')
        self.assertFalse(self.warehouse.get_log('test_log').is_open())
        
    def test_close_nonexistent_log(self):
        with self.assertRaises(KeyError):
            self.warehouse.close('nonexistent_log')
