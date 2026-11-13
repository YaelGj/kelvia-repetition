#!/usr/bin/env bash
# Appelle /billets en boucle et affiche le code HTTP (200 : réponse ; 000 : pas de réponse). Ctrl+C pour arrêter.
# ./charge.sh rush : ouverture des ventes, 20 clients en parallèle pendant 60 s, puis rythme normal.
trap 'kill 0' INT
appeler() { echo "$(date +%T) /billets $(curl -s -o /dev/null -w '%{http_code}' --max-time 2 localhost:8000/billets)"; }
if [ "${1:-}" = rush ]; then
  for i in $(seq 20); do while [ $SECONDS -lt 60 ]; do appeler; done & done
  wait
fi
while true; do appeler; sleep 0.2; done
