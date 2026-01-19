# Testing reMarkacord

## Prerequisites

- Go 1.21 or later
- reMarkable tablet or emulator (optional, for on-device testing)
- Access to the `appload` environment (e.g., reMarkable frame buffer access if running full UI)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/StarNumber12046/reMarkacord.git
    cd reMarkacord
    ```

2.  **Configuration:**
    Create a config file at `~/.config/reMarkacord/.env`:
    ```env
    DISCORD_TOKEN=your_token_here
    ```

## Building

To build the backend for the host (PC):
```bash
go build -o reMarkacord
```

To cross-compile for reMarkable 2 (armv7):
```bash
GOOS=linux GOARCH=arm GOARM=7 go build -o reMarkacord-rm2
```

## Running the Backend Stub

The backend listens on a Unix domain socket passed as the first argument.

To test the backend manually without the full `appload` loader, you can use `socat` to simulate the connection.

1.  **Start the backend:**
    ```bash
    # Create a dummy socket location
    touch /tmp/appload.sock
    rm /tmp/appload.sock
    
    # Run the app, pointing to the socket
    ./reMarkacord /tmp/appload.sock
    ```

2.  **Send commands (in another terminal):**
    Use a tool to write to the Unix socket. The protocol uses binary headers.

    *Note: The protocol requires specific binary framing (MsgType + Length).*

## Protocol Testing

The app supports the following stubbed message types:
- `10` (GetChannelsRequest) -> Returns list of channels
- `11` (GetMessagesRequest) -> Returns messages for a channel
- `12` (SendMessageRequest) -> Logs message to stdout

## Integration

Deploy `reMarkacord-rm2`, `manifest.json`, and the `ui/` folder (once created) to the reMarkable's app loader directory.
