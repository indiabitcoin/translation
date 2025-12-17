#!/bin/bash
# Deployment script for frontend
# Usage: ./deploy.sh [nginx|apache|node]

set -e

DEPLOY_TYPE=${1:-nginx}
FRONTEND_DIR=$(dirname "$0")
DEPLOY_PATH="/var/www/translate.shravani.group"

echo "🚀 Deploying LibreTranslate Frontend"
echo "Deployment type: $DEPLOY_TYPE"
echo "Frontend directory: $FRONTEND_DIR"
echo "Deploy path: $DEPLOY_PATH"
echo ""

# Check if running as root for system paths
if [ "$DEPLOY_TYPE" != "node" ] && [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Warning: This script may need root privileges for system paths"
fi

case $DEPLOY_TYPE in
    nginx)
        echo "📦 Deploying to Nginx..."
        
        # Create directory
        sudo mkdir -p "$DEPLOY_PATH"
        
        # Copy files
        sudo cp -r "$FRONTEND_DIR"/* "$DEPLOY_PATH/"
        
        # Set permissions
        sudo chown -R www-data:www-data "$DEPLOY_PATH"
        sudo chmod -R 755 "$DEPLOY_PATH"
        
        # Copy nginx config if it exists
        if [ -f "$FRONTEND_DIR/nginx.conf.example" ]; then
            echo "📝 Nginx config example available at: $FRONTEND_DIR/nginx.conf.example"
            echo "   Copy it to: /etc/nginx/sites-available/translate.shravani.group"
            echo "   Then enable: sudo ln -s /etc/nginx/sites-available/translate.shravani.group /etc/nginx/sites-enabled/"
            echo "   Reload: sudo nginx -t && sudo systemctl reload nginx"
        fi
        
        echo "✅ Frontend deployed to $DEPLOY_PATH"
        ;;
        
    apache)
        echo "📦 Deploying to Apache..."
        
        # Create directory
        sudo mkdir -p "$DEPLOY_PATH"
        
        # Copy files
        sudo cp -r "$FRONTEND_DIR"/* "$DEPLOY_PATH/"
        
        # Set permissions
        sudo chown -R www-data:www-data "$DEPLOY_PATH"
        sudo chmod -R 755 "$DEPLOY_PATH"
        
        # Copy apache config if it exists
        if [ -f "$FRONTEND_DIR/apache.conf.example" ]; then
            echo "📝 Apache config example available at: $FRONTEND_DIR/apache.conf.example"
            echo "   Copy it to: /etc/apache2/sites-available/translate.shravani.group.conf"
            echo "   Then enable: sudo a2ensite translate.shravani.group.conf"
            echo "   Reload: sudo systemctl reload apache2"
        fi
        
        echo "✅ Frontend deployed to $DEPLOY_PATH"
        ;;
        
    node)
        echo "📦 Setting up Node.js server..."
        
        # Check if package.json exists
        if [ ! -f "$FRONTEND_DIR/package.json" ]; then
            echo "❌ package.json not found. Creating it..."
            # This would need the package.json content
        fi
        
        # Install dependencies
        if [ -f "$FRONTEND_DIR/package.json" ]; then
            cd "$FRONTEND_DIR"
            npm install
            echo "✅ Dependencies installed"
            echo "   Start server: npm start"
            echo "   Or with PM2: pm2 start server.js --name translate-frontend"
        fi
        ;;
        
    *)
        echo "❌ Unknown deployment type: $DEPLOY_TYPE"
        echo "Usage: ./deploy.sh [nginx|apache|node]"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Configure your web server (if using nginx/apache)"
echo "2. Set up SSL certificate (Let's Encrypt)"
echo "3. Update DNS to point translate.shravani.group to this server"
echo "4. Test: https://translate.shravani.group/"

