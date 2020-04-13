from imp import IndustryMarketplace
import sys

class ServiceProvider(IndustryMarketplace):
    name = 'DronesRus'
    service_provider = True
    fund_wallet = False
    gps_coords = '54.123, 4.321'


if __name__ == '__main__':
    imp = ServiceProvider()
    imp.listen()
