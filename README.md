# ROuting SEcurity Tool (ROSE-T)

## What is it?
**ROuting SEcurity Tool (ROSE-T)** is a network router configuration checker.

It allows to ensure that a certain router configuration is MANRS-compliant.

It leverages:
* __[Batfish](https://github.com/batfish/batfish)__ to parse and abstract the vendor configuration.
* __[Kathará](https://github.com/KatharaFramework/Kathara)__ to emulate a virtual network scenario in which the router **realistically interacts** with providers and customers.

**WARNING**: The current version is in alpha state for demonstration purposes, and it is not intended to be used in production.

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

Download this repository.

