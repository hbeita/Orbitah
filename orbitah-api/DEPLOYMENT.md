# Orbitah API Deployment Guide - Option A (Same Domain)

## Architecture
- **Frontend**: `https://yourdomain.com`
- **Backend**: `https://yourdomain.com/api`
- **Single domain** with API under `/api` path

## Environment Variables

### Backend (.env)
```bash
ENVIRONMENT=production
FRONTEND_URL=https://yourdomain.com
DATABASE_URL=your_production_database_url
SECRET_KEY=your_secret_key
```

### Frontend (.env.production)
```bash
VITE_API_BASE_URL=https://yourdomain.com/api
```

## Deployment Steps

### 1. Backend Deployment

#### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up production database (PostgreSQL recommended)
# Create .env file with production values
```

#### Production Server Setup
```bash
# Install production server
pip install uvicorn[standard] gunicorn

# Run with Gunicorn (recommended for production)
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or run with Uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Systemd Service (Linux)
Create `/etc/systemd/system/orbitah-api.service`:
```ini
[Unit]
Description=Orbitah API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/orbitah-api
Environment="PATH=/var/www/orbitah-api/.venv/bin"
Environment="ENVIRONMENT=production"
Environment="FRONTEND_URL=https://yourdomain.com"
ExecStart=/var/www/orbitah-api/.venv/bin/gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable orbitah-api
sudo systemctl start orbitah-api
sudo systemctl status orbitah-api
```

### 2. Frontend Deployment

#### Prerequisites
```bash
# Install Node.js dependencies
cd orbitah-frontend
pnpm install
```

#### Build for Production
```bash
# Create production environment file
echo "VITE_API_BASE_URL=https://yourdomain.com/api" > .env.production

# Build the application
pnpm build

# The built files will be in the `dist/` directory
```

#### Deploy to Web Server
```bash
# Copy built files to web server directory
sudo cp -r dist/* /var/www/orbitah-frontend/

# Set proper permissions
sudo chown -R www-data:www-data /var/www/orbitah-frontend
sudo chmod -R 755 /var/www/orbitah-frontend
```

### 3. Nginx Configuration

Create `/etc/nginx/sites-available/orbitah`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Frontend (React app)
    location / {
        root /var/www/orbitah-frontend;
        try_files $uri $uri/ /index.html;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8000/;
        access_log off;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/orbitah /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 5. Database Setup

#### PostgreSQL (Recommended)
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE orbitah;
CREATE USER orbitah_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE orbitah TO orbitah_user;
\q

# Update backend .env
DATABASE_URL=postgresql://orbitah_user:your_secure_password@localhost/orbitah
```

### 6. Firewall Configuration

```bash
# Allow HTTP, HTTPS, and SSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw enable
```

### 7. Monitoring and Logs

#### Backend Logs
```bash
# View API logs
sudo journalctl -u orbitah-api -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### Health Checks
```bash
# Test API health
curl https://yourdomain.com/health

# Test frontend
curl -I https://yourdomain.com
```

## Benefits of Option A
- ✅ **Simpler CORS configuration** (same origin)
- ✅ **Better security** (no cross-domain requests)
- ✅ **Easier SSL management** (single certificate)
- ✅ **Better performance** (no CORS preflight requests)
- ✅ **Simpler deployment** (single domain to manage)

## Security Notes
- All API requests will be same-origin
- No CORS preflight requests needed
- JWT tokens work seamlessly
- Single SSL certificate covers everything
- Regular security updates recommended

## Troubleshooting

### Common Issues
1. **502 Bad Gateway**: Check if backend service is running
2. **404 Not Found**: Verify file paths and permissions
3. **SSL Issues**: Check certificate validity and renewal
4. **Database Connection**: Verify DATABASE_URL and PostgreSQL status

### Useful Commands
```bash
# Restart services
sudo systemctl restart orbitah-api
sudo systemctl restart nginx

# Check service status
sudo systemctl status orbitah-api
sudo systemctl status nginx

# View real-time logs
sudo journalctl -u orbitah-api -f
sudo tail -f /var/log/nginx/error.log
```
