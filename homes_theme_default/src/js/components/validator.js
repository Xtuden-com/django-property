export default class Validator{

  static isValidEmail(input){
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(input.value);
  }

  static hasValue(input){
    return input.value !== '';
  }

  static capitalize(words){
    return words.charAt(0).toUpperCase() + words.slice(1);
  }

  static errorMessage(name, message){
    return {input:name, label:`${Validator.capitalize(name)} ${message}`};
  }

  static validate(form){
    const elements = form.querySelectorAll('input,select,textarea');
    const errors = [];
    elements.forEach(function(el){
      if (el.required && !Validator.hasValue(el)){
        errors.push(Validator.errorMessage(el.name, 'is required'));
      }
      if (el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'textarea'){ //Validators only needed on input not selects
        switch(el.type){ // Based on the type text, email, number etc
        case 'email':{
          if (!Validator.isValidEmail(el)){
            errors.push(Validator.errorMessage(el.name, 'is not valid format'));
          }
          break;
        }
        }
      }
    });
    return errors;
  }

}
