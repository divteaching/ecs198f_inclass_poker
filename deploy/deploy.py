#Step 1: Build our Image (Local)

#Step 2: Push our Image to the registry (Remote)

#Step 3: We need to update our kubernetes cluster to use the new image

import subprocess

def build_and_push_image():
    #FIXME: Use REST API Instead
    command = "docker buildx build --platform linux/arm64,linux/amd64 --tag divyanshteaching/poker_deploy:latest --push ."

    result = subprocess.run(command.split(" "), capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)

def upgrade_k8_cluster():
    command = "kubectl rollout restart deployment/poker-deploy"
    
    result = subprocess.run(command.split(" "), capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)

build_and_push_image()
upgrade_k8_cluster()