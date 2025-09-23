Atividade de Clusterização: Aplicativo Flask com Kubernetes e Minikube

Este projeto é um exemplo de aplicativo Flask que será usado para praticar implantação em Kubernetes com acesso externo via Ingress Controller.

---

1. Executando localmente

Para testar o aplicativo sem Docker ou Kubernetes:

cd webapp/
pip install -r requirements.txt
flask run

Em outro terminal, teste com:

curl localhost:5000

---

2. Executando com Docker

Você pode usar a imagem pronta albertoal/flask_webapp ou construir sua própria imagem:

# Na raiz do projeto
docker build -t myflask_app .
docker run -it --rm -p 5000:5000 myflask_app

Teste o acesso:

curl localhost:5000

---

3. Executando no Minikube

Para simular um cluster Kubernetes local:

1. Inicie o Minikube:

minikube start

2. Habilite o addon de Ingress (para acesso externo):

minikube addons enable ingress

3. Aplique o manifesto Kubernetes:

kubectl apply -f kubernetes.yaml

4. Descubra o IP do Minikube:

minikube ip
# Exemplo: 192.168.20.100

5. Teste o acesso via Ingress:

curl 192.168.20.100/ready

Dica: Se estiver usando outro cluster Kubernetes, consulte os Ingress Controllers disponíveis: 
https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers

---

4. Proxy Envoy (Opcional)

Existe uma versão com Envoy Proxy como sidecar para testes:

- Manifesto disponível em envoy/envoy.yaml.
- Observação: não é um Ingress Gateway, apenas um sidecar para aprendizado de proxy.

