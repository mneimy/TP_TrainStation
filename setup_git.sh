#!/bin/bash
# Script de configuration pour Git - Gare de Train

echo "🚀 Configuration de l'application pour Git"
echo "=========================================="

# Vérifier si Git est initialisé
if [ ! -d ".git" ]; then
    echo "📁 Initialisation du dépôt Git..."
    git init
fi

# Ajouter tous les fichiers sauf ceux dans .gitignore
echo "📝 Ajout des fichiers au dépôt Git..."
git add .

# Vérifier le statut
echo "📊 Statut du dépôt Git :"
git status

echo ""
echo "✅ Configuration terminée !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Créez un fichier .env avec vos configurations personnelles"
echo "2. Modifiez config.env.example selon vos besoins"
echo "3. Commitez vos changements : git commit -m 'Initial commit'"
echo "4. Ajoutez un remote : git remote add origin <votre-repo-url>"
echo "5. Poussez vers Git : git push -u origin main"
echo ""
echo "⚠️  Important :"
echo "- Le fichier .env ne sera PAS committé (protégé par .gitignore)"
echo "- Utilisez config.env.example comme modèle"
echo "- Toutes les configurations sensibles sont maintenant dans des variables d'environnement"
