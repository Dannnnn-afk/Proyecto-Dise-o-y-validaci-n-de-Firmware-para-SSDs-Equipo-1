# Team Deploy Key Setup

## Deploy Key Information
- **Name**: Team Deploy Key - NVMe Tester
- **SHA256 Fingerprint**: `[WILL_BE_GENERATED_WHEN_YOU_CREATE_THE_KEY]`
- **Public Key**: `[WILL_BE_GENERATED_WHEN_YOU_CREATE_THE_KEY]`

> **Note**: The actual fingerprint and public key will be generated when you run the setup script.

## Setup Instructions

### 1. Save the Deploy Key
```bash
# Create the deploy key file (you'll need to paste the private key content)
nano ~/.ssh/team_deploy_key

# Set correct permissions
chmod 600 ~/.ssh/team_deploy_key
```

### 2. Test the Connection
```bash
# Test with the team deploy key configuration
ssh -T team-deploy

# Or test with the alternative hostname
ssh -T team-github
```

### 3. Usage Examples

#### Clone using deploy key
```bash
# Use the custom host alias for team deploy key
git clone team-deploy:Dannnnn-afk/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1.git

# Or with the alternative hostname
git clone team-github:Dannnnn-afk/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1.git
```

#### Set remote origin with deploy key
```bash
# Change existing remote to use deploy key
git remote set-url origin team-deploy:Dannnnn-afk/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1.git

# Or add as new remote
git remote add team-origin team-deploy:Dannnnn-afk/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1.git
```

#### Push/Pull with deploy key
```bash
# Push to team remote
git push team-origin main

# Pull from team remote
git pull team-origin main
```

## SSH Config Added

The following configuration has been added to your SSH config:

```ssh
# Team Deploy Key configuration
# SHA256:i6Z1b0k1NSiJZch1uTQq5NN4buLLgrBzAWu3M2BgOaY
Host team-deploy
    HostName github.com
    User git
    IdentityFile ~/.ssh/team_deploy_key
    PreferredAuthentications publickey
    StrictHostKeyChecking yes

# Alternative configuration for team deploy key with custom hostname
Host team-github
    HostName github.com
    User git
    IdentityFile ~/.ssh/team_deploy_key
    PreferredAuthentications publickey
```

## Security Notes

1. **Deploy keys** are read-only by default and tied to a specific repository
2. Make sure the deploy key file has **600 permissions** (owner read/write only)
3. The deploy key should be stored securely and not shared
4. Test the connection before using it in production

## Troubleshooting

### If connection fails:
```bash
# Debug SSH connection
ssh -vT team-deploy

# Check key fingerprint
ssh-keygen -lf ~/.ssh/team_deploy_key

# Verify the fingerprint matches: [YOUR_GENERATED_FINGERPRINT]
```

### Common issues:
- Wrong file permissions on the key file
- Key not added to the repository's deploy keys
- Incorrect hostname or user in SSH config
- Private key file not found or corrupted
