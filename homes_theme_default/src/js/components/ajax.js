export default class Ajax{
  static getAjax(url) {
    return new Promise(function(resolve, reject){
      let req = new XMLHttpRequest();
      req.open('GET', url);
      req.onload = function(){
        if (req.status == 200){
          resolve(req.response);
        }else{
          reject(new Error(req.statusText));
        }
      };
      req.onerror = function(){
        reject(new Error('Network Error'));
      };
      req.send();
    });
  }
  static postAjax(url, data){
    return new Promise(function(resolve, reject){
      let req = new XMLHttpRequest();
      req.open('POST', url, true);
      req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      req.onload = function(){
        if (req.status == 200){
          resolve(req.response);
        }else{
          reject(new Error(req.statusText));
        }
      };
      req.onerror = function(){
        reject(new Error('Network Error'));
      };
      req.send(data);
    });
  }
}
