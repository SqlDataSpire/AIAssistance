@rem Copy this file to openclaw_gui.config.cmd (same folder) and edit the values.
@rem openclaw_gui.config.cmd is git-ignored, so your host details stay private.

@rem Required: the machine running the OpenClaw gateway.
set "OPENCLAW_HOST=your-server.example.com"

@rem SSH login. Leave blank to use your ~/.ssh/config or Windows user name.
set "OPENCLAW_USER=your-ssh-user"

@rem Optional settings (defaults shown).
set "OPENCLAW_SSH_PORT=22"
set "OPENCLAW_REMOTE_PORT=18789"
set "OPENCLAW_LOCAL_PORT=18789"

@rem Optional: private key for passwordless login.
@rem set "OPENCLAW_SSH_KEY=%USERPROFILE%\.ssh\id_ed25519"

@rem Optional: a specific Chromium browser (Chrome or Edge are found automatically).
@rem set "OPENCLAW_BROWSER=C:\Path\To\chrome.exe"

@rem Optional: keep the app window's browser profile between runs so the
@rem Control UI stays signed in. By default a temporary profile is deleted on exit.
@rem set "OPENCLAW_KEEP_PROFILE=1"
