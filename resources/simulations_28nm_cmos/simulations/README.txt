# Created by: Diogo Andre
# Date: 18-05-2022

This file contains the simulations of the DC operating point of generic and RF PMOS and NMOS devices
existing in the 28nm TSMC technology node installed in this machine. This data was used to build a model
of the transistor that allows to obtain the best Channel Width (W) and Channel Length (L) for a device using the
Gm/Id design methodology. Given the specifications of:
- gm
- id
- gm/id
- ft
- gm/gds
- vdsat
- inversion coefficient (IC)
- vds
- vgs
the model will allow us to size the P or N channel CMOS transistor.

The simulations performed and exported to the directories present in this folder were performed through a 
parametric sweep analysis of 4 out of 5 degrees of freedom for the NMOS and PMOS transistors: Vgs, L, Vds, 
and Vsb, keeping W constant equal to a single finger of width=2.3u M, and L = Lmin = 30nm.

The parametric sweep was performed on two variables at a time, Vgs and Vds, while manually varying the Vbs, 
and L variables for each parametric sweep.
The values used during the simulations are as given in the following table:
	From	To	Sweep Type	Step Size
L	1xLmin	3xLmin	Linear Steps	Lmin=30n M
Vbs	0 V	600m V	Linear Steps	100m V
Vds	0 V	1.2 V	Linear Steps	100m V
Vgs	0 V	1.2 V	Linear Steps	50m V	<-- Abciss Variable (Main control X axis variable)


The folder tree of this main directory can be represented as given by the following tree diagram.

simmulations/
|--ncell/
|  |-- # ... simulation files for a 28nm generic NMOS device
|--pcell/
|  |-- # ... simulation files for a 28nm generic PMOS device
|--rf_ncell/
|  |-- # ... simulation files for a 28nm RF NMOS device
|--rf_pcell/
|  |-- # ... simulation files for a 28nm RF PMOS device
|--config.scs 	# configuration file to add to ADE L > Setup > Simulation Files... > Definition Files, 
|		# in order to save all the device model's parameters during DC operating point simulation sweep
/

The device model's parameters saved in a .CSV file after each simulation are:

-cds: Cdrain_source parasitic capacitor
-cgb: Cgate_bulk capacitor
-cgd: Cgate_drain parasitic capacitor
-cgs: Cgate_source parasitic capacitor
-csb: Csource_bulk parasitic capacitor
-cdb: Cdrain_bulk parasitic capacitor
-gds: Channel conductance
-gm: Device transconductance
-id: DC OP channel current
-gmbs: Device's bulk to source transconductance (body effect)
-vdsat: Device drain to source saturation voltage
-region: Channel Inversion region
-gmoverid: gm/id value of device transconductance efficiency
-ft: intrinsic device maximum operating frequency
-self_gain: gm/gds value of intrinsic device gain


