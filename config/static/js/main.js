const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(() => { // call back function
  $('#message').fadeOut("slow"); // 比得'$' , jQuery function
  // 3秒後漫漫消失 , bootstrap 4.2 version
},3000);