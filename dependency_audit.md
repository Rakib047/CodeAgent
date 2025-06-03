**Python Version** : 2.7.18

| Package         | Version | Latest     | Type  |
|-----------------|---------|------------|-------|
| chardet         | 3.0.4   | 4.0.0      | wheel |
| futures         | 3.3.0   | 3.4.0      | wheel |
| idna            | 2.6     | 2.10       | wheel |
| python-dateutil | 2.7.5   | 2.9.0.post0| wheel |
| requests        | 2.18.4  | 2.27.1     | wheel |
| six             | 1.15.0  | 1.17.0     | wheel |
| urllib3         | 1.22    | 1.26.20    | wheel |

### Dependency Tree

enum34==1.1.10
futures==3.3.0
pipdeptree==2.2.1
  - pip [required: >=6.0.0, installed: 20.3.4]
python-dateutil==2.7.5
  - six [required: >=1.5, installed: 1.15.0]
requests==2.18.4
  - certifi [required: >=2017.4.17, installed: 2021.10.8]
  - chardet [required: >=3.0.2,< 3.1.0, installed: 3.0.4]
  - idna [required: >=2.5,<2.7, installed: 2.6]
  - urllib3 [required: >=1.21.1,<1.23, installed: 1.22]
setuptools==44.1.1
wheel==0.37.1


### Static Code security scan

**Code scanned**:
        Total lines of code: 500766
        Total lines skipped (#nosec): 0

**Run metrics**:
        Total issues (by severity):
                Undefined: 0
                Low: 2693
                Medium: 72
                High: 41
        Total issues (by confidence):
                Undefined: 0
                Low: 2
                Medium: 36
                High: 2768
**Files skipped (5)**:
        ./logger.py (syntax error while parsing AST from file)
        ./tests.py (syntax error while parsing AST from file)
        ./utils.py (syntax error while parsing AST from file)
        ./venv/lib/python2.7/os.py (syntax error while parsing AST from file)
        ./venv/lib/python2.7/site-packages/concurrent/futures/_base.py (syntax error while parsing AST from fil


### Safety Scan

Safety 3.5.1 scanning /Users/rakibabdullah/Desktop/legacy_repo
2025-06-03 05:46:04 UTC

Account: Rakib Abdullah, rakibabdullah047@gmail.com 
 Environment: development
 Scan policy: None, using Safety CLI default policies

Python detected. Found 1 Python requirement file and 2 Python environments

Dependency vulnerabilities detected:

📝 requirements.txt:

 requests==2.18.4 [3 vulnerabilities found]                                                                    
 Update requests==2.18.4 to requests==2.32.2 to fix 3 vulnerabilities                                          
 Versions of requests with no known vulnerabilities: 2.32.3                                                    
 Learn more: https://data.safetycli.com/p/pypi/requests/eda/?from=2.18.4&to=2.32.2                             

✅ py3env/pyvenv.cfg: No issues found.

✅ venv/pyvenv.cfg: No issues found.

Tested 30 dependencies for security issues using default Safety CLI policies
29 vulnerabilities found, 26 ignored due to policy.
1 fix suggested, resolving 3 vulnerabilities.