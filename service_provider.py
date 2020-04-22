from imp import IndustryMarketplace
import pprint

class ServiceProvider(IndustryMarketplace):
    name = 'DronesRus'
    service_provider = True
    fund_wallet = False
    gps_coords = '54.123, 4.321'
    
    endpoint = 'http://localhost:4000'

    def on_cfp(self, data, irdi, submodels):
        '''
        As soon as this service provider receives a CfP this function is called
        You can use the supplied irdi and submodels to define a price if you like
        '''

        print('Call for Proposal received for irdi %s!' % irdi)
        #print('Submodels: ')
        #pprint.pprint(submodels)
        
        if irdi == '0173-1#01-AAJ336#002':
            price = 10
        elif irdi == '0173-1#01-AAO742#002':
            price = 5
        else:
            print('We only do Drone transport and EV charging, ignore this one!')
            return

        try:
            ret = self.proposal(data, price_in_iota=price)
        except Exception as e:
            print('Unable to send proposal', e)
        
        print('proposal sent!')

    def on_accept_proposal(self, data, irdi, submodels):
        print('Proposal accepted! Start fulfilling')
        print('Sending inform confirm')
        ret = self.inform_confirm(data)
        #print(ret)

    def on_reject_proposal(self, data, irdi, submodels):
        print('Proposal rejected! Either do nothing or offer a Discount?')
        #pprint.pprint(data)

    def on_inform_payment(self, data, irdi, submodels):
        print('Payment received! IMP transaction done!')
        #pprint.pprint(data)


if __name__ == '__main__':
    imp = ServiceProvider()
    imp.listen()
