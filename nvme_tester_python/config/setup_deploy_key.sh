#!/bin/bash

# SSH Deploy Key Setup Script for NVMe Tester Project
# This script safely generates and configures SSH deploy keys

set -e  # Exit on any error

echo "🔐 SSH Deploy Key Setup for NVMe Tester Project"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if SSH directory exists
if [ ! -d "$HOME/.ssh" ]; then
    echo "Creating SSH directory..."
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    print_status "SSH directory created"
fi

# Create sockets directory
mkdir -p "$HOME/.ssh/sockets"
chmod 700 "$HOME/.ssh/sockets"

# Generate deploy key
KEY_PATH="$HOME/.ssh/team_deploy_key"
if [ -f "$KEY_PATH" ]; then
    print_warning "Deploy key already exists at $KEY_PATH"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing key..."
    else
        rm "$KEY_PATH" "$KEY_PATH.pub" 2>/dev/null || true
    fi
fi

if [ ! -f "$KEY_PATH" ]; then
    echo "Generating new deploy key..."
    ssh-keygen -t ed25519 -C "team-deploy-key@nvme-tester" -f "$KEY_PATH" -N ""
    print_status "Deploy key generated"
    
    # Show the public key
    echo ""
    echo "📋 Your PUBLIC key (add this to GitHub as Deploy Key):"
    echo "======================================================"
    cat "$KEY_PATH.pub"
    echo "======================================================"
    
    # Show fingerprint
    echo ""
    echo "🔍 Key fingerprint:"
    ssh-keygen -lf "$KEY_PATH.pub"
    echo ""
fi

# Copy SSH config template
CONFIG_SOURCE="./nvme_tester_python/config/ssh_config"
if [ -f "$CONFIG_SOURCE" ]; then
    print_warning "This will update your SSH config. Current config will be backed up."
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Backup existing config
        if [ -f "$HOME/.ssh/config" ]; then
            cp "$HOME/.ssh/config" "$HOME/.ssh/config.backup.$(date +%Y%m%d_%H%M%S)"
            print_status "SSH config backed up"
        fi
        
        # Copy new config
        cp "$CONFIG_SOURCE" "$HOME/.ssh/config"
        chmod 600 "$HOME/.ssh/config"
        print_status "SSH config updated"
    fi
else
    print_error "SSH config template not found at $CONFIG_SOURCE"
fi

# Test connection
echo ""
echo "🧪 Testing SSH connection to GitHub..."
if ssh -T team-deploy 2>&1 | grep -q "successfully authenticated"; then
    print_status "SSH connection to GitHub working!"
else
    print_warning "SSH connection test failed. Make sure to:"
    echo "   1. Add the public key above to GitHub as a Deploy Key"
    echo "   2. Enable write access if you need to push"
    echo "   3. Run: ssh -T team-deploy"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Copy the public key above"
echo "   2. Go to GitHub.com → Your repo → Settings → Deploy keys"
echo "   3. Click 'Add deploy key'"
echo "   4. Paste the public key"
echo "   5. Enable 'Allow write access' if needed"
echo "   6. Test with: ssh -T team-deploy"
echo ""
echo "🔄 To use SSH instead of HTTPS for git:"
echo "   git remote set-url origin team-deploy:Dannnnn-afk/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1.git"
