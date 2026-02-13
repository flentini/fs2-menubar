# FreeStyle Libre 2+ Menubar

A macOS menubar app that displays real-time glucose readings from a FreeStyle Libre 2+ sensor.

See your current glucose level and trend arrow at a glance without checking your phone.

```
┌─────────────┐     HTTPS/REST      ┌──────────────────┐
│ LibreLinkUp  │ ◄─── poll/60s ──── │    Menubar App    │
│  Cloud API   │ ───── glucose ────► │  (Python + rumps) │
└─────────────┘                      └──────────────────┘
```

## 📡 Setting Up Data Sharing

Before using the menubar app, you need to share your glucose data from the LibreLink app to the LibreLinkUp cloud.

### 1. Invite a follower from LibreLink

- Open the **LibreLink** app on your phone (the one connected to your sensor)
- Go to **Connected Apps** or **Sharing** in the menu
- Tap **Add Connection** and enter an email address to invite as a follower
- You can use your own second email address — it just needs to be different from your LibreLink account

### 2. Set up LibreLinkUp

- Check the invitation email and follow the link
- Download the **LibreLinkUp** app on your phone
- Create a new account using the **same email address** the invitation was sent to
- Once signed in, you should see the shared glucose data in the app

### 3. Note your credentials

The email and password you just used to create the LibreLinkUp account are what the menubar app needs to pull your data.

## 🛠️ Installation

### Prerequisites

- macOS
- Python 3.11+

### Steps

```bash
git clone git@github.com:flentini/fs2-menubar.git
cd fs2-menubar
cp .env.example .env
```

Edit `.env` with your LibreLinkUp credentials:

```
LIBRE_USERNAME=your_librelinkup_email@example.com
LIBRE_PASSWORD=your_librelinkup_password
```

Then run the install script:

```bash
./install.sh
```

This will create a virtual environment, install dependencies, and register a Launch Agent that starts automatically at login.

## 🚀 Usage

After installation, the app appears in your menu bar:

- **`105 →`** — current glucose (mg/dL) and trend arrow
- **`⚠ --`** — error or no data available

Click the icon to see:

- Last reading timestamp
- High/Low alert (when applicable)
- **Refresh Now** — fetch the latest reading immediately
- **Quit**

It polls for new data every 60 seconds, matching the sensor's update frequency. You'll also get macOS notifications when glucose goes high or low.

## 🧪 Running Manually

If you prefer to run it from a terminal instead of as a service:

```bash
source .venv/bin/activate
python main.py
```

## 🗑️ Uninstalling

```bash
launchctl unload ~/Library/LaunchAgents/com.fs2-menubar.plist
rm ~/Library/LaunchAgents/com.fs2-menubar.plist
```
