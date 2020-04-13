from imp import IndustryMarketplace
import sys

class ServiceRequester(IndustryMarketplace):
    name = 'ProSumer'
    service_provider = False
    fund_wallet = False
    gps_coords = '54.000, 4.000'
    
    def on_proposal(self, data):
        '''
        Always accept the proposal automatically 
        '''
        print('Accepting proposal')
        self.accept_proposal(data)


if __name__ == '__main__':

    imp = ServiceRequester()

    if len(sys.argv) == 1:
        imp.listen()
    
    if len(sys.argv) == 2 and sys.argv[1] == 'request_drone':

        values = {
            '0173-1#02-AAJ336#002': 2,
            '0173-1#02-BAF163#002': '54.1234, 4.3210',
            '0173-1#02-AAO631#002': '54.4321, 4.5210',
        }

        imp.cfp(irdi='0173-1#01-AAJ336#002', values=values, location='54.321, 4.123')
