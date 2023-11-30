# ROSE-T Global Information Verifier

This folder contains the Prolog code to perform the verification of Action 4 (Global Information).

## Files

- `Makefile`: Instructions on how to compile the program.
- `main.pl`: Main program to manage input and output messages.
- `rir.pl`: Module to parse RPSLng fields in RIR DB.
- `bgp.pl`: Module to parse BGP table from a RouteCollector.
- `check.pl`: Module to find matching transit declarations.

## Quick Start

1. Download and install Prolog.
2. Download a RIB dump from a RouteCollector (an example [here](https://archive.routeviews.org/bgpdata/2023.10/RIBS/rib.20231031.2200.bz2)).
3. Get [`ubgpsuite`](https://git.doublefourteen.io/bgp/ubgpsuite) where the tool `bgpgrep` belongs to.
4. Choose the AS number to analyse (e.g., `AS59715`), then extract the AS from the RIB. An example of the command is:
```bash 
./bgpgrep ./rib.20231031.2200.bz2 -aspath "59715$" > 59715.bgp
```
5. Extract the `aut-num` object, for the chosen AS, from an IRR. An example command is:
```bash 
whois AS59715|iconv -f ISO-8859-1 -t UTF8-MAC|sed -n -e '/aut-num:/,/source:         RIPE/ p' > 59715.rir
```
6. Build the project:
```bash
make
```
7. Run the verification, for example:
```bash
./verify --bgp=59715.bgp --rir=59715.rir
```