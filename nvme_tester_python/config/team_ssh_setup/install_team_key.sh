#!/bin/bash
echo "🔧 Installing Team Deploy Key..."

# Create SSH directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Copy team key
cp team_key ~/.ssh/team_deploy_key
cp team_key.pub ~/.ssh/team_deploy_key.pub
chmod 600 ~/.ssh/team_deploy_key
chmod 644 ~/.ssh/team_deploy_key.pub

# Update SSH config
if [ -f ~/.ssh/config ]; then
    cp ~/.ssh/config ~/.ssh/config.backup.$(date +%Y%m%d_%H%M%S)
    echo "📋 SSH config backed up"
fi

# Add team config to SSH config
cat ssh_config >> ~/.ssh/config
chmod 600 ~/.ssh/config

echo "✅ Team key installed successfully!"
echo ""
echo "🧪 Testing connection..."
if ssh -T team-deploy 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ SSH connection working!"
else
    echo "⚠️  SSH test failed. Make sure the deploy key is added to GitHub."
fi

echo ""
echo "🔄 Configure your git remote:"
echo "git remote set-url origin team-deploy:Dannnnn-afk/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1.git"
echo ""
echo "📝 Test git operations:"
echo "git pull"
echo "git push"
