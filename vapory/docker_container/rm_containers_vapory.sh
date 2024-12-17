#!/bin/bash
# Arguments du script
POVRAY_INPUT_FILE=$1
POVRAY_RESOURCES=$2
POVRAY_WIDTH=$3
POVRAY_HEIGHT=$4
POVRAY_EXTRA_PARAMS=$5

# Vérifiez si les arguments sont fournis
if [[ -z "$POVRAY_INPUT_FILE" || -z "$POVRAY_RESOURCES" || -z "$POVRAY_WIDTH" || -z "$POVRAY_HEIGHT" || -z "$POVRAY_EXTRA_PARAMS" ]]; then
  echo "Usage: $0 <input_file> <resources> <width> <height> <extra_params>"
  exit 1
fi

# Exporter les variables pour docker-compose
export POVRAY_INPUT_FILE
export POVRAY_RESOURCES
export POVRAY_WIDTH
export POVRAY_HEIGHT
export POVRAY_EXTRA_PARAMS

# Lancer docker-compose
docker-compose down -v --remove-orphans
