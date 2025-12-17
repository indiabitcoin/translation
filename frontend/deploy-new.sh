#!/bin/bash

# LibreTranslate Frontend Deployment Script

echo "🚀 Starting LibreTranslate Frontend Build & Deploy..."

# Exit on error
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
npm install

# Build the project
echo -e "${BLUE}🔨 Building for production...${NC}"
npm run build

# Check if build was successful
if [ -d "dist" ]; then
    echo -e "${GREEN}✅ Build completed successfully!${NC}"
    echo -e "${GREEN}📁 Build files are in the 'dist' directory${NC}"
    
    # Optional: Deploy to server
    # Uncomment and configure for your deployment method
    
    # Example: Copy to web server directory
    # echo -e "${BLUE}📤 Deploying to server...${NC}"
    # sudo cp -r dist/* /var/www/html/
    
    # Example: Deploy to S3
    # aws s3 sync dist/ s3://your-bucket-name --delete
    
    # Example: Deploy with rsync
    # rsync -avz --delete dist/ user@server:/path/to/webroot/
    
    echo -e "${GREEN}✨ Deployment complete!${NC}"
else
    echo "❌ Build failed!"
    exit 1
fi
