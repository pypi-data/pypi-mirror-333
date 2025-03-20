# Conversion Unit Library

### CLI Usage Demo

![Unit Conversion CPL](https://raw.githubusercontent.com/Minkeez/conversion_unit/main/CLI.png)

### REST API Usage Demo

![Unit Conversion REST API](https://raw.githubusercontent.com/Minkeez/conversion_unit/main/API.png)

### 📌 Overview

A powerful Python library for unit conversion, supporting **CLI and REST API**. Convert units effortlessly for length, weight, volume, time, speed, and more!

### 🔥 Features

- ✅ **CLI Support**: Run conversions from the command line
- ✅ **FastAPI REST API**: Convert units via HTTP requests
- ✅ **Comprehensive Units**: Includes length, mass, volume, temperature, energy, and more
- ✅ **Custom Units**: Add your own conversions dynamically

### 🚀 Installation

```sh
pip install conversion_unit
```

### 🔧 Usage

#### **1️⃣ CLI Mode**

```sh
convert 5 km to m
# Output: 5000.0
```

#### **2️⃣ Python Library**

```python
from conversion_unit import convert
result = convert(5, "km", "m")
print(result)  # 5000.0
```

#### **3️⃣ REST API Mode**

Run the API server:

```sh
python -m conversion_unit
```

Then access:

```http
GET http://localhost:8000/convert?value=5&from_unit=km&to_unit=m
```

Response:

```json
{ "result": 5000.0 }
```

### 📜 License

This project is licensed under the **[MIT License](./LICENSE)**.

### 🌍 Contribute

Pull requests are welcome! Open an issue to suggest features or improvements.

### ⭐ Support the Project

If you find this project useful, give it a ⭐ on [GitHub](https://github.com/Minkeez/conversion_unit)!
