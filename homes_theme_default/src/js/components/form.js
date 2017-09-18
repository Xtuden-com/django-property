import Ajax from './ajax';
import Validator from './validator';

export default class Form {

  static hideAlert(form) {
    let alert = form.querySelector('.alert');
    if (!alert) return;
    alert.style.display = 'none';
    alert.className = 'alert';
    alert.innerHTML = '';
  }

  static showAlert(form, status, messages) {
    let alert = form.querySelector('.alert');
    if (!alert) return;
    alert.style.display = 'block';
    alert.classList.add(status);
    alert.focus();
    let ul = document.createElement('ul');
    alert.appendChild(ul);
    messages.forEach((message) => {
      let li = document.createElement('li');
      li.innerHTML = message.label;
      ul.appendChild(li);
    });
  }

  static getFormInputsAsData(form, token) {
    const elements = form.querySelectorAll('input,select,textarea');
    const data = [];
    elements.forEach(el => {
      if (el.type === 'checkbox') {
        data.push(encodeURIComponent(el.name) + '=' + encodeURIComponent(el.checked));
      } else {
        data.push(encodeURIComponent(el.name) + '=' + encodeURIComponent(el.value));
      }
    });
    data.push(`token=${token}`);
    return data.join('&').replace(/%20/g, '+');
  }

  static handleFormSubmit(form, token) {
    Form.hideAlert(form); // remove any previous alerts
    const errors = Validator.validate(form); // Carry out validation
    if (errors.length > 0) {
      Form.showAlert(form, 'alert-danger', errors);
    } else {
      Ajax.postAjax(form.action, Form.getFormInputsAsData(form, token)) // Url based on submitted form action
        .then(JSON.parse)
        .then(function (data) {
          if (data.status === 'success') {
            Form.showAlert(form, 'alert-success', [{name: '', label: 'Form submitted successfully'}]);
            setTimeout(() => {
              Form.hideAlert(form);
            }, 3000);
            form.reset();
          } else {
            Form.showAlert(form, 'alert-danger', data.messages);
          }
        })
        .catch(err => console.error(err));
    }
    form.elements['send'].disabled = false;
    form.elements['send'].innerHTML = 'Send Message';
  }
}
