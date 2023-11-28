var obj=null;
var As=document.querySelector(".w_header_nav").getElementsByTagName('a');
obj = As[0];
for(i=1;i<As.length;i++){if(window.location.href.indexOf(As[i].href)>=0)
obj=As[i];}
console.log(obj)
// 添加class属性
obj.classList.add("active");
