import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def generate_cstr_data(num_samples=1000, temp_range=(20, 80), conc_range=(0.1, 1.0), flow_range=(1, 10),
                         volume_range=(1, 5), rate_constant_range=(0.01, 0.1)):
    """Generates data for a simple CSTR with a first-order reaction."""

    data = []

    for _ in range(num_samples):
        temperature = np.random.uniform(temp_range[0], temp_range[1])
        inlet_concentration = np.random.uniform(conc_range[0], conc_range[1])
        flow_rate = np.random.uniform(flow_range[0], flow_range[1])
        reactor_volume = np.random.uniform(volume_range[0], volume_range[1])
        rate_constant = np.random.uniform(rate_constant_range[0], rate_constant_range[1])

        # Calculate space time
        space_time = reactor_volume / flow_rate

        # Calculate conversion
        conversion = (space_time * rate_constant) / (1 + space_time * rate_constant)
        conversion = min(1.0, max(0.0, conversion))  # Ensure conversion is within 0-1

        data.append([temperature, inlet_concentration, flow_rate, reactor_volume, rate_constant, conversion])

    df = pd.DataFrame(data, columns=['temperature', 'inlet_concentration', 'flow_rate', 'reactor_volume', 'rate_constant', 'conversion'])
    return df

# Generate the data
cstr_data = generate_cstr_data(num_samples=1000)

# Feature Engineering (Consider Carefully):
# In this case, using the raw features *might not* be the best approach because the underlying equation involves `space_time`.
# Let's create a feature for space time explicitly:
cstr_data['space_time'] = cstr_data['reactor_volume'] / cstr_data['flow_rate']

# Prepare the data
X = cstr_data[['temperature', 'inlet_concentration', 'space_time', 'rate_constant']]  # Using space_time
y = cstr_data['conversion']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)  # Remove squared=False
rmse = np.sqrt(mse)  # Calculate RMSE manually
print(f"RMSE: {rmse}")

# Print the model coefficients
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")