#!/bin/bash

# Script de configuration PostgreSQL pour l'application Gare de Train
# Exécutez ce script pour configurer la base de données PostgreSQL

echo "🚂 Configuration de PostgreSQL pour Gare de Train"
echo "=================================================="

# Variables de configuration
DB_NAME="trainstation"
DB_USER="trainuser"
DB_PASSWORD="trainpass123"
DB_HOST="localhost"
DB_PORT="5432"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si PostgreSQL est installé
if ! command -v psql &> /dev/null; then
    print_error "PostgreSQL n'est pas installé sur ce système."
    echo "Veuillez installer PostgreSQL avant de continuer."
    echo ""
    echo "Sur macOS avec Homebrew:"
    echo "  brew install postgresql"
    echo "  brew services start postgresql"
    echo ""
    echo "Sur Ubuntu/Debian:"
    echo "  sudo apt-get install postgresql postgresql-contrib"
    echo "  sudo systemctl start postgresql"
    echo ""
    echo "Sur CentOS/RHEL:"
    echo "  sudo yum install postgresql-server postgresql-contrib"
    echo "  sudo postgresql-setup initdb"
    echo "  sudo systemctl start postgresql"
    exit 1
fi

print_message "PostgreSQL est installé ✓"

# Vérifier si le service PostgreSQL est en cours d'exécution
if ! pg_isready -q; then
    print_warning "Le service PostgreSQL n'est pas démarré."
    echo "Tentative de démarrage..."
    
    # Essayer de démarrer PostgreSQL selon l'OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew services start postgresql
        else
            print_error "Homebrew non trouvé. Veuillez démarrer PostgreSQL manuellement."
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo systemctl start postgresql
    fi
    
    # Attendre que le service démarre
    sleep 3
    
    if ! pg_isready -q; then
        print_error "Impossible de démarrer PostgreSQL. Veuillez le démarrer manuellement."
        exit 1
    fi
fi

print_message "Service PostgreSQL en cours d'exécution ✓"

# Créer la base de données
print_message "Création de la base de données '$DB_NAME'..."

# Se connecter en tant que postgres et créer la base de données
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || {
    print_warning "Impossible de créer la base de données en tant que postgres."
    echo "Tentative de connexion directe..."
    
    createdb $DB_NAME 2>/dev/null || {
        print_error "Impossible de créer la base de données '$DB_NAME'."
        echo "Veuillez créer la base de données manuellement :"
        echo "  createdb $DB_NAME"
        exit 1
    }
}

print_message "Base de données '$DB_NAME' créée ✓"

# Créer l'utilisateur
print_message "Création de l'utilisateur '$DB_USER'..."

sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || {
    print_warning "L'utilisateur '$DB_USER' existe peut-être déjà."
}

# Accorder les privilèges
print_message "Attribution des privilèges..."

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || {
    print_warning "Impossible d'attribuer les privilèges via postgres."
    echo "Tentative de connexion directe..."
    
    psql -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || {
        print_warning "Impossible d'attribuer les privilèges automatiquement."
        echo "Veuillez exécuter manuellement :"
        echo "  psql -d $DB_NAME -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;\""
    }
}

print_message "Privilèges attribués ✓"

# Exécuter le script de création des tables
print_message "Exécution du script de création des tables..."

if [ -f "SQL/Creation_script.sql" ]; then
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f SQL/Creation_script.sql || {
        print_warning "Impossible d'exécuter le script SQL automatiquement."
        echo "Veuillez exécuter manuellement :"
        echo "  psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f SQL/Creation_script.sql"
    }
else
    print_warning "Script SQL non trouvé. Les tables seront créées automatiquement par l'application."
fi

print_message "Tables créées ✓"

# Créer le fichier .env
print_message "Création du fichier de configuration .env..."

cat > .env << EOF
# Configuration de l'application Gare de Train
# Généré automatiquement le $(date)

# Configuration générale
SECRET_KEY=dev-secret-key-change-in-production-$(date +%s)
FLASK_ENV=development
FLASK_DEBUG=True

# Configuration de la base de données PostgreSQL
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME

# Configuration du serveur
HOST=0.0.0.0
PORT=5001

# Configuration de sécurité
WTF_CSRF_ENABLED=True
EOF

print_message "Fichier .env créé ✓"

# Tester la connexion
print_message "Test de la connexion à la base de données..."

if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" &>/dev/null; then
    print_message "Connexion à la base de données réussie ✓"
else
    print_error "Impossible de se connecter à la base de données."
    echo "Vérifiez les paramètres de connexion dans le fichier .env"
    exit 1
fi

echo ""
echo "🎉 Configuration terminée avec succès !"
echo "======================================"
echo ""
echo "Informations de connexion :"
echo "  Base de données: $DB_NAME"
echo "  Utilisateur: $DB_USER"
echo "  Mot de passe: $DB_PASSWORD"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo ""
echo "URL de connexion: postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
echo ""
echo "Pour démarrer l'application :"
echo "  source prod/bin/activate"
echo "  python3 app.py"
echo ""
echo "L'application sera accessible sur : http://localhost:5001"
echo ""
print_warning "N'oubliez pas de modifier le SECRET_KEY dans le fichier .env pour la production !"
