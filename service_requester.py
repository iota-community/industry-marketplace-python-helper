from imp import IndustryMarketplace
import pprint
import sys

class ServiceRequester(IndustryMarketplace):
    name = 'ProSumer'
    service_provider = False
    fund_wallet = True
    gps_coords = '54.000, 4.000'

    endpoint = 'http://localhost:4000'
    
    def on_proposal(self, data, irdi, submodels):
        '''
        Accept only if the price is between 5 and 15
        '''
        self.log('on proposal called!')
        try:
            price = self.get_price(irdi, submodels)
            self.log('Received proposal for %si for irdi %s' % (price, irdi))
            if not price:
                self.log('Price not found, submodels: %s' % submodels)

            if price >= 5 and price <= 15:
                self.log('Accepting proposal')
                self.accept_proposal(data)
            else:
                self.log('Rejecting proposal')
                self.reject_proposal(data)
        except Exception as e:
            self.log('Error on accepting: %s' % e)

    def on_inform_confirm(self, data, irdi, submodels):
        self.log('Offer confirmed, time to pay')
        self.inform_payment(data)


if __name__ == '__main__':

    imp = ServiceRequester()
    
    # Either run it as a listeing service
    if len(sys.argv) == 1:
        imp.listen()
    
    # Or as a one time command requesting a drone!
    if len(sys.argv) == 2 and sys.argv[1] == 'request_drone':

        values = {
            '0173-1#02-AAJ336#002': 2,
            '0173-1#02-BAF163#002': '54.1234, 4.3210',
            '0173-1#02-AAO631#002': '54.4321, 4.5210',
        }

        ret = imp.cfp(irdi='0173-1#01-AAJ336#002', values=values, location='54.321, 4.123')
        #pprint.pprint(ret)
    
    if len(sys.argv) == 2 and sys.argv[1] == 'drone_inspection':

        values = {
            '0173-1#02-AAP788#001': 2,
            '0173-1#02-AAY979#001': 10,
            '0173-1#02-BAF163#002': '54.4321, 4.5210',
        }

        ret = imp.cfp(irdi='0173-1#01-AAP788#001', values=values, location='54.321, 4.123')
        pprint.pprint(ret)
