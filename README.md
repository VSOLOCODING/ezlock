# 🔒 EzLock™ V1.0.0 - Secure File Encryption Suite

**An open-source file encryption tool released under the MIT License**

---
```
### Bitcoin Address:
bc1qm6pwqdrew7www4e92mahnf7rqwvmkhwrpyqjn5
```
---
---

## 📋 About the Project

EzLock™ is a secure file encryption application designed with **AES-256-GCM encryption (zero-header format)**. It supports account-based encryption, password-based sharing, folder auto-encryption, secure file editing, and built-in media preview tools.

⚠️ This is an **open-source hobby project** and is still slightly unfinished. Contributions, fixes, and improvements are welcome!

---

## 🔓 Open Source License (MIT)

This project is fully open source under the **MIT License**.

You are free to:

- ✔ Use it commercially  
- ✔ Modify it  
- ✔ Distribute it  
- ✔ Use it privately  

**Requirement:**  
You must include the original copyright and license in all copies or substantial portions.

---

## ⚠️ Important Notice - Folder Security



Secure folders ONLY auto-encrypt files while EzLock™ 
is actively running in the background. 
 
If you close the app, protection STOPS immediately. 
 
Keep EzLock™ minimized to maintain protection. 



---

## 🚀 Features

| Feature | Description | Status |
|--------|-------------|--------|
| 🔐 Zero Headers Encryption | No readable metadata in files | ✅ Working |
| 👤 Account Encryption | Files tied to user account | ✅ Working |
| 🔑 Password Encryption | Shareable encrypted files | ✅ Working |
| 📁 Folder Security | Auto-encrypt monitored folders | ⚠️ Requires running app |
| ✏️ Secure Edit | Edit encrypted files safely | ✅ Working |
| 🖼️ Image Preview | View without decrypting to disk | ✅ Working |
| 🎥 Video Preview | Basic playback support | ⚠️ Needs OpenCV |
| 🔊 Audio Preview | Waveform + playback | ⚠️ Needs extra deps |
| 📄 PDF Preview | Basic viewing support | ⚠️ Needs PyMuPDF |
| 💻 CLI Interface | Full terminal control | ✅ Working |
| 🖥️ GUI Interface | Graphical UI | ⚠️ Minor bugs |

---

## 🚧 Project Status

- ✅ Core encryption/decryption working  
- ✅ CLI fully functional  
- ⚠️ GUI has minor UI issues  
- ⚠️ Some preview features may crash on invalid files  
- ❌ Folder security does not persist after app closes  

---

## ⚡ Quick Start

### 📦 Install Dependencies
```bash
pip install cryptography argon2-cffi watchdog
```
▶️ Run CLI
```
python ezlock.py
```
🖥️ Run GUI
```
python ezlock.py --gui
```
🔑 First Time Setup
```
> register
Username: yourname
Password: ********
```
```
> login
Username: yourname
Password: ********
```
🔐 Encryption Usage
```
Account-based encryption
> enc secret.txt
Password-based encryption
> enc -p mypassword file.pdf
```
```
Decryption
> dec secret.txt.ezlock
> dec -p mypassword file.pdf.ezlock
```
📁 Folder Security (Experimental)

⚠️ Requires EzLock™ to stay running.
```
CLI
> secure ./Documents
Include subfolders? (y/n): y
Use password? (y/n): n
```
Manage folders
```
> folders
> unsecure ./Documents
```

⌨️ CLI Commands
```
Account --> User authentication and account management
```
```
register --> Create a new EzLock account
```
```
login --> Sign into your account
```
```
logout --> Sign out of current session
```
```
whoami --> Show current logged-in user
```
```
users --> List all registered users
```
```
Files --> File and directory operations
```
```
ls, cd, pwd --> List files, change directory, show current path
```
```
mkdir <name> --> Create a new folder
```
```
rm, mv, cp --> Delete, move/rename, or copy files
```
```
Encryption --> Secure file encryption tools'
```
```
enc <file> --> Encrypt file using account key
```
```
enc -p <file> --> Encrypt file using password
```
```
dec <file.ezlock> --> Decrypt encrypted file
```
```
preview <file> --> Preview encrypted file (in-memory only)
```
```
edit <file> --> Secure edit file with auto re-encryption
```
```

System --> Application control commands
```
```
clear --> Clear terminal screen
```
```
history --> Show command history
```
```
memwipe --> Wipe sensitive memory data
```
```
gui --> Launch graphical interface
```
```
exit --> Close EzLock safely
```


🖥️ GUI Shortcuts
Shortcut	Action
Ctrl + E	Encrypt (Account)
Ctrl + Shift + E	Encrypt (Password)
Ctrl + D	Decrypt
Ctrl + P	Preview
F5	Refresh
Delete	Remove file
📦 Supported File Format
Extension	Description
.ezlock	Encrypted file format (zero headers)

Example:

secret.txt.ezlock
- 🔒 Security Features
- AES-256-GCM encryption
- Argon2id key derivation
- HMAC-SHA256 integrity checks
- Zero metadata storage
- Memory-only password handling
- Auto memory wipe on exit

⚠️ Warning: Lost passwords cannot be recovered.

📋 Requirements
- Core
- Python 3.8+
- cryptography
- argon2-cffi
- watchdog
### Optional
- opencv-python (video)
- pygame + pydub (audio)
- Pillow (images)
- PyMuPDF (PDF)
🤝 Contributing

### This is an open-source project and contributions are welcome!

- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📝 Improve documentation
- 💰 Support Development

⚠️ Disclaimer

This software is provided "as is" without warranty.
It is a hobby project and may contain bugs.

Always keep backups of important files before encryption.
--- 
📌 Version History
- V1.0.0
- Initial open-source release
- MIT License
- CLI + GUI working
- Core encryption system complete
- Experimental folder security added
🔒 EzLock™ V1.0.0

Open Source. Secure. Lightweight. Experimental.

### Made with ❤️ by Ezcode™(Ezcool Entities™ )

--- 
