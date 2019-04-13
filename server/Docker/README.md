# Build image with Dockerfile, -t provides the image name, . indicates Dockerfile path
docker build -t connectfour:latest .

# Verify image creation with 
docker images

#Added virtual volume for saved file from games (pickled data)
sudo docker volume create saves

#list all volume
sudo docker volume ls

#inspect a volume
#if saves files exist --> need to be put in the saves volume directory
sudo docker volume inspect saves

#remove unused volume
sudo docker volume prune

#test launch with volume
sudo docker run -v saves:/home/lucblender/ConnectFour/server/saves -it image:version

# Start container from image, --name provides the name, -d : run it in background, -p maps ports	
# --rm will delete the container once it is terminated, last argument is the image name
docker run -v saves:/home/lucblender/ConnectFour/server/saves --name connectfour -d -p 5002:5002 --rm connectfour:latest

# Verify the containers that are running with "docker ps" or "docker ps -a" to see all of them
