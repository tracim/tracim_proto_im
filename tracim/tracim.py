import logging
from errbot import BotPlugin, botcmd, webhook

log = logging.getLogger(__name__)


class TracimPlugin(BotPlugin):
    """
    Just a Tracim plugin
    """

    ### Examples ###
    
    # @botcmd
    # def sendmefile(self, msg, args):
    #     stream = self.send_stream_request(msg.frm, open('/tmp/myfile.zip', 'rb'), name='myfile.zip',
    #                                       stream_type='application/zip')
    # @botcmd
    # def semdmecard(self,msg,args):
    #             self.send_card(title='EVEEERYTHINNNG !!!',
    #                    body='text body to put in the card',
    #                    #thumbnail='https://raw.githubusercontent.com/errbotio/errbot/master/docs/_static/err.png',
    #                    #image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
    #                    link='http://www.google.com',
    #                    fields=(('First Key', 'Value1'), ('Second Key', 'Value2')),
    #                    color='red',
    #                    to=self.build_identifier('~demo-notif'))

    
    @webhook
    def message(self, request):
        log.info("receive :" + str(request))
        rooms = [str(room) for room in self.rooms()]
        log.info("bot in rooms :" + str(rooms))
        if request['payload']['to'] in rooms:
            if request['type'] == 'IM_txt':
                # Only support title, body and link value for message content
                # simple message formating.
                txt = ""
                if 'title' in request['payload']:
                    if request['payload']['title']:
                        txt += "**{}**\n".format(request['payload']['title'])
                if 'body' in request['payload']:
                    if request['payload']['body']:
                        txt += "{}\n".format(request['payload']['body'])
                if 'link' in request['payload']:
                    if request['payload']['link']:
                        txt += "{}\n".format(request['payload']['link'])
                log.info('msg:' + txt)
                self.send(
                    self.build_identifier(request['payload']['to']),
                    txt
                )
            elif request['type'] == 'IM_card':
                request['payload']['to'] = self.build_identifier(
                    request['payload']['to'])
                log.info("sending card :" + str(request['payload']))
                self.send_card(**request['payload'])
            else:
                log.warning('Receive unsupported message type' +
                            request['type'])
        else:
            log.warning('ignore message to' + request['payload']['to'])
        return "OK"
