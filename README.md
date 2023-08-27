# Solar plus Battery EV charging park simulator
Simulate the hourly energy and cash flows of a solar + battery EV charging park throughout a whole year.

The cars are assumed to arrive randomly but poisson distributed. The solar radiation is assumed to be sine wave shaped throughout the year with a 10 times higher power in summer (perfectly facing the sun in summer). Then the energy flows are derived hourly with accounting for the cash flows.

Parameters to play around with are:
* charge rate in kW
* average charge in kWh
* average customers per day
* number of charge points
* solar radition at the location
* solar park capacity in kW
* battery size in kWh
* electricity sales price per kWh

Parameters for accounting are:
* grid electricity cost
* grid electricity sales price
* investment cost per solar kW
* investment cost per inverter kW
* investment cost per battery kWh

The model then reports all energy flows and cash flows accordingly, as well as a income statement by accounting for the depreciation.
