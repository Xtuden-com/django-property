import Ajax from '../js/components/ajax';

const MockXMLHttpRequest = require('mock-xmlhttprequest');

describe('Ajax testing', () => {
  let backup = null;
  beforeAll(()=>{
    backup = window.XMLHttpRequest;
    window.XMLHttpRequest = MockXMLHttpRequest;
  });
  afterAll(()=>{
    window.XMLHttpRequest = backup;
  });
  test('should return a promise resolve from remote', () => {
    MockXMLHttpRequest.onSend = xhr => xhr.respond(200, [], JSON.stringify({result:'success'}));
    return Ajax.getAjax('http://example.com')
      .then(JSON.parse)
      .then(data => expect(data.result).toBe('success'))
  });
  test('should cause a promise reject error from remote', () => {
    MockXMLHttpRequest.onSend = xhr => xhr.respond(403, [], JSON.stringify({result:'success'}));
    return Ajax.getAjax('http://example.com')
      .catch(function(error){expect(error.message).toBe('Forbidden')});
  });
});