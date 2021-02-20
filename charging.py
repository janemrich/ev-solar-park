import numpy as np
from numpy import sin, pi
import scipy
import scipy.stats

def sunshine(day):
    sinuswave = sin((day/365)*2*pi)
    shine = ((sinuswave + 1)/2) * 0.9 + 0.1
    shine = shine * 2 * (365/402)
    return shine

class park:



    def __init__ (self, charging_speed, average_charge, cars_per_day, kwh_per_panel_year):
        self.charging_speed = charging_speed
        self.average_charge = average_charge
        self.cars_per_day = cars_per_day
        self.kwh_per_panel_year = kwh_per_panel_year

        # electricity prices
        self.grid_sale_price = 0.05
        self.grid_buy_price = 0.2

        # installation cost
        self.cost_per_panel_kw = 250
        self.cost_inverter_per_kw = 5000 / 50
        self.cost_battery_per_kwh = 1200

        self.total_car_charging = 0
        self.grid_bought_energy = 0
        self.grid_sold_energy = 0
        self.total_battery_usage = 0

    def set_parameters(self, n_chargers, solar_capacity, battery_capacity, sales_price):
        self.n_chargers = n_chargers
        self.solar_capacity = solar_capacity
        self.battery_capacity = battery_capacity
        self.sales_price = sales_price

    def net_sales_price(self):
        return self.sales_price / 1.19

    def charging_demand(self):
        cars = np.random.poisson(16, self.cars_per_day)
        return [car % 24 for car in cars]

    def sun_on_day(self, day):
        # kWh on this day
        return sunshine(day) * (self.kwh_per_panel_year/365) * self.solar_capacity

    def electricity_flows_on_day(self, day, cars):
        kwh_on_day = self.sun_on_day(day)
        sun_hours = scipy.stats.norm(12, 3)

        cars = np.sort(cars)

        waiting = []
        battery_state = self.battery_capacity
        for hour in range(24):
            mask = np.where(cars == hour)
            new = cars[mask]

            for car in new:
                waiting.append(self.average_charge)

            charge_capacity = self.charging_speed * self.n_chargers

            used_electricity = 0
            charged_cars = 0
            for car, charge in enumerate(waiting):
                if charge_capacity == 0: break
                if charge < charge_capacity:
                    charge_capacity -= charge
                    used_electricity += charge
                    charged_cars += 1
                else:
                    partial_charge = charge - charge_capacity
                    waiting[car] = partial_charge
                    charge_capacity = 0
                    used_electricity += partial_charge

            waiting = waiting[charged_cars:]
            self.total_car_charging += used_electricity

            solar_energy = kwh_on_day * sun_hours.pdf(hour)

            # use up solar energy
            if solar_energy > used_electricity:
                solar_energy -= used_electricity
                used_electricity = 0
            else:
                used_electricity -= solar_energy
                solar_energy = 0

            # use battery
            if battery_state > used_electricity:
                battery_state -= used_electricity
                used_electricity = 0
                self.total_battery_usage += used_electricity
            else:
                used_electricity -= battery_state
                self.total_battery_usage += battery_state
                battery_state = 0

            # charge battery
            if solar_energy > 0 and battery_state < self.battery_capacity:
                charge = self.battery_capacity - battery_state

                if solar_energy > charge:
                    solar_energy -= charge
                    battery_state += charge
                else:
                    battery_state += solar_energy
                    solar_energy = 0

            # buy from grid
            if used_electricity > 0:
                self.grid_bought_energy += used_electricity
                used_electricity = 0

            # sell to grid
            if solar_energy > 0:
                self.grid_sold_energy += solar_energy
                solar_energy = 0

    def report_energies(self):
        print('-- energy flows --')
        print('bought energy \t', int(self.grid_bought_energy))
        print('sold energy \t', int(self.grid_sold_energy))
        print('charged energy \t', int(self.total_car_charging))
        if battery_size > 0:
            print('battery usage \t', int(self.total_battery_usage), ' cycles ', int(self.total_battery_usage / self.battery_capacity))
            self.battery_cycles = int(self.total_battery_usage / self.battery_capacity)

    def report_invest(self):
        chargers = self.n_chargers * 22500
        chargers += (self.n_chargers // 2) * 45000

        inverter = self.solar_capacity * self.cost_inverter_per_kw

        panels = self.solar_capacity * self.cost_per_panel_kw

        if (self.n_chargers * self.charging_speed > self.solar_capacity):
            grid_connect = self.n_chargers * self.charging_speed
        else:
            grid_connect = self.solar_capacity
        grid_connect *= 100

        batteries = self.battery_capacity * self.cost_battery_per_kwh

        self.invest_chargers = chargers
        self.invest_inverter = inverter
        self.invest_panels = panels
        self.invest_grid_connect = grid_connect
        self.invest_batteries = batteries

        print('-- investment --')
        print('charger\t\t', int(chargers))
        print('inverter\t', int(inverter))
        print('panels\t\t', int(panels))
        print('grid_connect ', int(grid_connect))
        print('batteries\t', int(batteries))

        total = chargers + inverter + panels + grid_connect + batteries
        print('total\t ', round(total, 0))
        return total

    def report_cash_flows(self):
        self.grid_sales = int(self.grid_sold_energy * self.grid_sale_price)
        self.grid_buys = int(self.grid_bought_energy * self.grid_buy_price)
        self.charging_revenue = int(self.total_car_charging * self.net_sales_price())

        self.total_cash_flow = self.grid_sales - self.grid_buys + self.charging_revenue

        print('-- cash flows --')
        print('grid sales\t\t', self.grid_sales)
        print('grid buys\t\t', self.grid_buys)
        print('charging revenue ', self.charging_revenue)
        print('total flow \t\t', self.total_cash_flow)
        return self.total_cash_flow

    def report_income_statement(self):
        revenue = self.grid_sales + self.charging_revenue

        depreciation = int(+ self.invest_chargers / 7
                        + self.invest_grid_connect / 30
                        + self.invest_inverter / 15
                        + self.invest_panels / 25)
        if battery_size > 0:
            depreciation += int(self.invest_batteries * (self.battery_cycles / 4000))

        expenses = self.grid_buys + depreciation

        print('-- income statement --')
        print('charging revenue ', self.charging_revenue)
        print('grid revenue ', self.grid_sales)
        print('total revenue ', revenue)

        print('electricity expense ', self.grid_buys)
        print('depreciation ', depreciation)
        print('total expenses ', expenses)

        print('gross income ', revenue - expenses)
        print('gross margin ', round((revenue-expenses) / revenue,2))





if __name__ == "__main__":
    charge_rate = 175
    average_charge = 30
    cars_per_day = 100
    kwh_per_panel_year = 900
    env = park(charge_rate, average_charge, cars_per_day, kwh_per_panel_year)

    chargers = 2
    solar_capacity = 600
    battery_size = 00
    sales_price = 0.25
    env.set_parameters(chargers, solar_capacity, battery_size, sales_price)

    for d in range(365):
        cars = env.charging_demand()
        env.electricity_flows_on_day(d, cars)

    env.report_energies()
    investment = env.report_invest()
    flow = env.report_cash_flows()
    print('RoI ', round(investment/flow, 1))

    env.report_income_statement()



