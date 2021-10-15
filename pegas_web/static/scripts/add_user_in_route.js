var $add_user =document.getElementsByClassName('add_user')[0];
var $del_user = document.getElementsByClassName('del_user')[0];
var $form_for_route = document.getElementsByClassName('form_for_route')[0];
var beforeinput = document.getElementById("bu")[0];
var index=0;
$add_user.addEventListener('click', function(event)
{
	index+=1;
	var $input = document.createElement('input');
	$input.type = 'text';
	$input.placeholder = 'Узел*';
	$input.name=`node[]`;
	$input.classList.add('user_was_added_in_route');
	$input.classList.add('padding10px');

	$form_for_route.insertBefore($input, beforeinput);
});
$del_user.addEventListener('click', function(event)
{
	console.log('click syka');
	var inputs=document.getElementsByName('node[]');
	if(inputs.length>1){
		$(inputs[inputs.length-1]).remove();
	}
});