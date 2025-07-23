#!/bin/bash

cd "$(dirname "$0")"

git add .
git status

echo "Digite a mensagem do commit:"
read mensagem

git commit -m "$mensagem"
git pull origin main --rebase
git push origin main

echo "Alterações salvas e enviadas para o GitHub!"