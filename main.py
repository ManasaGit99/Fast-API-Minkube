from fastapi import FastAPI, HTTPException
from kubernetes import client, config
import requests

app = FastAPI()

# Load Kubernetes configuration
config.load_kube_config()

# Kubernetes API client
k8s_client = client.AppsV1Api()

@app.post("/createDeployment/{deployment_name}")
async def create_deployment(deployment_name: str):
    # Define the deployment spec (using nginx as an example)
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector={'matchLabels': {'app': deployment_name}},
            template=client.V1PodTemplateSpec(
                metadata={'labels': {'app': deployment_name}},
                spec=client.V1PodSpec(containers=[
                    client.V1Container(
                        name="nginx",
                        image="nginx:latest",
                        ports=[client.V1ContainerPort(container_port=80)]
                    )
                ])
            )
        )
    )
    
    try:
        k8s_client.create_namespaced_deployment(namespace="default", body=deployment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": f"Deployment {deployment_name} created successfully."}

@app.get("/getPromdetails")
async def get_prom_details():
    # Prometheus query for pod metrics
    response = requests.get("http://prometheus-server/api/v1/query?query=kube_pod_info")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get data from Prometheus")
    
    data = response.json()
    return data
