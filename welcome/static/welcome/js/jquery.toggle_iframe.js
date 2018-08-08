$(document).ready(function(){
   $(".getLobFiles").find("input[type='submit']").click(function() {
   	$("#iframe").css("display","block");   		   
	});
   $(".dlBlobFiles").click(function() {
   	$("#iframe").css("display","block");   		   
	});
	$("iframe").load(function(){
      var iframe = $("iframe").contents();
      iframe.find(".back").click(function(){
         window.parent.$('#iframe').css('display','none'); 
      });
   });
});  