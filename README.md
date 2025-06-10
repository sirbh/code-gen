## Setup

### Python version

To get the most out of this, please ensure you're using Python 3.11 or later. 
This version is required for optimal compatibility with LangGraph. If you're on an older version, 
upgrading will ensure everything runs smoothly.
```
python3 --version
```



### Create an environment and install dependencies
#### Mac/Linux/WSL
```
$ python3 -m venv code-gen-env
$ source code-gen-env/bin/activate
$ pip install -r requirements.txt
```
#### Windows Powershell
```
PS> python3 -m venv code-gen-env
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
PS> code-gen-env\scripts\activate
PS> pip install -r requirements.txt
```
