$(document).ready(function () {
	sel_all_chbx = document.getElementById("check-all");
	delete_btn = document.getElementsByName("delete")[0];
	fav_btn = document.getElementsByName("tofavourite")[0];
	sel_all_chbx.onclick = function(event) {
	  checkboxes = document.getElementsByClassName('b-form-checkbox');
	  for(var i=0, n=checkboxes.length;i<n;i++) {
	    checkboxes[i].checked = sel_all_chbx.checked;
  		}
	}
	//when deleting messages or setting them to spam we call ajax function
	delete_btn.onclick = function(event) {
		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		sel_all_chbx.checked = false;
		var msgs_sel = [];
		var msgs_2del = [];
		all_msgs = document.getElementsByClassName('b-messages__message');
		for(var i=0, n=all_msgs.length;i<n;i++){
			if (all_msgs[i].getElementsByClassName('b-form-checkbox')[0].checked==true) {
				msgs_sel.push(all_msgs[i].querySelector('[name="msg_id"]').value);
				msgs_2del.push(all_msgs[i]);
			}
		}
		function csrfSafeMethod(method) {
	        // these HTTP methods do not require CSRF protection
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }

	    $.ajaxSetup({
	        beforeSend: function (xhr, settings) {
	            // if not safe, set csrftoken
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", csrftoken);
	            }
	        }
	    });

	 	$.ajax({
	 		type: 'POST',
	 		csrftoken,
	 		url: '',
	 		data:  {
	          type:'delete',
	          msgs: msgs_sel,
       		},
	 		
	 		success: function (response) {
	 			if (response.complete){
	 				for(var i=0, n=msgs_2del.length;i<n;i++){
	 					console.log(msgs_2del[i]);
	 					$(msgs_2del[i]).remove();
	 				}
	 				
	 			}
	 		},
	 		error: function (response) {
                // sign about error
                console.log(response.responseJSON.errors);
	        }
	 	});
	 	return false;
	}
	fav_btn.onclick = function(event) {
		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		sel_all_chbx.checked = false;
		var msgs_sel = [];
		var msgs_2del = [];
		all_msgs = document.getElementsByClassName('b-messages__message');
		for(var i=0, n=all_msgs.length;i<n;i++){
			if (all_msgs[i].getElementsByClassName('b-form-checkbox')[0].checked==true) {
				msgs_sel.push(all_msgs[i].querySelector('[name="msg_id"]').value);
			}
		}
		function csrfSafeMethod(method) {
	        // these HTTP methods do not require CSRF protection
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }

	    $.ajaxSetup({
	        beforeSend: function (xhr, settings) {
	            // if not safe, set csrftoken
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", csrftoken);
	            }
	        }
	    });

	 	$.ajax({
	 		type: 'POST',
	 		csrftoken,
	 		url: '',
	 		data:  {
	          type:'tofavourite',
	          msgs: msgs_sel,
       		},
	 		
	 		success: function (response) {
	 			if (response.complete){
	 					console.log('successfully tipped messages as favourite');
	 			}
	 			else{
	 				console.log('failed to tip messages as favourite');
	 			}
	 		},
	 		error: function (response) {
                // sign about error
                console.log(response.responseJSON.errors);
	        }
	 	});
	 	return false;
	}
});