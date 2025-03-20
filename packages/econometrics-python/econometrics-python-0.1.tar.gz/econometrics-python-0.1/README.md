# Econometrics 

## Linear Regression

A simple econometrics package for linear regression and plotting.

### Installation

You can install the package via pip: pip install econometrics

### Run with the package
```python

from LinearRegression.regression import LinearRegression

# Không cần truyền 'x_column' và 'y_column' vào nữa
model = LinearRegression(data_file='./data_file.csv')

# Huấn luyện mô hình
model.fit()

# In ra kết quả summary
model.summary()

# Vẽ đồ thị
model.plot()

