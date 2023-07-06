# Routing Security 4 Lazy Kids (RS4LK)

**Routing Security 4 Lazy Kids (RS4LK)** is a network router configuration checker.

It allows to ensure that a certain router configuration is compliant with MANRS.

It leverages:
* __[Batfish](https://github.com/batfish/batfish)__ to parse and abstract the vendor configuration.
* __[Kathará](https://github.com/KatharaFramework/Kathara)__ to emulate a virtual network scenario in which the router **realistically interacts** with providers and customers.
The vendor router is emulated through a [hellt/vrnetlab](https://github.com/hellt/vrnetlab) VM. Other routers are plain FRRouting containers.

**WARNING**: The current version is in alpha state for demonstration purposes, and it is not intended to be used in production.
It currently supports Juniper VMX configuration ONLY.
Moreover, it requires a patched version of Kathará (with vrnetlab support) which will be released soon.

