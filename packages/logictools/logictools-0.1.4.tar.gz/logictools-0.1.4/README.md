## What I Learned from Task 1 - CI/CD-Based Python Package

### **Module: Agentic AI Framework (Prodigal AI)**

In the first task, I was assigned to build a CI/CD based Python packa ge (funcationality of the Python package was upto us we could create a simple python package).

### **1️⃣ Understanding CI/CD in Python Packaging**
- CI/CD (Continuous Integration & Continuous Deployment) automates the build, test, and deployment of software.

- It helps in maintaining high-quality code and streamlining software updates.

---

### **2️⃣ Steps to Build a Python Package**
- **Step 1:**
  - Create a **seperate project folder** for your Python Package.
  - The name of the Folder should be the name what you want to give it to your Python Package.

- **Step 2:**
  - Inside your project folder, you need to create few folders and files.
  - **Package Souce Code Folder:**
    - Create a folder for your package source code.
    - Inside the Package Souce Code folder you will be writing your code in `main.py` (you can split your code accross multiple number of `.py` files if needed).
    - You must also create a Python Special file named `__init__.py` inside this folder.
  
  - **Testing Folder**
    - After, completing of your code, you should test it. For this, create a seperate folder named `tests`.
    - Inside the `tests` folder, create a `test_main.py` file to write test cases.
  
  - **GitHub Actions CI/CD Setup:**
    - Create a `.githuh` folder to set up **GitHub Actions CI/CD.**
    - Inside `.github`, create another folder named `workflows`.

    - Inside `workflows`, create a `.yml` file for CI/CD. This file should be named after your project, such as `your-project-name.yml`(eg: my_package.yml).

  - **Additional Files:**
  
    - `.gitignore` – To ignore unnecessary files from being tracked by Git.
  
    - `pyproject.toml` – For modern package configuration.

    - `README.md` – To provide documentation for the package.
    
    - `LICENSE.txt` – To define the package’s license.
    
    - `requirements.txt` – To list package dependencies.
---

### Here is the Structure in visual form:
```bash
my_package/
│── my_package/            # Package source code
│   ├── __init__.py        # Required for a Python package
│   ├── main.py            # Main module
│
│── tests/                 # Unit tests
│   ├── test_main.py
│
│── .github/               # GitHub Actions CI/CD
│   ├── workflows/
│       ├── python-package.yml
│
│── .gitignore             # Ignore unnecessary files
│── pyproject.toml         # Modern package configuration
│── README.md              # Documentation
│── LICENSE                # License file
│── requirements.txt       # Dependencies
```
---

### **3️⃣ Write Code for Your Package**
🔹 You need to write the code for your Package inside `main.py` which is present in your `my_package` folder.

🔹 Here is my code for `math_utils.py`:
```python
#Calculates the factorial of a number.
def factorial(n):
    try:
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    except ValueError as e:
        return f"{e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
```
---

🔹 Here is my code for `string_utils,py`:
```python
def convert_to_uppercase(text):
    return text.upper()  # Converts a string to uppercase.

def reverse_string(text):
    return text[::-1]  # Reverses a given string.

def character_count(text):
    return len(text)  # Returns the length of the string.
```
---

🔹**Now add the created files inside `__init__.py`**
```python
from .string_utils import convert_to_uppercase, reverse_string, character_count
from .math_utils import factorial
```
---

### **4️⃣ Code Test**
- Now, after writing the code we must test it by Unit Test:
  - You must test for all files.
  - Here is the test code for `math_utils.py` file.

    ```python
    import pytest
    from logictools import math_utils

    def test_factorial():
        assert math_utils.factorial(5) == 120
        assert math_utils.factorial(0) == 1
    ```
---

 - Here is the test code for `string_util.py` file.
    ```python
    import pytest
    from logictools import string_utils

    def test_convert_to_uppercase():
        assert string_utils.convert_to_uppercase("hello") == "HELLO"

    def test_reverse_string():
        assert string_utils.reverse_string("hello") == "olleh"

    def test_character_count():
        assert string_utils.character_count("Hello") == 5
    ```
---

### **5️⃣ Content inside `pyproject.toml` file**
- This is the modern way to define a package.

    🔹 `pyproject.toml`
```toml
[tool.poetry]
name = "logictools"           # Name of your package
version = "0.1.3"             # Current version of your package
description = "A simple utility package for string and math functions"
authors = ["RANGDAL PAVANSAI <psai49779@gmail.com>"]
license = "MIT"               # License type (MIT in this case)
readme = "README.md"          # Points to your README file

[tool.poetry.dependencies]
python = "^3.7"               # Your package supports Python 3.7 and later.

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"               # Your package requires pytest version 7.0 or higher for testing.

[build-system]
requires = ["poetry-core>=1.0.0"]       # Specifies that poetry-core (version 1.0.0 or later) is required to build the package.
build-backend = "poetry.core.masonry.api"    # Uses poetry.core.masonry.api as the build system.
```

---

### **6️⃣ Create `requirements.txt`**
- This lists dependencies
  ```sh
  touch requirements.txt
  ```

- In `requirements.txt` add the packages that are required or your project to run.

---

### **7️⃣ Create `.gitignore`**
- To ignore unnecessary files:
  ```markdown
  # Ignore Python cache & build files
  __pycache__/
  *.pyc
  *.pyo
  *.pyd
  *.egg-info/
  build/
  dist/
  venv/
  ```

### **8️⃣ Build & Test Your Package Locally**
  
**1. Install `build` Tool**
   
  ```sh
  pip install build
  ```
  
 **2. Build your package**

  ```sh
  python -m build
  ```

- This creates a `dist/` folder containing:

  ```pgsql
  dist/
    my_package-0.1.0-py3-none-any.whl
    my_package-0.1.0.tar.gz
  ```

**3. Test Your Package**

```sh
pip install dist/NAME-OF-YOUR-PACKAGE-0.1.0-py3-none-any.whl
python -c "import NAME-OF-YOUR-PACKAGE; print(NAME-OF-YOUR-PACKAGE.factorial(5))"
```

### **9️⃣ Set Up GitHub Actions for CI/CD**

1. Create `.github/workflows/python-package.yml`

    ```yaml
    name: Python Package CI/CD

    on:
      push:
        branches:
          - main
      pull_request:
        branches:
          - main
      release:
        types: [created]

    jobs:
      test:
        name: Run Tests
        runs-on: ubuntu-latest

        steps:
          - name: Checkout repository
            uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.10'

          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
              pip install pytest

          - name: Run tests
            run: pytest

      build:
        name: Build and Publish Package
        runs-on: ubuntu-latest
        needs: test
        if: github.event_name == 'release'

        steps:
          - name: Checkout repository
            uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.10'

          - name: Install Build Tools
            run: |
              python -m pip install --upgrade pip
              pip install build twine

          - name: Build Package
            run: python -m build

          - name: Publish to PyPI
            env:
              PYPI_USERNAME: ${{ secrets.PYPI_USERNAME }}
              PYPI_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
            run: |
              twine upload dist/* -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD"
    ```

### **🔟 Securely Store PyPI Credentials**

1. Go to your **GitHub repo → Settings**
2. Click **Secrets and variables → Actions**
3. Add these **GitHub Secrets:**
  
   - `PYPI_USERNAME` → Your PyPI username
   - `PYPI_PASSWORD` → Your PyPI API Token (from https://pypi.org/manage/account/)

### **1️1 Publish Your Package**

1. **Push to GitHub**

    ```sh
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/yourusername/my_package.git
    git push -u origin main
    ```

2. **Create a GitHub Release**

- Go to **GitHub** → **Releases** → **Create New Release**
- Tag it as **v0.1.3** (match `pyproject.toml` version)
- Click **Publish Release**
- **GitHub Actions will automatically build & upload your package to PyPI**!

### **12. Confirmation of Package**

- After uploading successfull go check `github actions`.
- If it successfully completes it's job that means your package is ready to use.
- Now, confirm your pip package in https://pypi.org/YOUR-PACKAGE-NAME.

### **13. Install, and use**

```sh
- pip install NAME-OF-YOUR-PACKAGE
- python -c "import NAME-OF-YOUR-PACKAGE; print(NAME-OF-YOUR-PACKAGE.factorial(5))"
```