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
		console.log(data["status"]);
		//json_reponse
		if(data["status"] == "true")
		{
			$(link_id).text("Disable");
			$(link_id).addClass("error-text");
			$(link_id).addClass("little-text");
			// quit focus when ajax
			$(link_id).blur();
		}
		else if(data["status"] == "false")
		{
			$(link_id).text("Enable");
			$(link_id).removeClass("error-text");
			$(link_id).blur();
		}
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
	return;
}