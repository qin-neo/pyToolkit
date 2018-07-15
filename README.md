# pyToolkit
Windows shortcut with parameters

  Left-Click on Alias button: execute shortcut<br/>
  Right-Click on Alias button: open main folder<br/>
  Right-Click in text-entry: copy select text<br/>
  Mid-Click in text-entry: clean text-entry<br/>
  REMOVE button: enable "-" button to remove shortcut<br/>

![alt text](https://github.com/qin-neo/pyToolkit/blob/master/example.PNG)

Examples:
  "main": "D:/Tools/PortableGit/git-cmd.exe"
   - shutdown windows:
     shutdown /p
   - Hibernate
     shutdown /h
   - run cmd in specific path
     E: & cd  "Z:/github/pyToolkit"

  Start VBox headless
  "main": "C:/Program Files/Oracle/VirtualBox/VBoxManage.exe"
   - startvm --type headless u1804

  Start servel web pages
  "main": "D:/Tools/MaxthonPortable/Bin/Maxthon.exe"
   - https://github.com/qin-neo/pyToolkit https://github.com/qin-neo/

  git-bash SSH
  "main": "D:/Tools/PortableGit/git-bash.exe"
  - -c 'ssh -o "StrictHostKeyChecking no" root@192.168.56.101

  Run python script
    "pyToolKit": {
        "folder": "D:/scripts/github_pyToolkit", 
        "interpreter": "C:/pypy2/pypyw.exe", 
        "list": [
            ""
        ], 
        "main": "D:/scripts/github_pyToolkit/toolkit.py"
    }