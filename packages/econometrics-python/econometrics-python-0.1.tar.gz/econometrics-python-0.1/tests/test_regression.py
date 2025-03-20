# File: test_regression.py
import unittest
from LinearRegression.regression import LinearRegression

class TestLinearRegression(unittest.TestCase):

    def setUp(self):
        # Chỉ cần truyền vào file dữ liệu, các cột sẽ tự động xác định
        self.model = LinearRegression(data_file='./linear_regression.csv')

    def test_fit(self):
        self.model.fit()  # Kiểm tra fit của mô hình
        self.assertIsNotNone(self.model.results)  # Đảm bảo mô hình đã có kết quả

    def test_load_data(self):
        data = self.model.load_data()
        print(f"Size of data: {data.shape[0]}")  # In ra số dòng của dữ liệu
        self.assertEqual(data.shape[0], 10)  # Kiểm tra số dòng dữ liệu

    def test_summary(self):
        self.model.summary()  # Kiểm tra summary của mô hình

if __name__ == '__main__':
    unittest.main()
