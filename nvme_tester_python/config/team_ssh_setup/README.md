# Team SSH Setup Package - NVMe Tester Project

## Quick Setup for Team Members

1. Run the installation script:
```bash
./install_team_key.sh
```

2. Configure git remote:
```bash
git remote set-url origin team-deploy:Dannnnn-afk/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1.git
```

3. Test the setup:
```bash
git pull
git push
```

## Files included:
- `team_key` - Team Deploy Key private key (keep secure)
- `team_key.pub` - Team Deploy Key public key
- `ssh_config` - SSH configuration
- `install_team_key.sh` - Installation script

## Team Deploy Key Info:
- **Name**: Team Deploy Key - NVMe Tester
- **Fingerprint**: SHA256:PqbqxUCl0Ut3vMQqerd7zk5ftL0NZT+i7S5bL55CcMg
- **Status**: Already configured in GitHub with write access

## Security Note:
This is the official team deploy key. Keep it secure and don't share outside the team.
