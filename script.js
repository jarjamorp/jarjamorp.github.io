function openModal(imageElement) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const captionText = document.getElementById("caption");
    
    modal.style.display = "block";

    // Remove "-tn" from the thumbnail src to get the large image src
    const largeImageSrc = imageElement.src.replace("-tn", "");

    modalImg.src = largeImageSrc;
    captionText.innerHTML = imageElement.alt; 
    modalImg.style.border = "1px solid gray";  
}


function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}

// flexmasonry dist code 
var FlexMasonry=function(e){var n={};function t(r){if(n[r])return n[r].exports;var o=n[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,t),o.l=!0,o.exports}return t.m=e,t.c=n,t.d=function(e,n,r){t.o(e,n)||Object.defineProperty(e,n,{enumerable:!0,get:r})},t.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},t.t=function(e,n){if(1&n&&(e=t(e)),8&n)return e;if(4&n&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(t.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&n&&"string"!=typeof e)for(var o in e)t.d(r,o,function(n){return e[n]}.bind(null,o));return r},t.n=function(e){var n=e&&e.__esModule?function(){return e.default}:function(){return e};return t.d(n,"a",n),n},t.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},t.p="",t(t.s=0)}([function(e,n,t){t(1),e.exports=t(2)},function(e,n,t){},function(e,n,t){"use strict";t.r(n);const r={responsive:!0,breakpointCols:{"min-width: 1500px":5,"min-width: 1200px":5,"min-width: 992px":4,"min-width: 768px":3,"min-width: 576px":2},numCols:4};let o=null,i={},s=[];function a(){s.forEach(function(e){c(e)})}function l(){o&&window.cancelAnimationFrame(o),o=window.requestAnimationFrame(function(){y()})}function c(e){if(d()<2)return void e.style.removeProperty("height");let n=[];Array.from(e.children).forEach(function(e){if(e.classList.contains("flexmasonry-break"))return;const t=window.getComputedStyle(e),r=t.getPropertyValue("order"),o=t.getPropertyValue("height");n[r-1]||(n[r-1]=0),n[r-1]+=Math.ceil(parseFloat(o))});const t=Math.max(...n);e.style.height=t+"px"}function f(e){const n=e.querySelectorAll(".flexmasonry-break");if(Array.from(n).length!==d()-1)for(let n=1;n<d();n++){const t=document.createElement("div");t.classList.add("flexmasonry-break"),t.classList.add("flexmasonry-break-"+n),e.appendChild(t)}}function u(e){e.classList.contains("flexmasonry-cols-"+d())||(e.className=e.className.replace(/(flexmasonry-cols-\d+)/,""),e.classList.add("flexmasonry-cols-"+d()))}function d(){if(!i.responsive)return i.numCols;const e=Object.keys(i.breakpointCols);for(const n of e)if(window.matchMedia("("+n+")").matches)return i.breakpointCols[n];return 1}function m(e,n={}){return i=Object.assign(r,n),u(e),function(e){const n=e.querySelectorAll(".flexmasonry-break");Array.from(n).length!==d()-1&&Array.from(n).forEach(function(e){e.parentNode.removeChild(e)})}(e),f(e),c(e),this}function y(e={}){return s.forEach(function(n){m(n,e)}),this}n.default={init:function(e,n={}){return s="string"==typeof e?document.querySelectorAll(e):e,i=Object.assign(r,n),s.forEach(function(e){!function(e){e.classList.add("flexmasonry"),i.responsive&&e.classList.add("flexmasonry-responsive"),u(e),Array.from(e.children).forEach(function(e){e.classList.add("flexmasonry-item")}),f(e)}(e),c(e)}),window.addEventListener("load",a),window.addEventListener("resize",l),this},refresh:m,refreshAll:y,destroyAll:function(){window.removeEventListener("load",a),window.removeEventListener("resize",l)}}}]).default;