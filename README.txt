⏰ Telegram Reminder Bot with aiogram 3

Never forget an important task again! This bot helps you set reminders directly in Telegram, ensuring you stay on top of your schedule.
Whether it’s a meeting, workout, or daily habit, this bot will remind you right on time!

✅ What does it do?

 • 📅 Allows users to set one-time or recurring reminders
 • 🔔 Sends notifications exactly when you need them
 • 📋 Lists and manages existing reminders
 • 🛠️ Built with aiogram 3 for fast and efficient performance

🔧 Features

✅ Easy-to-use commands for setting reminders
✅ Customizable notifications for personal or work tasks
✅ Reliable and precise scheduling

📩 Want to organize your time effectively?

Contact me on Telegram, and I’ll help you set up this bot to improve your productivity! 🚀

# Instructions for installing and launching a Telegram bot for reminders

This file contains detailed instructions for installing and running a Telegram bot for managing reminders. The instructions are available for both Windows and Linux.

## CONTENTS:
1. [Install and run on Windows](#windows)
2. [Install and run on Linux](#linux)
3. [General instructions](#general-instructions)
4. [Possible problems] (#possible-problems)

---

<a name="windows"></a>
## INSTALL AND RUN ON WINDOWS

### Step 1: Install Python 3.11

IMPORTANT**: It is not recommended to install Python 3.13 or higher, as they may cause problems when installing bot dependencies.

1. Download Python 3.11:
- Go to the website https://www.python.org/downloads /
- Find and click on the link "Python 3.11.x" (for example, Python 3.11.7)
- Click on the "Download" button

2. Install Python:
   - Run the downloaded file (for example, python-3.11.7-amd64.exe )
- **BE SURE TO** check the box "Add Python 3.11 to PATH" at the bottom of the installer window
   - Click "Install Now" and wait for the installation to complete

3. Check the installation:
   - Press Win+R, type "cmd" and press Enter to open the command prompt
   - Enter: `python --version`
   - You should see something like "Python 3.11.7"

### Step 2: Preparing the bot folder and files

1. Create a folder for the bot:
   - Open the command prompt (Win+R, type "cmd", press Enter)
   - Enter the commands:
   ```
   mkdir C:\TelegramBot
   cd C:\TelegramBot
   ```

2. Create a bot file:
   - In the command prompt, type:
   ```
   notepad reminder_bot.py
``
- Copy and paste the bot code into the Notebook that opens
   - Save the file (Ctrl+S)

### Step 3: Install the necessary libraries

1. Install the aiogram library:
- On the command line (make sure you are in the folder C:\TelegramBot ) enter:
   ```
   pip install aiogram==2.25.1
``
- Wait for the installation to complete

### Step 4: Setting up and launching the bot

1. Get a token for the bot:
   - Open Telegram and find @BotFather
   - Send the `/newbot` command
   - Follow the instructions: specify the bot's name and username
. Save the token that BotFather will send you.

2. Set up the bot:
   - Open the file reminder_bot.py (the `notepad' command reminder_bot.py `)
   - Find the string `TOKEN = "YOUR_BOT_TOKEN"`
- Replace YOUR_BOT_TOKEN with your BotFather token (keeping the quotes)
- Save the file (Ctrl+S)

3. Launch the bot:
   - In the command prompt, type:
   ```
   python reminder_bot.py
``
- If everything is correct, you will see messages about the launch of the bot

4. Create a file for convenient launch of the bot in the future:
- Open Notepad and enter:
   ```
   @echo off
   cd /d C:\TelegramBot
   python reminder_bot.py
   pause
   ``
- Save as "start_bot.bat" in the folder C:\TelegramBot
   - Now it's enough to double-click on this file to launch the bot.

---

<a name="linux"></a>
## INSTALL AND RUN ON LINUX

### Step 1: Install Python 3.11

IMPORTANT**: It is recommended to use Python 3.11 rather than newer versions to avoid dependency issues.

1. Update the package list and install the necessary tools:
   ```
   sudo apt update
   sudo apt install software-properties-common -y
   ```

2. Add a repository with Python 3.11:
``
   sudo add-apt-repository ppa:deadsnakes/ppa -y
   sudo apt update
   ```

3. Install Python 3.11 and pip:
``
   sudo apt install python3.11 python3.11-venv python3-pip -y
   ```

4. Check the installation:
``
   python3.11 --version
   ```
   You should see "Python 3.11.x"

### Step 2: Preparing the bot folder and files

1. Create a folder for the bot:
   ```
   mkdir ~/telegram-bot
   cd ~/telegram-bot
   ```

2. Create a bot file:
   ```
   nano reminder_bot.py
``
- Copy and paste the bot code into the editor that opens
   - Press Ctrl+O to save, then Enter, then Ctrl+X to exit

### Step 3: Create a virtual environment and install dependencies

1. Create a virtual environment:
   ```
   python3.11 -m venv venv
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
   After activation, (venv) should appear at the beginning of the terminal line

3. Install the aiogram library:
   ```
   pip install aiogram==2.25.1
   ```

### Step 4: Setting up and launching the bot

1. Get a token for the bot:
   - Open Telegram and find @BotFather
   - Send the `/newbot` command
   - Follow the instructions: specify the bot's name and username
. Save the token that BotFather will send you.

2. Set up the bot:
   ```
   nano reminder_bot.py
   ```
   - Find the string `TOKEN = "YOUR_BOT_TOKEN"`
- Replace YOUR_BOT_TOKEN with your BotFather token (keeping the quotes)
- Save the file (Ctrl+O, Enter, Ctrl+X)

3. Launch the bot:
   ```
   python reminder_bot.py
   ```

4. Create a script for easy launch:
``
   nano start_bot.sh
   ```
   Enter:
   ```
   #!/bin/bash
   cd ~/telegram-bot
   source venv/bin/activate
   python reminder_bot.py
   ```
   Save (Ctrl+O, Enter, Ctrl+X) and make the script executable:
``
   chmod +x start_bot.sh
   ```

5. To launch the bot in the future, use:
   ```
   ./start_bot.sh
   ```

### Step 5 (optional): Setting up Autorun on Linux

1. Create a systemd service file:
   ```
   sudo nano /etc/systemd/system/telegram-bot.service
   ```

2. Enter the following contents (replace "your_user name" with your Linux username):
``
   [Unit]
   Description=Telegram Reminder Bot
   After=network.target

   [Service]
   User=your user_name
   WorkingDirectory=/home/your user_name/telegram-bot
   ExecStart=/home/your username/telegram-bot/venv/bin/python /home/ваше_имя_пользователя/telegram-bot/reminder_bot.py
Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Save the file (Ctrl+O, Enter, Ctrl+X)

4. Turn on and start the service:
``
   sudo systemctl enable telegram-bot
   sudo systemctl start telegram-bot
   ```

5. Check the service status:
   ```
   sudo systemctl status telegram-bot
   ```

---

<a name="general instructions"></a>
## GENERAL INSTRUCTIONS FOR USING THE BOT

1. Find your Telegram bot by the username you specified when creating it.

2. Send the `/start` command to get started

3. Create reminders:
   - Send a message in the format: "Remind me in X hours/minutes: reminder text"
- For example: "Remind me in 1 hour: call mom"
   - Or: "Buy milk in 30 minutes"

4. Checking existing reminders:
- Send the command `/list`

---

<a name="possible-problems"></a>
## POSSIBLE PROBLEMS AND THEIR SOLUTIONS

### Problems installing libraries on Windows

1. **Access rights errors**:
- Run the command prompt as an administrator: right-click on the Start menu > Command prompt (administrator)
- Repeat the installation command: `pip install aiogram==2.25.1`

2. **Encoding problems on the command line**:
- Enter the command: `chcp 1251` or `chcp 65001`
   - Or use PowerShell instead of the command line

3. **Errors when installing dependencies with Rust**:
- This is one of the reasons why we recommend aiogram 2.25.1 instead of 3.x
- If you still need version 3.x, first install Rust from the official website https://www.rust-lang.org/tools/install

### Problems running on Linux

1. **No script execution rights**:
``
   chmod +x start_bot.sh
   ```

2. **Dependency issues**:
``
   pip install --upgrade pip
   pip install aiogram==2.25.1
   ```

3. **Problems with the virtual environment**:
``
   deactivate
   rm -rf venv
   python3.11 -m venv venv
   source venv/bin/activate
   pip install aiogram==2.25.1
   ```

### The bot is not responding

1. Make sure that the bot is running and there are no error messages in the console.
2. Check if you entered the token correctly in the file. reminder_bot.py
3. Check your internet connection

### Reminders are not coming

1. Make sure that the bot is up and running
2. Check that the time on the computer is set correctly.
3. Check the reminder list with the `/list` command

---

If you have any other problems, try restarting the bot or contact the developer.
