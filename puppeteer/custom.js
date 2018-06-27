var elems = document.body.getElementsByTagName("*");
var len = elems.length

for (var i=0;i<len;i++) {

    if (window.getComputedStyle(elems[i],null).getPropertyValue('position') == 'fixed') {
        elems[i].parentNode.removeChild(elems[i])
    }

}
