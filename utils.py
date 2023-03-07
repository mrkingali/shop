from kavenegar import *


def send_otp_code(phone_number, code):
    # api = KavenegarAPI('6E70764F35316366616A70313030504C6E73525072797A79547658693766534B4653444D7A765373436C413D')
    # message = f'{code}کد ورود شما به شاپ :'
    # params = {'sender': '1000596446', 'receptor': str(phone_number), 'message': str(message)}
    # response = api.sms_send(params)
    # return response

    try:
        api = KavenegarAPI('api')
        params = {
            'sender': '',  # optional
            'receptor': str(phone_number),  # multiple mobile number, split by comma
            'message': str(code),
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
