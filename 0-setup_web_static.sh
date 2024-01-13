#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Check if nginx is installed
if ! command -v nginx &> /dev/null
then
	# Update package lists
	sudo apt-get -y update
	# Install nginx
	sudo apt-get install -y nginx
	# start nginx
	sudo service nginx start
else
	pass
fi

# Create directories if not exists
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "
<html>
	<head>
		<title>FACTS</title>
	</head>
	<body>
  		<h1>Why do programmers prefer dark mode?</h1>
		<h2>Because light attracts bugs!</h2>
		<hr>
		Made by ♥ (ˆ⌣ˆ)
	</body>
</html>
" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link linked to /test/ folder
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '39 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default

# Restart nginx
sudo service nginx restart
