#!/bin/bash

UPSTREAM="upstream"
BRANCH="master"
REPO_ORIGINAL="https://github.com/luisvcsilva/clusterizacao_servidores_2025.git"


if ! git remote | grep -q "$UPSTREAM"; then
  #Adicionando o remote do repositório original...
  git remote add $UPSTREAM $REPO_ORIGINAL
else
  echo "Remote 'upstream' já configurado."
fi


# Buscando atualizações do repositório original...
git fetch $UPSTREAM


# merge das mudanças da branch '$BRANCH' do repositório original...
git merge $UPSTREAM/$BRANCH


# Se aparecerem conflitos, edite os arquivos conflitantes e depois:
# git add .
# git commit
