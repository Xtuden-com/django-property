import Ajax from './ajax';

export default class Toggler{

  static toggle(link){

    Ajax.getAjax(link.getAttribute('href')) // Url based on submitted form action
      .then(JSON.parse)
      .then(function(data){
        if (data.status === 200){
          const icon = link.querySelector('.fa');
          if (icon){
            if (icon.classList.contains(link.getAttribute('data-active'))){
              icon.classList.remove(link.getAttribute('data-active'));
              icon.classList.add(link.getAttribute('data-inactive'));
            }else{
              icon.classList.remove(link.getAttribute('data-inactive'));
              icon.classList.add(link.getAttribute('data-active'));
            }
          }
        }
      })
      .catch(err => console.error(err));
  }

  static addToggleHandler(){
    let links = document.querySelectorAll('.toggle--link');

    links.forEach(function(link){
      link.addEventListener('click', function(e){
        e.preventDefault();
        Toggler.toggle(this);
      });
    });
  }

}
