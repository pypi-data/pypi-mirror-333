class AdminBlogApiUrl:
    BLOGS = '/api/v4/admin/blogs'
    BLOG_DETAILS = '/api/v4/admin/blogs/{id}'
    BLOG_COUNT = '/api/v4/admin/blogs/count'
    BLOG_COMMENTS = '/api/v4/admin/blogs/{id}/comments'
    BLOG_COMMENT_APPROVE = '/api/v4/admin/blogs/{id}/comments/{comment_id}/approve'
    BLOG_COMMENT_SPAM = '/api/v4/admin/blogs/{id}/comments/{comment_id}/mark-spam'
    BLOG_CATEGORIES = '/api/v4/admin/blog_categories'
    BLOG_CATEGORY_DETAILS = '/api/v4/admin/blog_categories/{category_id}'
