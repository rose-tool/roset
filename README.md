# ROuting SEcurity Tool (ROSE-T)

## What is it?
**ROuting SEcurity Tool (ROSE-T)** is a network router configuration checker.

It allows to ensure that a certain router configuration is MANRS-compliant.

It leverages:
* __[Batfish](https://github.com/batfish/batfish)__ to parse and abstract the vendor configuration.
* __[Kathará](https://github.com/KatharaFramework/Kathara)__ to emulate a virtual network scenario in which the router **realistically interacts** with providers and customers.

**WARNING**: The current version is in alpha state for demonstration purposes, and it is not intended to be used in production.

## How does it work?

![img.png](img.png)

### Step 1: Gather Candidate Information
In this step, ROSE-T verifies: 
1. That the networks announced to transit are in the IRR Entry.
2. That the networks in the IRR Entry are announced to transits.

### Step 2: Parse the Configuration
In this step, ROSE-T: 
1. Exploits Batfish to parse the vendor configurations. 
2. Enriches the information from Batfish with missing information (e.g., IPv6).

### Step 3: Analyze the Configuration
In this step ROSE-T analyzes the parsed configuration to reconstruct the neighbours relationships. 
It integrates the information from the IRRs and a RIB dump to infer the topology and understand the relationships. 

### Step 4: Emulate the Minimal Network Topology
In this step the system uses the computed information to build a minimal network topology to be emulated. 
To power the emulation, ROSE-T leverages on Kathará. The candidate router will use the original configuration/vendor software, while other ASes are emulated as a single router running FRRouting. 

### Step 5: Verify Compliance to MANRS
In this step the system leverages on the emulated environment to verify MANRS Action 3 and Action 4. 
- Action 3 (Anti-Spoofing):
  For each provider:
  2. Create a client inside the provider AS.
  3. Assign IPs (v4/v6) to each created client
  4. Send the spoofed ICMP packet
  
![img_2.png](img_2.png)

- Action 4 (Filtering):
  For each customer: 
  1. Select non-overlapping subnet and announce it to the candidate router.
  2. Wait that BGP converges.
  3. Check the provider's received routes using the FRRouting control plane.
  
![img_3.png](img_3.png)
  
## Supported Vendor Routers
Currently, ROSE-T supports two Vendor Routers:
- **Juniper VMX** through a [hellt/vrnetlab](https://github.com/hellt/vrnetlab) VM embedded in a Docker container. 
  - We use a custom version of the VM, which `.patch` files are located in the `vrnet_patches` folder.
- **Cisco IOS XR** using the official [XRd Control Plane](https://software.cisco.com/download/home/286331236/type/280805694) Docker image.
  - You need to properly configure the host machine before running the XRd container. See [this tutorial](https://xrdocs.io/virtual-routing/tutorials/2022-08-22-setting-up-host-environment-to-run-xrd/) for more information.
    - Particularly, you have to increase the `fs.inotify.max_user_instances` and `fs.inotify.max_user_watches` to at least `64000`:
      ```bash
        sysctl -w fs.inotify.max_user_instances=64000
        sysctl -w fs.inotify.max_user_watches=64000
      ```

## Hands-on

### Pre-Requisites

1. Run the Batfish container:
```
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone
```

2. Download the requisites:
```
python3 -m pip install -r src/requirements.txt
```

3. You need an updated a MRT RIB dump downloaded from a Route Collector, for example you can download the latest dump from [RRC00](https://data.ris.ripe.net/rrc00/).
Now, enter the `resources` directory, and run the `load_mrt.py` script:
```
cd resources
python3 load_mrt.py <TABLE_DUMP_RIB_FILE> <OUTPUT_FILE.db>
```
The command requires two positional parameters: 
- `<TABLE_DUMP_RIB_FILE>` is the RIB dump in `.gz` format. 
- `<OUTPUT_FILE.db>` is the name of the output SQLite3 database (stored in the `resources` directory). By default, the name is `rib_latest.db`.

## Build the Juniper VMX image (only if you plan to test Juniper)

1. Clone the [hellt/vrnetlab](https://github.com/hellt/vrnetlab) repository, you can clone it inside the root directory of ROSE-T:
```bash
git clone https://github.com/hellt/vrnetlab
```

2. Apply the patch located in the `vrnet_patches` folder. If you cloned `vrnetlab` in the root directory of ROSE-T:
```bash
cd vrnetlab
git apply ../vrnet_patches/vmx.patch
```

3. Now, to build the VMX image, copy the VM `.tar.gz` provided by Juniper inside the `vmx` folder and run `make`. The process will take few minutes.

**NOTE:** For now, the container name is hardcoded into ROSE-T [here](https://github.com/Skazza94/roset/blob/51665243d054ccb9af8da91503ebc6b9716ec8c6/src/rs4lk/configuration/vendor/vmx_configuration.py#L159C35-L159C35). We plan to add a configuration parameter to specify the image name. If your image name differs, you have to manually change it.

## Run a Test

To run a test, the simplest command is:
```
cd src
python3 test.py --config_path <CONFIGURATION_PATH>
```

The supported parameters are:
- `--batfish_url`: The URL for the Batfish API endpoint. If you run the Docker container, the default value is `localhost`.
- `--config_path`: Path to the configuration to test.
- `--rib_dump`: Path pointing to the `.db` SQLite3 database containing the parsed MRT RIB dump. By default, the value is `resources/rib_latest.db`.
- `--exclude_checks`: A comma separated string to exclude some MANRS checks. Supported values are `spoofing` and `leak`.
- `--result-level`: The output of the validation will report both successful checks, warnings and errors. You can change the level of output with this parameters. Supported values are `WARNING`, `SUCCESS`, and `ERROR`.

The test can take up to few minutes, depending on your hardware. Ensure that you have a good amount of RAM and nested virtualization enabled.

**NOTE**: ROSE-T works only on Docker on Linux or WSL2, and it is compatible only with the `amd64` architecture (Apple Silicon is not supported).
