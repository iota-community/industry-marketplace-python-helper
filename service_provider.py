from imp import IndustryMarketplace
import random
import pprint

class ServiceProvider(IndustryMarketplace):
    name = 'DronesRus'
    service_provider = True
    fund_wallet = False
    gps_coords = '54.123, 4.321'
    
    endpoint = 'http://localhost:4001'

    def on_cfp(self, data, irdi, submodels):
        '''
        As soon as this service provider receives a CfP this function is called
        You can use the supplied irdi and submodels to define a price if you like
        '''

        self.log('Call for Proposal received for irdi %s!' % irdi)
        #self.log('Submodels: ')
        #pprint.pprint(submodels)
        
        if irdi == '0173-1#01-AAJ336#002':
            price = random.randint(10, 20)
        elif irdi == '0173-1#01-AAO742#002':
            price = random.randint(5, 9)
        else:
            self.log('We only do Drone transport and EV charging, ignore this one!')
            return

        try:
            ret = self.proposal(data, price_in_iota=price)
        except Exception as e:
            self.log('Unable to send proposal', e)
        
        self.log('proposal sent! Requesting %si for this service' % price)

    def on_accept_proposal(self, data, irdi, submodels):
        self.log('Proposal accepted! Start fulfilling')
        self.log('Sending inform confirm')
        ret = self.inform_confirm(data)
        #self.log(ret)

    def on_reject_proposal(self, data, irdi, submodels):
        self.log('Proposal rejected! Either do nothing or offer a Discount?')
        #pprint.pprint(data)

    def on_inform_payment(self, data, irdi, submodels):
        self.log('Payment received! IMP transaction done!')
        #pprint.pprint(data)


if __name__ == '__main__':
    imp = ServiceProvider()
    imp.listen()
