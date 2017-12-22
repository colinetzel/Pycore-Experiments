# pycore Information #

This is simply a short writeup of things I learned about the pycore module while working on this code, similar to a FAQ. This may be of interest to other developers learning how to use the pycore module.

Date of last update to this document is 12/22/2017

## Linking Two Nodes ##

Establishing a link between two nodes requires the creation of a third node (the hubnode) to manage the link. This can be learned from one of the sample programs in pycore or looking through my code, here's a simple few lines of python code:

session = pycore.Session(persistent=True)

node1 = session.addobj(cls=pycore.nodes.CoreNode, name="n1")
node2 = session.addobj(cls=pycore.nodes.CoreNode, name="n2")
hub1 = session.addobj(cls=pycore.nodes.HubNode, name="hub1")

node1.newnetif(hub1, ["10.0.0.1/24"], ifname = "net1")
node2.newnetif(hub1, ["10.0.0.2/24"], ifname = "net2")

Note that two network interfaces are required, not one.

## Linkconfig ##

### A note on bandwidth ###

Leaving bandwidth undefined or setting it to 0 functions strangely, there isn't a bandwidth cap on the link effectively and it will generally be a lot higher than might be expected, most likely limited by how fast your machine runs CORE than any hard limit. So specify a bandwidth for both netifs that makes sense for what is being emulated.

### Default values and new calls to linkconfig ###

Whenever linkconfig is called it always needs an argument for each parameter being specified. CORE won't remember what was put as a value the last time linkconfig was called, it will just reset everything not provided to the initial undefined state. For example, each time linkconfig is called if a value for bandwidth is not provided it will reset to the behavior mentioned above.

### Setting parameters and round-trip settings ###

As mentioned above two network interfaces attached to a hubnode is required, a lot different from drawing a link between two gui objects in CORE-GUI

Each network interface applies its linkconfig parameters to one direction, generally you want to set parameters to both so the link functions the same both ways.

For example, when running TCP between two nodes if loss is set to 20% on both interfaces of the link, 20% of all remaining packets will be lost on each half of the round trip, which means about (1 - 0.8\*0.8) = 36% packet loss for the round trip. For delay the round trip delay will be a sum of the two netifs' delay, etc.

### Units ###

This isn't a quirk so much as something I confirmed experimentally to be thorough: the units of the network parameters in the linkconfig command are the same as the units displayed when manually editing a link in the CORE-GUI

Here's a table for easy reference.

Parameter | Units of parameter
----------| ------------------
Bandwidth | bps (bits per second)
Delay | us (microseconds)
Jitter | us (microseconds)
Loss | % (percent)
Duplicate | % (percent)












