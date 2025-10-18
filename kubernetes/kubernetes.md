- helm and helm charts can be used to deploy a docker container to a kubernetes cluster

```
$ minikube status
minikube
type: Control Plane
host: Stopped
kubelet: Stopped
apiserver: Stopped
kubeconfig: Stopped
```

```
# Install kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create cluster
kind create cluster
```

```
# Start etcd
$ docker run -d --name etcd \
  --net=host \
  k8s.gcr.io/etcd:3.4.13-0 \
  etcd --advertise-client-urls=http://127.0.0.1:2379 \
  --listen-client-urls=http://0.0.0.0:2379

# Start API Server
$ docker run -d --name kube-apiserver \
  --net=host \
  k8s.gcr.io/kube-apiserver:v1.21.0 \
  kube-apiserver \
  --etcd-servers=http://127.0.0.1:2379 \
  --service-cluster-ip-range=10.0.0.0/16 \
  --insecure-bind-address=0.0.0.0 \
  --insecure-port=8080 \
  --disable-admission-plugins=ServiceAccount

# Start Controller Manager
$ docker run -d --name kube-controller-manager \
  --net=host \
  k8s.gcr.io/kube-controller-manager:v1.21.0 \
  kube-controller-manager \
  --master=http://127.0.0.1:8080

# Start Scheduler
$ docker run -d --name kube-scheduler \
  --net=host \
  k8s.gcr.io/kube-scheduler:v1.21.0 \
  kube-scheduler \
  --master=http://127.0.0.1:8080

# Configure kubectl
$ export KUBECONFIG=/workspaces/knowledge-sharing/kubernetes/config.yaml
$ kubectl cluster-info
```
