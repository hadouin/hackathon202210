Competition task for Hackathon Green Code 7-8/10/22

The scripts in this repository deploy the platform into DS Outscale cloud, initialize and configure the virtual machines, and install the applications.

The goal of this competition is to minimize the power consumption of a system running in the Cloud.

The evaluation script allows testing the platform by running the commands, testing their correctness, and measuring the power consumption.

The platform should not be considered as an example to follow for real production systems. It was created with the maximum simplification of all its aspects. A real platform is much more complicated. But, all this complication is not the subject of this competition. The idea is to let anyone find ways of optimization. People with different profiles can identify and improve something here. It can be architecture, infrastructure, and code optimization. You are free to do whatever you want to reduce consumption. Start with forking the project and use your fork to install the platform and run the tests. Then, depending on your knowledge and preferences you can focus only on some aspects or you can recreate all and rewrite the code in another language. All this is up to you. In the end, you have to give us your GitHub repo with an updated system. We install and test it with the same commands. Make sure that all is automatically deployable and the evaluation tests pass! 

If you think that the task is too difficult for you, do not give up! Think about optimization and prepare your pitch!

## Evaluation critaria
Only the power consumtion is taken into consideration. Performance, security, fault tolerance, best coding practices are NOT the subject of this competition.

Think about:

- The more resources you reserve, the more you consume even if they are not fully utilized.
- Avoid doing the same thing more than once.
- If you're not sure something will be used, don't waste time initializing it earlier.
- Try to take the maximum from the available resources. Think about parallelization.
- Some operations take time, but a significant portion of the time they wait for other tasks to complete and block their resources.
- Check if there are standard language methods or well-established libraries for what you are coding.
- Interpreted code is usually much slower than compiled one. Some interpreted languages allow compilation.
- When processing data, prefer matrix operations and avoid loops.
- Think about traffic minimization (compression, binary and text protocols).
- Process, filter, and aggregate data as close to its source as possible to minimize traffic.
- Revise the segmentation of your system. The more segmented it is, the more resources are wasted.
- Think about idle time and auto-scaling. Your system is consuming even if no operations are taking place.

# Project file structure
```
.
├── README.md - this file
├── app1 - installation of app1 in VM
│   ├── init.sh - script to be run in VM after its creation to install the app1
│   ├── src 
│   │   ├── app1.py - main file with a message loop
│   │   ├── prime_numbers.py 
│   │   └── store_price.py
│   └── vscode - files to run VSCode in container on VM
│       ├── Dockerfile
│       ├── build.sh
│       └── run.sh
├── app1_connect.sh - script to connect to app1 by ssh
├── db1 - installation of database in VM
│   ├── db_init.sql - prefill script
│   ├── docker - compose.yml - run db in containers
│   └── init.sh - script to be run in VM after its creation to install the db
├── db1_connect.sh - script to connect to db1 by ssh
├── env_init_example.sh - example of script to initialize environment varables to connect to the Cloud
├── main.tf - Terraform configuration
├── metrics - folder with evaluation script and command files example
│   ├── README.md - readme for evaluation
│   ├── expected - folder with expected outputs
│   │   ├── prime.txt
│   │   └── store_prices.txt
│   ├── input - folder with commands to run
│   │   ├── prime.json
│   │   └── store_prices.json
│   ├── metrics - empty folder used start.sh
│   ├── output -  empty folder used start.sh
│   ├── process.py - script used by start.sh
│   ├── start.sh - main script to run the evaluation
│   ├── totals -  empty folder used by start.sh
│   └── wait_termination.py - script used by start.sh
├── ms1 - installation of the microservice 1 in VM
│   ├── init.sh - script to be run in VM after its creation to install the ms1
│   ├── src
│   │   └── app.py - ms1 source code
│   └── vscode - files to run VSCode in container on VM
│       ├── Dockerfile
│       ├── build.sh
│       └── run.sh
├── ms1_connect.sh - script to connect to ms1 by ssh
├── platform_create.sh - script to create a platform in DS Outscale cloud
└── platform_destroy.sh - script to destroy a platform
```

# Preconditions
1. GitHub account

You need a GitHub account. Please create it. It's free. You start by forking https://github.com/outscale-dev/hackathon202210 into your account.

Your delivery is a GitHab repository with an updated project.

2. Linux or Mac computer

The scripts in this project are for the bash. If you have a Windows computer you can use a VM running in VirtualBox on your computer or in DS Outscale cloud.

3. Installed Terraform

We use Terraform to deploy the environment into the cloud. Please [install it](https://learn.hashicorp.com/tutorials/terraform/install-cli).


4. Access and Secret keys for DS Outscale cloud account.

Every team has a separate account. Access and secret keys give you an access to it. 

You can work with account using:

- [Terraform](https://www.terraform.io/) - automation tool. 
    - See [OUTSCALE Provider](https://registry.terraform.io/providers/outscale-dev/outscale/latest/docs)
- [Cockpit](https://cockpit.outscale.com/login/) - Web UI. Normally, you don't need to use it, but if you want please use AccessKey as login and SecretKey as password.
- [VS Code plugin osc-viewer](https://marketplace.visualstudio.com/items?itemName=outscale.osc-viewer)

For this competition the only thing you really need is Terraform.

# Platform installation

## Initialize Terraform in the project 

Run it once after project cloning from GitHub in the project folder:
```
terraform init
```
This creates several folders to keep Terraform states. Don't touch them. They are managed by Terraform and excluded from version control.

## Set Access and Secret keys

Rename ```env_init_example.sh``` file into ```env_init.sh``` and set values for OUTSCALE_ACCESSKEYID and OUTSCALE_SECRETKEYID.
```
export OUTSCALE_ACCESSKEYID=...
export OUTSCALE_SECRETKEYID=...
export OUTSCALE_REGION="eu-west-2"
```

## Create a platform
```
./platform_create.sh
```
The script does the following:
1. Create virtual machines, security groups, and other environmental elements in the DS Outscale Cloud. 
2. Create ```~/.ssh/hackathon.rsa``` private key to access this VM by ssh. The same key for all VMs.
3. Create ```<vm>_connect.sh``` files to connect to the VMs.

Be patient. It takes about 20 minutes.

If you work with the platform from different locations share (copy) the private key and connection scripts to all of them.

The next section explayns how to destroy the platform, but if you make some changes such as security group reconfiguration or if you add a new resource you can run this script again without destroing the platform. 

## Destroy platform
If you want to restart your work or test your updated scripts you have first destroy the platform. 
```
./platform_destroy.sh
```
The script destroys ALL its resources in the cloud.
Then you can re-create it again.

**Attention!** If you make any updates in the running platform, such as code update or package installation make sure that you save all this in the project before destroing!

## Connect to VMs by ssh:
When the platform is up, you can connect to machines by SSH. To simplify this the scripts are created in the project root for all VMs.

```
./<vm>_connect.sh
```
Where ```<vm>``` is app1, ms1, db1, ...

These files are re-created by platform_create.sh script on every platform re-creation.

# Working with code

You can use whatever method you want to work with code. 

- Debug all locally and then test in the platform. 
- Debug some part of code locally connecting to componenets in the platform.
- Run VS Code directly on virtual machines and work with it in the browser.
- Connect to VMs from locally installed VS Code remotely.
- ...


# Connect to VMs from VS Code remotely

1. Install [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) plugin in VS Code on your computer.
2. Install openssh-server on a VM:
```
./<vm>_connect.sh
sudo apt-get install openssh-server -y
```
Install it on all virtual machines that you plan to connect to remotely.

4. In your VS Code open command panel (Command+Shift+P on Mac) and select: 

```Remote-SSH: Open SSH Configuration File...```

5. Select the default config (```/Users/<user>/.ssh/config``` on Mac) and add hosts for every VM:
```
Host <vm_ip>
	HostName <vm_ip>
	User outscale
    IdentityFile  ~/.ssh/hackathon.rsa
```

4. Open command panel (Command+Shift+P on Mac) and select: 

```Remote-SSH: Connect to Host...```

5. Enter VM's ip. 

You can see and modify any files on this VM as if VS Code is running on this VM. 


# Running VS Code on a virtual machine

You can also run VS Code as a Web application directly on VMs and work with it via any browser.

It is not running automatically to avoid unnecessary resource consumption.
You can run it manually in a docker container. 

Example of its configuration is in ```<application>/vscode``` folder:
    - Dockerfile - install all needed tools here
    - build.sh - Image compilation script
    - run.sh - Run container with VSCode.

To run VSCode in a VM:
1. Connect by SSH: ```./<app>_connect.sh```
2. Unzip files with vscode: ```unzip vscode.zip```
3. Build the image (it may take up to 20 minutes):
```
cd <app>/vscode # example: cd app1/vscode
bash ./build.sh 
```
4. Run container with VSCode: ```bash ./run.sh```
5. Open VSCode in your browser: ```http://<vm_ip>:3000```, where ```<vm_ip>``` can be found in ```<app>_connect.sh``` script.

If you run your application on this VM in another container make sure that your code is mapped to the service as a local volume pointed to the same local folder.
By default, this is ```/data/code```, but you can change it in ```run.sh``` script.

# Components

## Application 1
Python application which is running as a service.

- To stop: ```sudo systemctl stop app1.service```
- To start: ```sudo systemctl start app1.service```
- To restart: ```sudo systemctl restart app1.service```
- To see service log: ```journalctl -u app1.service```

**Attention:** If you update the code in place into the VM don't forget to restart the service.

The application watches for new files in VM's local ```/data/input``` folder, processes them, and outputs the result in ```/data/output```.

The file names must be unique otherwise the result of previous files with the same name will be rewritten by the more recent one.

Example of input file:
```
{
    "1": {
	    "type": "typeA",
	    "arguments": {
            "arg1": "Hello",
		    "arg2": "world"
        }
	},
    "2": {
	    "type": "typeB",
	    "arguments": {"arg1": "Filled !"}
    },
    "3": {
	    "type": "typeA",
	    "arguments": {
            "arg1": "Beautiful",
		    "arg2": "sunny",
            "arg3": "day"
        }
	},
    "4": {
        "type": "typeB",
        "arguments": {}
    }
}
``` 

The numeric first-level keys are task ids. They must be unique within a file.
- "type" is a command type.
- "arguments" can be unique for every command type

Every command is processed by its function in the app1 (see ```/app1/src/app1.py```).

The output for all commands is a string.

The outputs are saved in the output file.

The output file has the same name as the input one, but with .txt extension. Ex: a234.json -> a234.txt.

Every line starts with command id, then one space as separator followed by command output.

Commands in the output file can be in any order.

Example of an output file:

```
1 Hello_world
2 value
3 Beautiful_sunnyday
4 Not filled !
```

To manually send/receive files from a remote machine can be used the following commands:

Send a file from the local machine to app1:
```
scp -i ~/.ssh/hackathon.rsa /tmp/aa.json outscale@<app1_ip>:/data/input/aa.json
```

List files in app1 /data/output:
```
ssh -o StrictHostKeyChecking=no -i ~/.ssh/hackathon.rsa outscale@<app1_ip> "ls /data/output"
```

Copy file from app1 to the local machine:
```
scp -i ~/.ssh/hackathon.rsa outscale@<app1_ip>:/data/input/aa.json /tmp/
```

You can use the evaluation script described in [metrics/README.md](metrics/README.md).

## Microservice 1
A simple Web server. It is used by the application 1 to process some commands.

The source code is in ```ms1/src/app.py```.

In the VM the file is copied and running in ```/home/outscale/``` folder as a service.

- To stop: ```sudo systemctl stop ms1.service```
- To start: ```sudo systemctl start ms1.service```
- To restart: ```sudo systemctl restart ms1.service```
- To see service log: ```journalctl -u ms1.service```

**Attention:** If you update the code in place into the VM don't forget to restart the service.

The application is accessible via ```http://<ms1_ip>:8000/...``` from everywhere.

To connect from other VMs ```<ms1_ip>``` can be replaced by ```ms1``` (configured in ```/etc/hosts```)

## Database 1
PostgreSQL database.

The prefill script is in ```db1/db_init.sql```.

For debugging you can connect to it via web interface ```http://<db1_vm_ip>:8080``` using these connection parameters:
```
host: postgres
username: postgres
password: postgres
database: postgres
```

# Connections between containers
VMs can be accessed by their short names: app1, ms1, and db1
These hosts are added to /etc/hosts of all VMs

# Run vvaluation
To start the evaluation:
```
cd metrics
./start.sh
```

The script sends the files from ```metrics/input``` to app1, waits for them to be processed, checks the output, and calculates the power consumption.

See [metrics/README.md](metrics/README.md) for detailes.
