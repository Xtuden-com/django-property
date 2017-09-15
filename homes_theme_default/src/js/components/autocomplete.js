import Ajax from './ajax';

export default class Autocomplete{

  static showSpinner(el){
    el.classList.add('spinner');
  }

  static hideSpinner(el){
    el.classList.remove('spinner');
  }

  static createResultsList(location, results, items){
    let ul = document.createElement('ul');
    results.appendChild(ul);
    for(let item of items){
      let li = document.createElement('li');
      let a = document.createElement('a');
      a.setAttribute('href','javascript:void(0);');
      a.appendChild(document.createTextNode(item.label));
      a.addEventListener('click', function(){
        location.value = item.label;
        Autocomplete.hideSpinner(location);
        Autocomplete.hideResults(results);
      });
      li.appendChild(a);
      ul.appendChild(li);
    }
  }

  static showResults(results){
    results.style.display = 'block';
    results.innerHTML = '';
  }

  static hideResults(el){
    el.style.display = 'none';
  }

  static google(){

    let location = document.getElementById('id_location');
    let results = document.getElementById('id_results');

    location.addEventListener('keydown', e => {
      var timeout = null;
      if (e.key.length == 1 && location.value.length >= 3){
        clearTimeout(timeout);
        timeout = setTimeout(()=>{
          Autocomplete.showSpinner(location);
          Ajax.getAjax(`/json/places/${location.value}`)
            .then(JSON.parse)
            .then(data => data.map((item) => {return {label: item};}))
            .then(
              data => {
                Autocomplete.showResults(results);
                Autocomplete.createResultsList(location, results, data);
              }
            )
            .catch(function(error){console.error(error);});
        }, 500);
      }else{
        Autocomplete.hideSpinner(location);
        Autocomplete.hideResults(results);
      }
    });

  }

}
