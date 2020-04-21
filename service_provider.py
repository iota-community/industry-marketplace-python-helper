from imp import IndustryMarketplace
import pprint

class ServiceProvider(IndustryMarketplace):
    name = 'DronesRus'
    service_provider = True
    fund_wallet = False
    gps_coords = '54.123, 4.321'
    
    endpoint = 'http://localhost:4001'

    def on_cfp(self, data, irdi, submodels):
        # Automatically respond to every cfp with a price of 10, no filtering
        print('Call for Proposal received for irdi %s!' % irdi)
        print('Submodels: ')
        pprint.pprint(submodels)
        
        try:
            ret = self.proposal(data, price_in_iota=10)
        except Exception as e:
            print('Unable to send proposal', e)
        
        print('proposal sent!')
        pprint.pprint(ret)



if __name__ == '__main__':
    imp = ServiceProvider()
    imp.listen()
