// ajax call
function enable_disable_ajax(post_id)
{
	$.ajax(
	{
		type : "POST",
		url : "/change_status",
		contentType: 'application/json',
		datatype : "json",
		// sent json to the server
		data : JSON.stringify({"post_id" : post_id}),
	})
	.done(function(data)
	{
		var link_id = "#" + post_id 
		var row_id = "#row_" + post_id;
		console.log(data["status"]);
		//json_reponse
		if(data["status"] == "true")
		{
			$(link_id).text("Disable");
			$(link_id).addClass("error-text");
			$(link_id).addClass("little-text");
			// quit focus when ajax
			$(link_id).blur();
			console.log(row_id);
			// changing row color
			$(row_id).addClass("good-panel");
			$(row_id).removeClass("error-panel");
		}
		else if(data["status"] == "false")
		{
			$(link_id).text("Enable");
			$(link_id).removeClass("error-text");
			// changing row color
			$(row_id).addClass("error-panel");
			$(row_id).removeClass("good-panel")
			$(link_id).blur();
		}
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
	return;
}

function delete_post(post_id)
{
	$.ajax(
	{
		type : "POST",
		url : "/administration",
		contentType: 'application/json',
		datatype : "json",
		// sent json to the server
		data : JSON.stringify({"post_id" : post_id, "action" : "delete_post"}),
	})
	.done(function(data)
	{
		console.log(data);
		
		// deleting post from the grid
		var row_id = "#row_" + post_id;
		console.log(row_id)
		$(row_id).remove();
			
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});	
}