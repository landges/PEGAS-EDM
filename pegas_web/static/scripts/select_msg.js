$(document).ready(function () {
	sel_all_chbx = document.getElementById("check-all");
	delete_btn = document.getElementsByName("delete")[0];
	tospam_btn = document.getElementsByName("tospam")[0];
	sel_all_chbx.onclick = function(event) {
	  checkboxes = document.getElementsByClassName('b-form-checkbox');
	  for(var i=0, n=checkboxes.length;i<n;i++) {
	    checkboxes[i].checked = sel_all_chbx.checked;
  		}
	}
	//when deleting messages or setting them to spam we call ajax function
	delete_btn.onclick = function(event) {
		sel_all_chbx.chacked = false;
		var msgs_sel = [];
		all_msgs = document.getElementsByClassName('b-messages__message');
		for(var i=0, n=all_msgs.length;i<n;i++){
			if (all_msgs[i].getElementsByClassName('b-form-checkbox')[0].checked==true) {
				msgs_sel.push(all_msgs[i].querySelector('[name="msg_id"]').value);
			}
		}
	 	$.ajax({
	 		data:  {
	          type:'delete',
	          msgs:'msgs_sel',
       		},
	 		type: 'POST',
	 		url: "{% url 'messages' %}",
	 		success: function (response) {
	 			if (response.complete){
	 				for(var i=0, n=msgs_sel.length;i<n;i++){
	 					msgs_sel[i].remove();
	 				}
	 			}
	 		}
	 		 error: function (response) {
                      // sign about error
                      console.log(response.responseJSON.errors)
                }
	 	})
	}
})