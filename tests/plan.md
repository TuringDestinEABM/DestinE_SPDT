## Overall strategy
1. Home page tests
2. Other linchpin tests
3. Implement Tox
4. Implement Github actions
5. Expand coverage

## Scope
- Behaviour of user visible functionality
- Loading and performance of web pages
- Input validation on forms
- Consider performance and user behaviour of MABM seperately? review with DB

## App structure
### data
- Do not test, static/user generated data only, to be replaced with data basing

### library
- forms.py: validate inputs
- getData: validate data, exceptions
- plotting: validate inputs, exceptions
- runSim: validate inputs, outputs, exceptions

### modelling
Discuss with DB. Likely to be final implementation

### routes
- GET/POST, exceptions, dummy tests for unimplemented pages 

### static
no tests

### templates
check standards

### __init.py__
check best practice

### digitalTwin.py
- basic routes  ***!Start here***
- other stuff? check with DB