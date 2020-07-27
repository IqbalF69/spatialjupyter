# Create session with su - $USER
su - $USER # enter password for sudo group

# make your life easier
alias kubectl='microk8s kubectl'
alias helm='microk8s helm3'

# start install jupyter helm with create namespace jhub
kubectl create namespace jhub

# Go to this default documentation installation 
https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub/setup-jupyterhub.html

# or you can use my installation method and config.yaml, first helm repo add and update
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

# enable storage first
microk8s.enable storage

# edit a config.yaml using nano, vi, or other editor in current directory
proxy:
   secretToken: "6457f0ff2d6728ded9772e6526640cc671e0de2f562bb71c7aaf880d73d1115a"
   service:
     type: NodePort
     nodePorts:
       http: 30229
       https: 31223
singleuser:
  image:
    name: muhfirdausiqbal/jupyter
    tag: v2
  extra_resource_limits:
    nvidia.com/gpu: 1

  profileList:

    - display_name: "ARCGIS-GEE API-With NVIDIA GPU"
      description: "From ArcGIS Docker API + Google Earth Engine Enhance with NVIDIA GPU"
      default: true

    - display_name: "Spark environment + GEE"
      description: "The Jupyter Stacks spark image! + GEE"
      kubespawner_override:
        image: muhfirdausiqbal/jupyter:v1
        extra_resource_limits:
          nvidia.com/gpu: 1
  memory:
    limit: 4G
                                      
    guarantee: 1024M
  cpu:
    limit: 2
    guarantee: 0.5

  storage:
    dynamic:
      storageClass: microk8s-hostpath
  cloudMetadata:
    enabled: true


prePuller:
  hook:
    enabled: true

scheduling:
  userScheduler:
    enabled: true
  podPriority:
    enabled: true
  userPlaceholder:
    enabled: true
    replicas: 4

cull:
  enabled: true
  timeout: 3600
  every: 300

debug:
  enabled: true

auth:  
  admin:
    users:
      - <your username>
  whitelist:
    users:
      - <your username>

hub:
  cookieSecret: "6457f0ff2d6728ded9772e6526640cc671e0de2f562bb71c7aaf880d73d1115a"
  db:
    type: sqlite-pvc

# execute helm install upgrade with config.yaml with high timeout 1 hour, to ensure docker image pull job, otherwise change the images.
microk8s helm3 upgrade --install jhub jupyterhub/jupyterhub \
  --namespace jhub  \
  --version=0.9.0 \
  --values config.yaml --timeout=60m
 
 
