from basic_handler import *

class HottestPost(Handler):
	def get(self):
		post_numdata_comments =  numdata_comments_all_post()
		dic_hottest_posts = hottest_posts(post_numdata_comments, 5)
		# ordering
		# data structure of this behavior
		#  idpost				number of comments,   postentity
		# [('5710932114145280', [6, <models.blog_model.Blog object at 0x04428110>])
		dic_hottest_posts = sort_dictionary_desc(dic_hottest_posts)
		
		hottest_category = numcomments_all_category()
		logging.error(hottest_category)
		self.render("hottest.html", dic_hottest_posts = dic_hottest_posts)
