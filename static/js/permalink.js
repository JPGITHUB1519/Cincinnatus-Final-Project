function insert_comment(post_id, subject, content)
{
	$.ajax(
	{
		type : "POST",
		url : "/" + post_id,
		contentType : "application/json",
		datatype : "json",
		data : JSON.stringify({"subject" : subject, "content" : content, "action" : "insert"})
	})
	.done(function(response)
	{
		var string_html = "<div class='well'><div class='row little-padding'><div class='col-md-1'><img src='/img_serve/%user_id%'></div><div class='col-md-11'><h4>%user_name% <span class='text-light little-margin-left size-minus-one'>%date% </span></h4><p>%content%</p></div></div></div>";
		string_html = string_html.replace("%user_id%", response["data"]["user_id"]);
		string_html = string_html.replace("%user_name%", response["data"]["username"]);
		string_html = string_html.replace("%date%", response["data"]["date"]);
		string_html = string_html.replace("%content%", response["data"]["content"]);
		$("#comment-container").prepend(string_html);
		$("#subject").val('');
		$("#content").val('');
		$("#total_comments").text(response["data"]["total_comments"]);
		console.log(response);

	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	})
}

function report_comment(post_id, comment_id, user_id, reason)
{	
	$.ajax(
	{
		type : "POST",
		url : "/" + post_id,
		contentType : "application/json",
		datatype : "json",
		data : JSON.stringify({"comment_id" : comment_id, "user_id" : user_id, "reason" : reason, "action" : "report"})
	})
	.done(function(response)
	{
		var cond_error = false;
		if(response["error_comment"])
		{
			$("#error_reason").text(response["error_comment"]);
			cond_error = true;
		}
		if(response["error"])
		{
			$("#error_report").text(response["error_report"]);
			cond_error = true;
		}
		// if there was no error
		if (cond_error == false)
		{
			console.log(response);
			$('#report_modal').modal('toggle');
			$('#report_text').val("");
			$('#error_reason').text("");
			$('#error_report').text("");
		}	
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
}

$(document).ready(function()
{
	$("#btn_submit_comment").click(function(e)
	{
		e.preventDefault();
		var subject = $("#subject").val();
		var content = $("#content").val();
		var post_id = $("#btn_submit_comment").data("post-id");
		insert_comment(post_id, subject, content);
	});

	$(document).on("click", '.reporter', function (e) 
	{
		// open modal
		e.preventDefault();
		$("#report_modal").modal();
		// add the data of the comment to the textarea
		$('#report_text').attr("data-comment", $(this).data("comment"));
	});

	// report button comment
	$("#report_button").click(function(e)
	{
		e.preventDefault();
		// take idcomment, user_reporter, reason
		var idcomment = $("#report_text").data("comment");
		// getting the actual user by the hidden input
		var user_reporter = $("#user_session").val();
		var reason = $("#report_text").val();
		var post_id = $("#post_id").val();
		// call ajax call 
		report_comment(post_id, idcomment, user_reporter, reason);
	});

	$("#close_report_modal").click(function(e)
	{
		e.preventDefault();
		$('#report_text').val("");
		$('#error_reason').text("");
		$('#error_report').text("");
	});
});