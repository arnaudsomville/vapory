#!/bin/bash
# Arguments du script
POVRAY_INPUT_FILE=$1
POVRAY_RESOURCES=$2
POVRAY_WIDTH=$3
POVRAY_HEIGHT=$4
POVRAY_EXTRA_PARAMS=$5

# Chemin du fichier docker-compose.yml
DOCKER_COMPOSE_FILE="$(dirname "$0")/docker-compose.yml"

# Vérifiez si les arguments sont fournis
if [[ -z "$POVRAY_INPUT_FILE" || -z "$POVRAY_RESOURCES" || -z "$POVRAY_WIDTH" || -z "$POVRAY_HEIGHT" || -z "$POVRAY_EXTRA_PARAMS" ]]; then
  echo "Usage: $0 <input_file> <resources> <width> <height> <extra_params>"
  exit 1
fi

# Vérifiez si le fichier docker-compose.yml existe
if [[ ! -f "$DOCKER_COMPOSE_FILE" ]]; then
  echo "Erreur : Fichier docker-compose.yml introuvable à l'emplacement : $DOCKER_COMPOSE_FILE"
  exit 1
fi

# Exporter les variables pour docker-compose
export POVRAY_INPUT_FILE
export POVRAY_RESOURCES
export POVRAY_WIDTH
export POVRAY_HEIGHT
export POVRAY_EXTRA_PARAMS

# Lancer docker-compose avec le fichier spécifié
docker-compose -f "$DOCKER_COMPOSE_FILE" up
