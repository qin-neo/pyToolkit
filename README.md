# pyToolkit
Windows shortcut with parameters

  Left-Click on Alias button: execute shortcut.<br>
  Right-Click on Alias button: open main folder.<br>
  Right-Click in text-entry: clean text-entry, and trigger dropdown.<br>
  Mid-Click in text-entry: remove chosen line from history.<br>
  Double-Click in text-entry: select all and copy.<br>
  REMOVE button: enable "-" button to remove shortcut.<br>
  CountDown button: start a timer on upper right corner of screen.<br>
    Left-Click on timer: reset timer.<br>
    Right-Click on timer: exit timer.<br>

![alt text](https://github.com/qin-neo/pyToolkit/blob/master/example.PNG)

Examples:
  "main": "D:/Tools/PortableGit/git-cmd.exe"
   - shutdown windows:
     shutdown /p
   - Hibernate
     shutdown /h ^& exit
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