function test(){
    alert("测试函数");
}

function getChatMessage(obj,chat_id){
	
    $.ajax({
        url: "{% url 'chatMessage' %}",
        type:'GET',
        data:{
            chat_id:chat_id,
        }
        cache:false,
        success:function(data){
            console.log(data)
            $('.chat-main').empty();
        },
        error:function(xhr){
            console.log(xhr)
        }
    })
}