# Anti-Cheating Browser

A restricted browser built using Python and PyQt for conducting coding assessments on HackerRank in a controlled environment.

The browser runs the exam inside a custom desktop application and restricts several actions that could be used for cheating such as accessing external coding resources, copying answers, or switching to other applications.

---

## Purpose

During coding assessments hosted on HackerRank, participants may attempt to open external websites, copy solutions, or switch to other applications to search for answers.

This project was created to provide a controlled browser environment where students can only interact with the test platform.

---

## Features

* Custom browser interface built with PyQt
* Embedded browsing using PyQtWebEngine
* Fullscreen exam environment
* Blocking of commonly used coding-help websites
* Clipboard clearing system to prevent copying and pasting
* Tab switching restriction (prevents switching to other applications)
* Multiple experimental browser versions
* Version 4 is currently the most stable implementation

---

## Blocked Websites

The browser blocks access to commonly used coding or AI assistance platforms, including:

* ChatGPT
* GeeksforGeeks
* Stack Overflow
* LeetCode
* CodeChef
* Codeforces
* GitHub

If the user attempts to navigate to any of these websites, the request is intercepted and the page is prevented from loading.

---

## How the Browser Works

The browser is built using PyQt5 and PyQtWebEngine which allow embedding a Chromium-based browser inside a Python application.

### 1. Custom Browser Window

A PyQt window is created which acts as the main browser interface.
This replaces the need for external browsers like Chrome or Edge.

---

### 2. Embedded Web Engine

PyQtWebEngine loads web pages directly inside the application window.
The HackerRank test link is opened inside this embedded browser.

---

### 3. Navigation Request Interception

Every time the browser tries to load a URL, the request is intercepted before the page loads.

The program checks whether the URL belongs to a blocked domain.

Example logic:

* If URL contains `stackoverflow.com`
* or `chat.openai.com`
* or `leetcode.com`

then the navigation request is rejected.

This prevents the user from opening external help websites.

---

### 4. Clipboard Protection Mechanism

Instead of blocking keyboard shortcuts directly, the browser continuously clears the system clipboard.

A timer runs inside the application that resets the clipboard contents every **100 milliseconds**.

This means:

* If a user copies text using **Ctrl+C**, the clipboard is quickly cleared.
* If a user tries to paste using **Ctrl+V**, there is no content available to paste.

This effectively prevents copying and pasting answers during the test.

---

### 5. Tab Switching Restriction

The browser detects when the application loses focus (for example when a user presses **Alt+Tab** or tries to switch windows).

If the browser window loses focus:

* The application immediately regains focus.
* The user is forced back into the exam window.

This prevents switching to other applications such as:

* web browsers
* messaging apps
* search engines
* AI tools

---

### 6. Allowed Platform

The HackerRank test environment is allowed to load normally and users can solve coding problems directly within the browser.

---

## Project Structure

```id="h8r2li"
ACM_BROWSER
│
├── src/
│   ├── ACM_BROWSER1.py
│   ├── ACM_BROWSER2.py
│   ├── ACM_BROWSER3.py
│   ├── ACM_BROWSER4.py   ← Stable version
│   └── ACM_BROWSER5.py
│
├── assets/
│   └── acm_logo.ico
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository

```id="9mlc8o"
git clone https://github.com/YOUR_USERNAME/Anti-Cheating-Browser.git
```

Navigate to the project directory

```id="clq6ym"
cd Anti-Cheating-Browser
```

Create a virtual environment

```id="o4iayk"
python -m venv venv
```

Activate the environment

Windows:

```id="9q6h3v"
venv\Scripts\activate
```

Mac / Linux:

```id="w9ivj4"
source venv/bin/activate
```

Install dependencies

```id="6r6l8g"
pip install -r requirements.txt
```

---

## Running the Browser

Run the stable browser version

Windows:

```id="4p3m4b"
python src/ACM_BROWSER4.py
```

Mac / Linux:

```id="6vshb6"
python3 src/ACM_BROWSER4.py
```

---

## Technologies Used

* Python
* PyQt5
* PyQtWebEngine

---

## Future Improvements

* Activity logging during exams
* Webcam monitoring
* AI-based cheating detection
* Server-based exam integration
* Advanced browser restriction policies

---

## Disclaimer

This browser provides basic restrictions to reduce cheating during online assessments but cannot guarantee complete prevention of all cheating methods.

---

## Author

Himanshu