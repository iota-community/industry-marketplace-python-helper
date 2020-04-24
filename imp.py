import requests
import paho.mqtt.client as mqtt
import datetime
import json
import os
import pprint


class IndustryMarketplace:
    '''
    Abstract Industry Marketplace instance,
    Should not be called directly but you should inherit it 
    with your own implementation class. See `service_provider.py`
    for an example
    '''
    
    # Generic Marketplace settings, overwrite these to your needs
    service_provider = False
    name = 'Anonymous'
    fund_wallet = False
    gps_coords = None
    reply_time = 10
    
    # MQTT settings, leave as is to work out of the box with the ServiceApp
    mqtt_timeout = 60
    mqtt_port = 1883
    mqtt_id = None
    mqtt_broker = 'test.mosquitto.org'

    # The endpoint of the ServiceApp Node application
    endpoint = 'http://localhost:4000'
    eclass = None
    operations = None


    def __init__(self):
        self.mqtt_client = mqtt.Client()
        self.update_eclass_whitelist()

    def update_eclass_whitelist(self):
        '''
        Function to load the eclass whitelist or create it from it's source
        if it does not exist. Only these IRDI's and Attributes can be used
        with the Industry Marketplace right now.
        '''
        if not os.path.exists('eclass.json'):
            with open('eclass.json', 'wb') as fh:
                resp = requests.get('https://raw.githubusercontent.com/iotaledger/industry_4.0_language/master/catalog/eClass.json')
                fh.write(resp.content)
                self.eclass = resp.json()
        else:
            self.eclass = json.loads(open('eclass.json', 'r').read())
        
        if not os.path.exists('operations.json'):
            with open('operations.json', 'wb') as fh:
                resp = requests.get('https://raw.githubusercontent.com/iotaledger/industry_4.0_language/master/catalog/operations.json')
                fh.write(resp.content)
                self.operations = resp.json()
        else:
            self.operations = json.loads(open('operations.json', 'r').read())

    def get_price(self, irdi, submodels):
        '''
        Get the price for a irdi from the submodels
        '''
        try:
            return [x['value'] for x in submodels.values() if x['idShort'] == 'price'][0]
        except IndexError:
            return None

    def config(self):
        data = {
            'name': self.name, 
            'role': 'SP' if self.service_provider else 'SR', 
            'gps': self.gps_coords or '', 
            'wallet': self.fund_wallet
        }

        config = self.api('config', data=data)
        if config.get('success', False):
            self.log('Now running as %s under the name "%s"' % ('Service Provider' if self.service_provider else 'Service Requester', self.name))

        return config
    
    def api(self, uri, data=None):
        try:
            if data:
                resp = requests.post('%s/%s' % (self.endpoint, uri), json=data, timeout=15)
                #self.log('POST body: %s' % json.dumps(data))
                return resp.json()
            else:
                resp = requests.get('%s/%s' % (self.endpoint, uri), timeout=15)
                return resp.json()
        except requests.exceptions.ConnectionError as e:
            self.log('Unable to connect to Industry Marketmanager ServiceApp; Make sure it is running on %s' % self.endpoint)
            exit(1)

    def user(self):
        user = self.api('user')
        #self.log(user)
        return user

    def cfp(self, irdi, location=None, start_at=None, end_at=None, values=None):
        '''
        Send a call for proposal as a service requester

        irdi: ecl@ss irdi number for requested service/product, see https://www.eclasscontent.com
        location: LAT,LON
        start_at: Datetime object, if None defaults to now
        end_at: Datetime object, if None defaults to 10 minutes from now
        values: Dict with as keys the property ID's and as values the property values as defined by ecl@ss
        '''

        if self.service_provider:
            raise ValueError('Only Service Requesters are allowed to call this method')
        
        if not location:
            location = ''

        if not start_at:
            start_at = datetime.datetime.now() + datetime.timedelta(minutes=10)

        if not end_at:
            end_at = start_at + datetime.timedelta(minutes=20)

        start_ts = int(start_at.timestamp()) * 1000
        end_ts = int(end_at.timestamp()) * 1000

        user = self.user()

        data = {
            'messageType': 'callForProposal',
            'irdi': irdi,
            'userId': user.get('id'),
            'userName': user.get('name'),
            'replyTime': self.reply_time,
            'location': location,
            'startTimestamp': start_ts,
            'endTimestamp': end_ts,
            'creationDate': datetime.datetime.now().strftime('%d %B, %Y %I:%M %p'),
            'submodelValues': values or {},
        }

        pprint.pprint(data)

        ret = self.api('cfp', data=data)
        #self.log(ret)
        return ret
        #print(ret)
 
    
    def proposal(self, proposal_data, price_in_iota):
        '''
        Send a proposal as a response to a call for proposal
        Takes the original message it replies to as the `proposal_data` argument
        '''

        if not self.service_provider:
            raise ValueError('Only Service Providers are allowed to call this method')
        
        user = self.user()

        irdi = proposal_data['dataElements']['submodels'][0]['identification']['id']

        data = {
            'messageType': 'proposal',
            'irdi': irdi,
            'userId': user.get('id'),
            'userName': user.get('name'),
            'replyTime': self.reply_time,
            'price': int(price_in_iota),
            'originalMessage': proposal_data
        }

        ret = self.api('proposal', data=data)
        #self.log(ret)
        #print(ret)
        return ret


    def accept_proposal(self, proposal_data):

        if self.service_provider:
            raise ValueError('Only Service Requesters are allowed to call this method')
        
        user = self.user()

        irdi = proposal_data['dataElements']['submodels'][0]['identification']['id']
        price = proposal_data['frame'].get('price')

        data = {
            'messageType': 'acceptProposal',
            'irdi': irdi,
            'userId': user.get('id'),
            'userName': user.get('name'),
            'replyTime': self.reply_time,
            'originalMessage': proposal_data
        }

        ret = self.api('acceptProposal', data=data)
        return ret
    

    def inform_confirm(self, proposal_data):

        if not self.service_provider:
            raise ValueError('Only Service Providers are allowed to call this method')
        
        user = self.user()

        irdi = proposal_data['dataElements']['submodels'][0]['identification']['id']
        price = proposal_data['frame'].get('price')

        data = {
            'messageType': 'informConfirm',
            'irdi': irdi,
            'price': price,
            'userId': user.get('id'),
            'userName': user.get('name'),
            'replyTime': self.reply_time,
            'originalMessage': proposal_data
        }

        ret = self.api('informConfirm', data=data)
        return ret
    
    def inform_payment(self, proposal_data):

        if self.service_provider:
            raise ValueError('Only Service Requesters are allowed to call this method')
        
        user = self.user()

        irdi = proposal_data['dataElements']['submodels'][0]['identification']['id']
        price = proposal_data['frame'].get('price')

        data = {
            'messageType': 'informPayment',
            'irdi': irdi,
            'price': price,
            'userId': user.get('id'),
            'userName': user.get('name'),
            'replyTime': self.reply_time,
            'originalMessage': proposal_data
        }

        ret = self.api('informPayment', data=data)
        return ret


    def reject_proposal(self, proposal_data):
        if self.service_provider:
            raise ValueError('Only Service Requesters are allowed to call this method')
        
        user = self.user()

        irdi = proposal_data['dataElements']['submodels'][0]['identification']['id']
        price = proposal_data['frame'].get('price')

        data = {
            'messageType': 'rejectProposal',
            'price': price,
            'irdi': irdi,
            'userId': user.get('id'),
            'userName': user.get('name'),
            'replyTime': self.reply_time,
            'originalMessage': proposal_data
        }

        ret = self.api('rejectProposal', data=data)
        return ret
    

    def listen(self, mqtt=False):
        self.config()

        data = self.api('mqtt', {'message': 'subscribe'})
        if not data.get('success'):
            raise ValueError('Unable to subscribe to MQTT stream: %s' % data.get('error'))

        self.mqtt_id = data.get('id')
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, self.mqtt_timeout)
        self.mqtt_client.loop_forever()

    def log(self, message):
        print('[%s] %s' % (datetime.datetime.now(), message))

    def on_proposal(self, data, irdi=None, submodels=None):
        '''
        This function is called as soon as a proposal is received
        Implement this function to do what you need as you please
        '''
        
        self.log('`[WARNING] on_proposal` function not implemented yet, you might want to implement this!')
    
    def on_inform_confirm(self, data, irdi=None, submodels=None):
        '''
        This function is called as soon as a fulfillment has been confirmed
        Implement this function to do what you need as you please
        '''
        
        self.log('`[WARNING] on_inform_confirm` function not implemented yet, you might want to implement this!')
    
    def on_inform_payment(self, data, irdi=None, submodels=None):
        '''
        This function is called as soon as a payment has been completed
        Implement this function to do what you need as you please
        '''
        
        self.log('`[WARNING] on_inform_payment` function not implemented yet, you might want to implement this!')
    
    def on_cfp(self, data, irdi=None, submodels=None):
        '''
        This function is called as soon as a call for proposal is received
        Implement this function to do what you need as you please
        '''
        
        self.log('`[WARNING] on_cfp` function not implemented yet, you might want to implement this!')

    def on_accept_proposal(self, data, irdi=None, submodels=None):
        '''
        This function is called as soon as a proposal is accepted
        Implement this function to do what you need as you please
        '''
        
        self.log('`[WARNING] on_accept_proposal` function not implemented yet, you might want to implement this!')
    
    def on_reject_proposal(self, data, irdi=None, submodels=None):
        '''
        This function is called as soon as a proposal is rejected
        Implement this function to do what you need as you please
        '''
        
        self.log('`[WARNING] on_reject_proposal` function not implemented yet, you might want to implement this!')


    #TODO: Implement other callback functions

    def on_message(self, client, userdata, message):
        try:
            data = json.loads(message.payload)
        except json.decoder.JSONDecodeError:
            self.log('Unable to decode, no json found')
        
        try:
            self.log('Received %s from %s' % (data['data']['messageType'], data['data']['data']['userName']))
            
            try:
                dat = data['data']['data']
                first_request = dat['dataElements']['submodels'][0]['identification']
                irdi = first_request['id']
                submodels = first_request['submodelElements']
                submodeldict = dict([(x['semanticId'], x) for x in submodels])
            except Exception as e:
                self.log('Error getting data: %s' % e)


            if data['data']['messageType'] == 'proposal':
                self.on_proposal(dat, irdi=irdi, submodels=submodeldict)
            
            elif data['data']['messageType'] == 'acceptProposal':
                self.on_accept_proposal(dat, irdi=irdi, submodels=submodeldict)
            
            elif data['data']['messageType'] == 'rejectProposal':
                self.on_reject_proposal(dat, irdi=irdi, submodels=submodeldict)
            
            elif data['data']['messageType'] == 'informConfirm':
                self.on_inform_confirm(dat, irdi=irdi, submodels=submodeldict)
            
            elif data['data']['messageType'] == 'informPayment':
                self.on_inform_payment(dat, irdi=irdi, submodels=submodeldict)

            elif data['data']['messageType'] == 'callForProposal':
                self.on_cfp(dat, irdi=irdi, submodels=submodeldict)

            else:
                self.log('Unhandled message type: %s' % data['data']['messageType'])
            
        except KeyError as e:
            self.log('Invalid message format for data (%s) - %s' % (data, e))

    def on_connect(self, client, *args, **kwargs):
        self.log('connected')
        self.mqtt_client.subscribe(self.mqtt_id)
        self.log('subscribed to %s' % self.mqtt_id)

    def on_disconnect(self, client, *arg, **kwargs):
        self.log('mqtt disconnected')
