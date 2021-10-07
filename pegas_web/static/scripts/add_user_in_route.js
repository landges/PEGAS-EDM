var $add_user =document.getElementsByClassName('add_user')[0];
var $form_for_route = document.getElementsByClassName('form_for_route')[0];
$add_user.addEventListener('click', function(event)
{
	var $input = document.createElement('input');
	$input.type = 'text';
	$input.placeholder = 'Узел*';
	$input.classList.add('user_was_added_in_route');
	$input.classList.add('padding10px');
	$form_for_route.insertBefore($input, $add_user);
});