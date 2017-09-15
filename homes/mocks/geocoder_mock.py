class GeocoderMock(object):
    latlng = [0,1]


class GeocoderErrorMock(object):
    latlng = False


class GeocoderExceptionMock(object):
    latlng = Exception('test')