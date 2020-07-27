# spatialjupyter
Jupyterhub for spatial database and analyses

This repository is the place for "sharing the practical guide" to deploy spatial programming using jupyter notebook and other IDE. 
in addition as prerequisite installation of jupyter notebook into zero to jupyterhub to kubernetes using microk8s also included in this readme.

If you cannot install jupyterhub, you can also directly using jupyter notebooks (using docker run), and it is built for spatial purpose based on my docker jupyter custom image hub, i hope you could also add another packages that neccessary, and add the function model to the particular tools. I hope this is become one of the place for sharing the script together to build the cool stuff.

This repository most will be something like practically script for special purposes, such as spatial analyses, and data mining.
Incorporating other tools will be nice for this repository project.

# First start that we need to do is to install docker.
(I get this commands from geonode documentation https://docs.geonode.org/en/master/install/basic/index.html)
- Requirement: Using Linux 18.04+

# Docker installation with docker compose
ubuntu terminal:
  sudo add-apt-repository universe
  sudo apt-get update -y
  sudo apt-get install -y git-core git-buildpackage debhelper devscripts
  sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose
  sudo apt autoremove --purge

  sudo usermod -aG docker ${USER}
  su ${USER}

# After that you could pull the customized images, and run.
docker pull muhfirdausiqbal/jupyter:v2

# Example running for jupyter container from image assuming that you have directory in your linux server /home/my_notebooks 
docker run -d --restart always -p 8888:8888 -v /home/my_notebooks:home/jovyan/my_notebooks/ --name JupyterArcGIS muhfirdausiqbal/jupyter:v2

# for installation microk8s and zero to jupyterhub check this link
https://github.com/IqbalF69/spatialjupyter/blob/master/install_microk8s.md
