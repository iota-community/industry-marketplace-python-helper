from imp import IndustryMarketplace
import pprint
import sys

class ServiceRequester(IndustryMarketplace):
    name = 'ProSumer'
    service_provider = False
    fund_wallet = True
    gps_coords = '54.000, 4.000'

    endpoint = 'http://localhost:4001'
    
    def on_proposal(self, data, irdi, submodels):
        '''
        Accept only if the price is between 5 and 15
        '''
        print('Received proposal')
        price = submodels['0173-1#02-AAJ333#002']['value']

        try:
            if price >= 5 and price <= 15:
                print('Accepting proposal')
                self.accept_proposal(data)
            else:
                print('Rejecting proposal')
                self.reject_proposal(data)
        except Exception as e:
            print('Error on accepting', e)
            pprint.pprint(data)

    def on_inform_confirm(self, data, irdi, submodels):
        print('Offer confirmed, time to pay')
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
