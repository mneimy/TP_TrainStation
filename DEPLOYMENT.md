# 🚀 Guide de Déploiement - Gare de Train

## Vue d'ensemble

Ce guide vous accompagne dans le déploiement de l'application Gare de Train en environnement de production.

## Prérequis

### Serveur de Production
- **OS** : Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **RAM** : Minimum 2GB, recommandé 4GB+
- **CPU** : 2 cœurs minimum
- **Stockage** : 20GB minimum
- **Python** : 3.8+
- **PostgreSQL** : 12+

### Outils Nécessaires
- `git` - Gestion de version
- `nginx` - Serveur web
- `gunicorn` - Serveur WSGI
- `supervisor` - Gestion des processus
- `certbot` - Certificats SSL

## Installation

### 1. Préparation du Serveur

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances système
sudo apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib

# Installation de Gunicorn
pip3 install gunicorn
```

### 2. Configuration de PostgreSQL

```bash
# Démarrer PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Créer la base de données
sudo -u postgres psql -c "CREATE DATABASE trainstation;"
sudo -u postgres psql -c "CREATE USER trainuser WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE trainstation TO trainuser;"
```

### 3. Déploiement de l'Application

```bash
# Cloner le repository
git clone <your-repo-url> /opt/trainstation
cd /opt/trainstation

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
pip install gunicorn

# Configuration de l'environnement
cp config.env.example .env
nano .env
```

### 4. Configuration du Fichier .env

```bash
# Configuration de production
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False

# Base de données PostgreSQL
DATABASE_URL=postgresql://trainuser:secure_password@localhost:5432/trainstation

# Configuration du serveur
HOST=0.0.0.0
PORT=5001

# Sécurité
WTF_CSRF_ENABLED=True
```

## Configuration de Gunicorn

### 1. Fichier de Configuration Gunicorn

Créez `/opt/trainstation/gunicorn.conf.py` :

```python
# Configuration Gunicorn pour Gare de Train
import multiprocessing

# Nom du fichier d'application
wsgi_module = "app:app"

# Nombre de workers (2 * CPU + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Nombre de threads par worker
threads = 2

# Adresse et port
bind = "127.0.0.1:5001"

# Répertoire de travail
chdir = "/opt/trainstation"

# Utilisateur et groupe
user = "www-data"
group = "www-data"

# Logs
accesslog = "/var/log/trainstation/access.log"
errorlog = "/var/log/trainstation/error.log"
loglevel = "info"

# Processus principal
daemon = False
pidfile = "/var/run/trainstation.pid"

# Redémarrage automatique
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Timeout
timeout = 30
keepalive = 2
```

### 2. Service Systemd

Créez `/etc/systemd/system/trainstation.service` :

```ini
[Unit]
Description=Gare de Train Flask Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/trainstation
Environment=PATH=/opt/trainstation/venv/bin
ExecStart=/opt/trainstation/venv/bin/gunicorn --config gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 3. Activation du Service

```bash
# Créer le répertoire de logs
sudo mkdir -p /var/log/trainstation
sudo chown www-data:www-data /var/log/trainstation

# Recharger systemd
sudo systemctl daemon-reload

# Démarrer le service
sudo systemctl start trainstation
sudo systemctl enable trainstation

# Vérifier le statut
sudo systemctl status trainstation
```

## Configuration de Nginx

### 1. Configuration Nginx

Créez `/etc/nginx/sites-available/trainstation` :

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirection vers HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # Certificats SSL
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Configuration SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Headers de sécurité
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Fichiers statiques
    location /static {
        alias /opt/trainstation/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy vers l'application Flask
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Logs
    access_log /var/log/nginx/trainstation_access.log;
    error_log /var/log/nginx/trainstation_error.log;
}
```

### 2. Activation du Site

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/trainstation /etc/nginx/sites-enabled/

# Tester la configuration
sudo nginx -t

# Recharger Nginx
sudo systemctl reload nginx
```

## Certificats SSL avec Let's Encrypt

### 1. Installation de Certbot

```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

### 2. Obtenir le Certificat

```bash
# Obtenir le certificat
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Vérifier le renouvellement automatique
sudo certbot renew --dry-run
```

## Monitoring et Maintenance

### 1. Logs

```bash
# Logs de l'application
sudo tail -f /var/log/trainstation/error.log
sudo tail -f /var/log/trainstation/access.log

# Logs Nginx
sudo tail -f /var/log/nginx/trainstation_error.log
sudo tail -f /var/log/nginx/trainstation_access.log

# Logs système
sudo journalctl -u trainstation -f
```

### 2. Surveillance

```bash
# Statut des services
sudo systemctl status trainstation
sudo systemctl status nginx
sudo systemctl status postgresql

# Utilisation des ressources
htop
df -h
free -h
```

### 3. Sauvegarde

```bash
# Script de sauvegarde
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/trainstation"

# Créer le répertoire de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarder la base de données
pg_dump -h localhost -U trainuser trainstation > $BACKUP_DIR/db_$DATE.sql

# Sauvegarder les fichiers de l'application
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /opt/trainstation

# Nettoyer les anciennes sauvegardes (garder 30 jours)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## Mise à Jour

### 1. Mise à Jour de l'Application

```bash
# Arrêter le service
sudo systemctl stop trainstation

# Sauvegarder
cp -r /opt/trainstation /opt/trainstation.backup.$(date +%Y%m%d)

# Mettre à jour le code
cd /opt/trainstation
git pull origin main

# Mettre à jour les dépendances
source venv/bin/activate
pip install -r requirements.txt

# Redémarrer le service
sudo systemctl start trainstation
```

### 2. Vérification Post-Déploiement

```bash
# Vérifier que l'application répond
curl -I https://your-domain.com

# Vérifier les logs
sudo journalctl -u trainstation --since "5 minutes ago"
```

## Dépannage

### Problèmes Courants

1. **Service ne démarre pas**
   ```bash
   sudo journalctl -u trainstation -n 50
   ```

2. **Erreur de base de données**
   ```bash
   sudo -u postgres psql -c "SELECT 1;"
   ```

3. **Problème de permissions**
   ```bash
   sudo chown -R www-data:www-data /opt/trainstation
   ```

4. **Port déjà utilisé**
   ```bash
   sudo netstat -tlnp | grep :5001
   ```

## Sécurité

### 1. Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# iptables (CentOS)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### 2. Mise à Jour Système

```bash
# Mise à jour automatique des paquets de sécurité
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades
```

### 3. Surveillance des Intrusions

```bash
# Installation de fail2ban
sudo apt install fail2ban

# Configuration pour l'application
sudo nano /etc/fail2ban/jail.local
```

## Performance

### 1. Optimisation de la Base de Données

```sql
-- Index pour améliorer les performances
CREATE INDEX idx_reservation_user_id ON reservation(id_user);
CREATE INDEX idx_reservation_train_id ON reservation(id_train);
CREATE INDEX idx_train_number ON train(train_number);
```

### 2. Cache Redis (Optionnel)

```bash
# Installation de Redis
sudo apt install redis-server

# Configuration dans l'application
pip install redis flask-caching
```

## Support

Pour toute question ou problème :

1. Vérifiez les logs
2. Consultez la documentation
3. Créez une issue sur GitHub
4. Contactez l'équipe de développement

---

**Note** : Ce guide est fourni à titre informatif. Adaptez-le selon vos besoins spécifiques et votre environnement de production.
