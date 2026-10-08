# OpenClaw Web UI launcher (Windows)

For an OpenClaw gateway running on a **remote machine** with its bind set to **loopback** (local only). That's the safe setting, but it means the Control UI isn't reachable from your PC directly. `openclaw_gui.bat` does three things:

1. Opens an SSH tunnel from `localhost:<port>` on your PC to the gateway's loopback port on the server.
2. Opens the Control UI in its own Chrome or Edge app window.
3. Closes the tunnel when you close that window.

The tunnel listens on `127.0.0.1` only, so nothing on your network can use it.

## Requirements

- Windows 10 or 11 with the **OpenSSH Client** (Settings → System → Optional features). It's installed by default on most systems.
- SSH access to the machine running OpenClaw.
- Chrome or Edge for the app window. Without either, it falls back to your default browser.

## Usage

```bat
openclaw_gui.bat                         :: uses your config, or prompts
openclaw_gui.bat user@my-server          :: one-off, default port 18789
openclaw_gui.bat user@my-server 18789 28789   :: remote port 18789, local port 28789
openclaw_gui.bat --help
```

On first run with no config, it asks for the host and SSH user and offers to save them.

## Configuration

Copy `openclaw_gui.config.example.cmd` to `openclaw_gui.config.cmd` in the same folder and edit it. That file is git-ignored, so your host details stay out of the repo.

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `OPENCLAW_HOST` | *(required)* | Machine running the OpenClaw gateway |
| `OPENCLAW_USER` | your SSH config or Windows user | SSH login |
| `OPENCLAW_SSH_PORT` | `22` | SSH port |
| `OPENCLAW_SSH_KEY` | *(none)* | Private key file, for passwordless login |
| `OPENCLAW_REMOTE_PORT` | `18789` | Gateway port on the server |
| `OPENCLAW_LOCAL_PORT` | same as remote | Port on your PC |
| `OPENCLAW_BROWSER` | auto-detect | Path to `chrome.exe` or `msedge.exe` |
| `OPENCLAW_KEEP_PROFILE` | *(off)* | Set to `1` to keep the app window's browser profile so the UI stays signed in |

Priority: command-line arguments, then environment variables, then the config file, then prompts.

**Tip:** with an SSH key (`OPENCLAW_SSH_KEY`, or a `Host` entry in `~/.ssh/config`) there's no password prompt and the tunnel opens almost instantly.

## Troubleshooting

| Message | Likely cause |
| :--- | :--- |
| *SSH connection closed before the tunnel opened* | Wrong password or user, host unreachable, or nothing listening on the remote port. Run `ssh user@host` by hand to check the login, then confirm the gateway is running on the server. |
| *Local port … is already in use* | A tunnel from an earlier run is still open (choose **O** to reuse it), or another program uses that port (pass a different local port). |
| *ssh was not found* | Install the Windows OpenSSH Client feature. |

## macOS / Linux

You don't need a script. Run this, then open <http://localhost:18789>:

```bash
ssh -N -L 127.0.0.1:18789:127.0.0.1:18789 user@my-server
```
