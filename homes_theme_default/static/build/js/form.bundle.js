window["form"] =
webpackJsonp_name_([1],{

/***/ 7:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _ajax = __webpack_require__(0);

var _ajax2 = _interopRequireDefault(_ajax);

var _validator = __webpack_require__(8);

var _validator2 = _interopRequireDefault(_validator);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Form = function () {
  function Form() {
    _classCallCheck(this, Form);
  }

  _createClass(Form, null, [{
    key: 'hideAlert',
    value: function hideAlert(form) {
      var alert = form.querySelector('.alert');
      if (!alert) return;
      alert.style.display = 'none';
      alert.className = 'alert';
      alert.innerHTML = '';
    }
  }, {
    key: 'showAlert',
    value: function showAlert(form, status, messages) {
      var alert = form.querySelector('.alert');
      if (!alert) return;
      alert.style.display = 'block';
      alert.classList.add(status);
      alert.focus();
      var ul = document.createElement('ul');
      alert.appendChild(ul);
      messages.forEach(function (message) {
        var li = document.createElement('li');
        li.innerHTML = message.label;
        ul.appendChild(li);
      });
    }
  }, {
    key: 'getFormInputsAsData',
    value: function getFormInputsAsData(form, token) {
      var elements = form.querySelectorAll('input,select,textarea');
      var data = [];
      elements.forEach(function (el) {
        if (el.type === 'checkbox') {
          data.push(encodeURIComponent(el.name) + '=' + encodeURIComponent(el.checked));
        } else {
          data.push(encodeURIComponent(el.name) + '=' + encodeURIComponent(el.value));
        }
      });
      data.push('token=' + token);
      return data.join('&').replace(/%20/g, '+');
    }
  }, {
    key: 'handleFormSubmit',
    value: function handleFormSubmit(form, token) {
      Form.hideAlert(form); // remove any previous alerts
      var errors = _validator2.default.validate(form); // Carry out validation
      if (errors.length > 0) {
        Form.showAlert(form, 'alert-danger', errors);
      } else {
        _ajax2.default.postAjax(form.action, Form.getFormInputsAsData(form, token)) // Url based on submitted form action
        .then(JSON.parse).then(function (data) {
          if (data.status === 'success') {
            Form.showAlert(form, 'alert-success', [{ name: '', label: 'Form submitted successfully' }]);
            setTimeout(function () {
              Form.hideAlert(form);
            }, 3000);
            form.reset();
          } else {
            Form.showAlert(form, 'alert-danger', data.messages);
          }
        }).catch(function (err) {
          return console.error(err);
        });
      }
      form.elements['send'].disabled = false;
      form.elements['send'].innerHTML = 'Send Message';
    }
  }]);

  return Form;
}();

exports.default = Form;

/***/ }),

/***/ 8:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Validator = function () {
  function Validator() {
    _classCallCheck(this, Validator);
  }

  _createClass(Validator, null, [{
    key: 'isValidEmail',
    value: function isValidEmail(input) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(input.value);
    }
  }, {
    key: 'hasValue',
    value: function hasValue(input) {
      return input.value !== '';
    }
  }, {
    key: 'capitalize',
    value: function capitalize(words) {
      return words.charAt(0).toUpperCase() + words.slice(1);
    }
  }, {
    key: 'errorMessage',
    value: function errorMessage(name, message) {
      return { input: name, label: Validator.capitalize(name) + ' ' + message };
    }
  }, {
    key: 'validate',
    value: function validate(form) {
      var elements = form.querySelectorAll('input,select,textarea');
      var errors = [];
      elements.forEach(function (el) {
        if (el.required && !Validator.hasValue(el)) {
          errors.push(Validator.errorMessage(el.name, 'is required'));
        }
        if (el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'textarea') {
          //Validators only needed on input not selects
          switch (el.type) {// Based on the type text, email, number etc
            case 'email':
              {
                if (!Validator.isValidEmail(el)) {
                  errors.push(Validator.errorMessage(el.name, 'is not valid format'));
                }
                break;
              }
          }
        }
      });
      return errors;
    }
  }]);

  return Validator;
}();

exports.default = Validator;

/***/ })

},[7]);