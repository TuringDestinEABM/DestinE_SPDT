Information about how to run tests goes into this file

## Python Unit tests


1. Create a virtual environment (first time only)

(Windows)
```bash
python -m venv venv_test
```
(Linux)
```bash
/usr/local/bin/python3 -m venv venv_test 
```

2. Activate environment

(Windows)
```bash
venv_test\Scripts\activate
```
(Linux)
```bash
source venv_test/bin/activate
```

3. Install requirements.txt 
```bash
pip install -r requirements.txt
```

4. Install testing packages
```bash
pip install pytest pytest-cov
```
5. Move into test folder
```bash
cd ./tests
```

6. Run tests
```bash
 pytest --cov=fizzbuzz --cov-report=term-missing
```