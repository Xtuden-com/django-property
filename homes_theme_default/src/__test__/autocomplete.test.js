import Autocomplete from '../js/components/autocomplete';
import Ajax from '../js/components/ajax';


test('should remove class from classList',() => {
  let el = document.createElement('input');
  el.classList.add('spinner');
  Autocomplete.hideSpinner(el);
  expect(el.classList.contains('spinner')).toBe(false);
});

test('should add class to classList', () => {
  let el = document.createElement('input');
  Autocomplete.showSpinner(el);
  expect(el.classList.contains('spinner')).toBe(true);
});

test('should change passed element to block and remove children', () => {
  let el1 = document.createElement('div');
  let el2 = document.createElement('div')
  el1.style.display = 'none';
  el2.innerHTML = 'Test';
  el1.appendChild(el2);
  Autocomplete.showResults(el1);
  expect(el1.style.display).toBe('block');
  expect(el1.innerHTML).toBe('');
});

test('should changed passed element to display none', () => {
  let el = document.createElement('div');
  el.style.display = 'block';
  Autocomplete.hideResults(el);
  expect(el.style.display).toBe('none');
});

test('list with entries added is created and added to passed element', () => {

  let el1 = document.createElement('div'); //location
  let el2 = document.createElement('div'); //results
  let items = [{label:'test1'},{label:'test2'}]

  Autocomplete.createResultsList(el1, el2, items);

  expect(el2.hasChildNodes()).toBe(true);
  expect(el2.childNodes.length).toBe(1);
  expect(el2.childNodes[0].tagName).toBe('UL');
  expect(el2.childNodes[0].childNodes.length).toBe(2);
  expect(el2.childNodes[0].childNodes[0].tagName).toBe('LI'); // First item
  expect(el2.childNodes[0].childNodes[0].childNodes.length).toBe(1);
  expect(el2.childNodes[0].childNodes[0].childNodes[0].tagName).toBe('A');
  expect(el2.childNodes[0].childNodes[0].childNodes[0].getAttribute('href')).toBe('javascript:void(0);');
  expect(el2.childNodes[0].childNodes[0].childNodes[0].innerHTML).toBe(items[0].label);
  expect(el2.childNodes[0].childNodes[1].tagName).toBe('LI'); // Second item
  expect(el2.childNodes[0].childNodes[1].childNodes.length).toBe(1);
  expect(el2.childNodes[0].childNodes[1].childNodes[0].tagName).toBe('A');
  expect(el2.childNodes[0].childNodes[1].childNodes[0].getAttribute('href')).toBe('javascript:void(0);');
  expect(el2.childNodes[0].childNodes[1].childNodes[0].innerHTML).toBe(items[1].label);

});

test('main function', () => {

});