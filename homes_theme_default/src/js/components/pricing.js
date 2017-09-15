import Ajax from './ajax';

export default class Pricing{

  static populatePriceSelects(searchType, minPrice, maxPrice){
    switch(searchType.options[searchType.selectedIndex].value){
    case 'sales':{
      Pricing.populatePriceSelectGroup('/json/prices/2/', minPrice, maxPrice);
      break;
    }
    default:{
      Pricing.populatePriceSelectGroup('/json/prices/1/', minPrice, maxPrice);
      break;
    }
    }
  }

  static populatePriceSelectGroup(url, minElement, maxElement){
    Ajax.getAjax(url)
      .then(JSON.parse)
      .then((data) => data.map((item)=>{return{amount:item.fields.price, label:item.fields.label};}))
      .then(function(data){
        Pricing.bind(data, minElement);
        Pricing.bind(data, maxElement);
      })
      .catch(function(error){console.log(error);});
  }

  static getSelected(el){
    return (el.options.length > 0 && el.selectedIndex > -1) ? el.options[el.selectedIndex].value : false;
  }

  static bind(items, el){
    let selected = Pricing.getSelected(el);
    el.options.length = 0;
    for(const item of items){
      let opt = document.createElement('option');
      opt.value = item.amount;
      opt.innerHTML = item.label;
      el.appendChild(opt);
    }
    if (selected && items.filter(item => item.amount == selected).length > 0){
      el.value = selected;
    }
  }

  static search(){
    let searchType = document.getElementById('id_search_type');
    let minPrice = document.getElementById('id_min_price');
    let maxPrice = document.getElementById('id_max_price');

    Pricing.populatePriceSelects(searchType, minPrice, maxPrice);

    searchType.addEventListener('change',function(){
      Pricing.populatePriceSelects(searchType, minPrice, maxPrice);
    });
  }
}