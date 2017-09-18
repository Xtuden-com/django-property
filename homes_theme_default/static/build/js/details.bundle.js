window["details"] =
webpackJsonp_name_([0],{

/***/ 5:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _pricing = __webpack_require__(1);

var _pricing2 = _interopRequireDefault(_pricing);

var _autocomplete = __webpack_require__(2);

var _autocomplete2 = _interopRequireDefault(_autocomplete);

var _toggler = __webpack_require__(6);

var _toggler2 = _interopRequireDefault(_toggler);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

(function () {
  _pricing2.default.search();
  _autocomplete2.default.google();
  _toggler2.default.addToggleHandler();
})();

/***/ }),

/***/ 6:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _ajax = __webpack_require__(0);

var _ajax2 = _interopRequireDefault(_ajax);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Toggler = function () {
  function Toggler() {
    _classCallCheck(this, Toggler);
  }

  _createClass(Toggler, null, [{
    key: 'toggle',
    value: function toggle(link) {

      _ajax2.default.getAjax(link.getAttribute('href')) // Url based on submitted form action
      .then(JSON.parse).then(function (data) {
        if (data.status === 200) {
          var icon = link.querySelector('.fa');
          if (icon) {
            if (icon.classList.contains(link.getAttribute('data-active'))) {
              icon.classList.remove(link.getAttribute('data-active'));
              icon.classList.add(link.getAttribute('data-inactive'));
            } else {
              icon.classList.remove(link.getAttribute('data-inactive'));
              icon.classList.add(link.getAttribute('data-active'));
            }
          }
        }
      }).catch(function (err) {
        return console.error(err);
      });
    }
  }, {
    key: 'addToggleHandler',
    value: function addToggleHandler() {
      var links = document.querySelectorAll('.toggle--link');

      links.forEach(function (link) {
        link.addEventListener('click', function (e) {
          e.preventDefault();
          Toggler.toggle(this);
        });
      });
    }
  }]);

  return Toggler;
}();

exports.default = Toggler;

/***/ })

},[5]);