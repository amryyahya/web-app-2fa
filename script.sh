docker rmi -f web-app-2fa:latest
docker build -t web-app-2fa .
docker rm -f web-app-2fa
docker run -p 3000:3000 --name web-app-2fa web-app-2fa