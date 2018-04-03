# for DNS cache cleanup:
sudo apt-get install nscd

# Install Jenkins:
wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins

# Install Allure:
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Install chrome stable:
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install google-chrome-stable

# The following combination works fine:
# Google chrome Google Chrome 65.0.3325.181
# ChromeDriver 2.36.540471 (9c759b81a907e70363c6312294d30b6ccccc2752)


