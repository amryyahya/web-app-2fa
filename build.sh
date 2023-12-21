IMAGE_NAME="web-app-2fa"
IMAGE_TAG="v1"

GITHUB_USERNAME="amryyahya"

docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

docker images

NEW_IMAGE_NAME="ghcr.io/$GITHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG"
docker tag "$IMAGE_NAME:$IMAGE_TAG" "$NEW_IMAGE_NAME"

echo $GITHUB_PAT | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

docker push "$NEW_IMAGE_NAME"