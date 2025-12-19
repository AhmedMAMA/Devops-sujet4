# Cat-Dog Classification Service - Kubernetes / Flask / ML

## Description

Ce projet déploie un **modèle de machine learning** capable de **classer une image en chat ou chien**.  
Le service tourne dans **des pods Kubernetes**, accessibles via un **service LoadBalancer**, et est entièrement conteneurisé avec Docker.

- **Niveau 1** : un seul pod avec le modèle  
- **Niveau 2** : plusieurs pods avec un Load Balancer (répartition de charge)  
- **Niveau 3** : modèle deep learning pour classification d’images  

L’ensemble du projet peut être testé **localement avec Minikube**.

---

## Technologies utilisées

- Python 3.10  
- Flask (REST API pour le modèle)  
- Docker (conteneurisation)  
- Kubernetes / Minikube (orchestration et pods)  
- TensorFlow / Ultralytics (modèle ML)  
- Pillow / NumPy (prétraitement d’images)  

---

## Structure du projet
```python
project/
│
├─ Dockerfile # Construction de l’image Flask + ML
├─ deployment.yaml # Déploiement Kubernetes (3 pods)
├─ service.yaml # Service Kubernetes (LoadBalancer)
├─ test.py # Script Flask servant le modèle ML
├─ img/ # Images test (chat/chien)
└─ README.md
```


---

## Prérequis

- Docker installé et fonctionnel  
- Minikube installé et opérationnel  
- Kubectl configuré pour Minikube  

---

## Installation et déploiement local

### 1️⃣ Construire l’image Docker

```bash
docker build -t docker_cat-dog-api:latest .
```

# 2️⃣ Démarrer Minikube
```bash
minikube start --driver=docker
```

# 3️⃣ Charger l’image dans Minikube

```bash
minikube image load docker_cat-dog-api:latest
```

# 4️⃣ Déployer les pods et le service
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

# 5️⃣ Vérifier les pods
```bash
kubectl get pods
```

**Tu devrais voir :**
```sql
READY   STATUS
1/1     Running
1/1     Running
1/1     Running
```
6️⃣ Accéder au service via Minikube
```bash
minikube service cat-dog-service --url
```

Puis tester l’API :
```bash
curl -X POST -F "file=@img/cat.jpg" http://<minikube-url>/predict
```

**Réponse attendue :**
```json
{"prediction":"Cat","confidence":0.98}
```

## Endpoints disponibles
* /predict : POST avec une image pour obtenir la prédiction
* /whoami (optionnel) : GET pour vérifier quel pod a répondu (test du load balancing)
* /health (optionnel) : GET pour vérifier que le pod est prêt

## Nettoyage / Repartir de zéro
Supprimer tout le cluster et pods :
```bash
kubectl delete deployment --all
kubectl delete service --all
kubectl delete pod --all
minikube delete
docker rmi -f docker_cat-dog-api:latest
docker system prune -a
```

## Difficulté : 
Déploiement des load balanceur pour la gestion de la scalabilité des requêtes en direction de web service.

## Projet réalisé pour le Learning XP : Module DevOps