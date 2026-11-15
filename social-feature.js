document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('[data-social-video]').forEach(function(stage){
    var player=stage.querySelector('video');var cover=stage.querySelector('[data-social-play]');
    if(!player||!cover)return;
    cover.addEventListener('click',function(){
      cover.hidden=true;
      try{var p=player.play();if(p&&typeof p.catch==='function')p.catch(function(){cover.hidden=false;player.focus()});}
      catch(e){cover.hidden=false;player.focus()}
    });
    player.addEventListener('playing',function(){cover.hidden=true});
  });
});
