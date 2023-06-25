# Botnet Detection in IoT Networks Using ML and DL

### Overview:
Botnets are one of the most prominent threats to system and IoT security in the recent age
of cloud-enabled pervasive computing. Due to the large increase in interconnected devices
and system platforms. A botnet is a network of malware-infected hosts, which are typically
controlled by a Command and Control (C&C) server also known as a botmaster which can
be either centralized or decentralized.\
The concept of Domain Generation Algorithm (DGA) botnets refers to the botnets deployed
under the client-server architecture. The bots act as the client. After infecting the victim’s
computer, it will connect to the C&C server to receive commands. They usually look up the
IP address of the C&C server through a DNS query. According to an automatic domain name
generation algorithm, these domain names are constantly being changed to bypass security
systems.
Thus our task will involve developing and deploying several models for detecting botnets
based on domain generation algorithms (DGAs). These models will be applied into a realistic
IoT simulation network from where the flow data will be obtained.

This project involved three main phases: 

-  ## Phase 1:
  Understanding Botnets: botnet structures, classification, detection methods, objectives, and specific attacks.
-  ## Phase 2:
  Given that our project focused on machine learning and deep learning for DGA detection, we extensively experimented with a range of models, 
  employing eight different variations, in order to detect Domain Generation Algorithms (DGAs) 
-  ## Phase 3:
   Real-World Simulation on an IoT Network
A crucial aspect of our project involved simulating a real IoT network that incorporated botnets.
After obtaining the hardware resources needed to build a small model iot network .Our IoT network architecture comprised several key components.
The Raspberry Pi cards played a crucial role,simulating various activities including benign, malicious, and hybrid behaviors.
The switch facilitated the mirroring of flow from the Raspberry Pi cards to the port mirror.
An additional Raspberry Pi card was dedicated to capturing and filtering the flow from the switch mirror port specifically for DNS packets (Capturing and filtering server).
The main PC was responsible for receiving the domain names from the Filtering server,conducting classification, and displaying the results through a web interface.
Finally, the router, (another PC) served as the gateway for the DNS packets .

![Inkedwhole](https://github.com/1b71h3l/2CS-Project/assets/74022204/c51109c3-8914-4843-9dab-b614acb2c2a5)

After the classification of the domain names using the AI model,In the event of the presence of a botnet, 
the administrator will be informed and a list of all the domain names that have appeared in a dns request will be displayed with their calssification and source IP.

<img width="443" alt="Capture d'écran 2023-06-25 201438" src="https://github.com/1b71h3l/2CS-Project/assets/74022204/a7398701-6374-4167-9e35-17018f3a974c">

<img width="445" alt="Capture d'écran 2023-06-25 201557" src="https://github.com/1b71h3l/2CS-Project/assets/74022204/a369b7de-9836-45ad-940e-826578cf3259">
