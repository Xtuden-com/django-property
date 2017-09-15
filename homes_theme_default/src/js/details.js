import Form from './components/form';
import Pricing from './components/pricing';
import Autocomplete from './components/autocomplete';
import Toggler from './components/toggler';

(function(){
  Pricing.search();
  Autocomplete.google();
  Toggler.addToggleHandler();
  Form.addSubmitHandler();
})();
